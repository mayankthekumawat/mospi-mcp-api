#!/usr/bin/env python3
"""
NFHS (National Family Health Survey) Tests
Tests all NFHS API calls with proper validation
"""

import pytest
import pytest_asyncio
from fastmcp import Client

# Test Configuration - uses HTTP transport
MCP_SERVER_URL = "http://localhost:8000/mcp"


@pytest_asyncio.fixture
async def client():
    """Fixture for MCP client connection using HTTP transport"""
    async with Client(MCP_SERVER_URL) as c:
        yield c


async def call_tool(client, tool_name, **params):
    """Helper to call MCP tool and extract data"""
    result = await client.call_tool(tool_name, params)
    return result.data if hasattr(result, 'data') else result


def assert_valid_api_response(response):
    """Assert response is a valid API response with data"""
    assert response is not None, "Response should not be None"
    assert isinstance(response, dict), "Response should be a dict"

    # Check for successful response
    if "error" in response and response.get("statusCode") is False:
        pytest.fail(f"API returned error: {response.get('error')}")

    # Valid responses should have data or statusCode
    assert "data" in response or "statusCode" in response or "count" in response, \
        f"Response should have 'data', 'statusCode', or 'count': {response}"


# ============================================================================
# NFHS INDICATORS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_nfhs_indicators(client):
    """Test getting NFHS indicators list"""
    result = await call_tool(client, "get_nfhs_indicators")

    assert result is not None
    assert "data" in result, "Should return data array"

    indicators = result["data"]
    assert isinstance(indicators, list), "Data should be a list"
    assert len(indicators) >= 20, f"Should have at least 20 indicators, got {len(indicators)}"


@pytest.mark.asyncio
async def test_nfhs_indicators_structure(client):
    """Test NFHS indicators have correct structure"""
    result = await call_tool(client, "get_nfhs_indicators")

    indicator = result["data"][0]
    assert "indicator_code" in indicator, "Should have indicator_code"
    assert "label" in indicator, "Should have label"


# ============================================================================
# NFHS METADATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_nfhs_metadata(client):
    """Test NFHS metadata for indicator 1"""
    result = await call_tool(client, "get_nfhs_metadata",
                            indicator_code=1)

    assert result is not None
    assert isinstance(result, dict)
    assert "data" in result


@pytest.mark.asyncio
async def test_nfhs_metadata_has_state(client):
    """Test NFHS metadata contains state filter"""
    result = await call_tool(client, "get_nfhs_metadata",
                            indicator_code=1)

    assert "data" in result
    data = result["data"]
    assert "state" in data, "Should have state filter"

    states = data["state"]
    assert isinstance(states, list), "States should be a list"
    assert len(states) >= 30, "Should have at least 30 states/UTs"


@pytest.mark.asyncio
async def test_nfhs_metadata_has_survey(client):
    """Test NFHS metadata contains survey filter"""
    result = await call_tool(client, "get_nfhs_metadata",
                            indicator_code=1)

    assert "data" in result
    data = result["data"]
    assert "survey" in data, "Should have survey filter"

    surveys = data["survey"]
    assert isinstance(surveys, list), "Surveys should be a list"
    assert len(surveys) >= 2, "Should have NFHS-4 and NFHS-5"


# ============================================================================
# NFHS DATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_nfhs_data_basic(client):
    """Test basic NFHS data query"""
    result = await call_tool(client, "get_nfhs_data",
                            indicator_code="1",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_nfhs_data_infant_mortality(client):
    """Test NFHS infant mortality data (indicator 4)"""
    result = await call_tool(client, "get_nfhs_data",
                            indicator_code="4",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_nfhs_data_with_state(client):
    """Test NFHS data with state filter"""
    result = await call_tool(client, "get_nfhs_data",
                            indicator_code="4",
                            state_code="99",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_nfhs_data_with_survey(client):
    """Test NFHS data with survey filter"""
    result = await call_tool(client, "get_nfhs_data",
                            indicator_code="4",
                            survey_code="3",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_nfhs_data_with_sector(client):
    """Test NFHS data with sector filter"""
    result = await call_tool(client, "get_nfhs_data",
                            indicator_code="4",
                            sector_code="1",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_nfhs_data_pagination(client):
    """Test NFHS data with pagination"""
    result = await call_tool(client, "get_nfhs_data",
                            indicator_code="1",
                            page=1,
                            limit=5)

    assert_valid_api_response(result)
    assert "data" in result


# ============================================================================
# SUMMARY
# ============================================================================
# Total: 13 tests covering:
# - Indicators endpoint
# - Metadata endpoint (state, survey filters)
# - Data endpoint (various filters)
# - Pagination
