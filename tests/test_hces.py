#!/usr/bin/env python3
"""
HCES (Household Consumption Expenditure Survey) Tests
Tests all HCES API calls with proper validation
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
    assert "data" in response or "statusCode" in response, \
        f"Response should have 'data' or 'statusCode': {response}"


# ============================================================================
# HCES INDICATORS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_hces_indicators(client):
    """Test getting HCES indicators list"""
    result = await call_tool(client, "get_hces_indicators")

    assert_valid_api_response(result)
    assert "data" in result, "Should return indicators data"

    data = result["data"]
    assert isinstance(data, list), "Data should be a list"
    assert len(data) >= 9, f"Should have at least 9 indicators, got {len(data)}"


@pytest.mark.asyncio
async def test_hces_indicators_structure(client):
    """Test HCES indicators have correct structure"""
    result = await call_tool(client, "get_hces_indicators")

    assert_valid_api_response(result)
    indicator = result["data"][0]
    assert "indicator_code" in indicator, "Should have indicator_code"
    assert "description" in indicator, "Should have description"


# ============================================================================
# HCES METADATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_hces_metadata_default(client):
    """Test HCES metadata with default indicator"""
    result = await call_tool(client, "get_hces_metadata")

    assert_valid_api_response(result)
    assert "data" in result, "Should return metadata"


@pytest.mark.asyncio
async def test_hces_metadata_indicator_1(client):
    """Test HCES metadata for indicator 1"""
    result = await call_tool(client, "get_hces_metadata",
                            indicator_code=1)

    assert_valid_api_response(result)
    data = result["data"]
    assert "year" in data, "Should have year filter"
    assert "state" in data, "Should have state filter"
    assert "sector" in data, "Should have sector filter"


@pytest.mark.asyncio
async def test_hces_metadata_indicator_2(client):
    """Test HCES metadata for indicator 2"""
    result = await call_tool(client, "get_hces_metadata",
                            indicator_code=2)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_hces_metadata_has_states(client):
    """Test HCES metadata contains state information"""
    result = await call_tool(client, "get_hces_metadata",
                            indicator_code=1)

    assert_valid_api_response(result)
    states = result["data"]["state"]
    assert isinstance(states, list), "States should be a list"
    assert len(states) >= 30, f"Should have 30+ states, got {len(states)}"


# ============================================================================
# HCES DATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_hces_data_default(client):
    """Test basic HCES data query"""
    result = await call_tool(client, "get_hces_data",
                            indicator_code="1")

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_hces_data_with_year(client):
    """Test HCES data with year filter"""
    result = await call_tool(client, "get_hces_data",
                            indicator_code="1",
                            year="2022-23")

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_hces_data_with_state(client):
    """Test HCES data with state filter"""
    result = await call_tool(client, "get_hces_data",
                            indicator_code="1",
                            state_code="1")

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_hces_data_with_sector(client):
    """Test HCES data with sector filter"""
    result = await call_tool(client, "get_hces_data",
                            indicator_code="1",
                            sector_code="1")

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_hces_data_indicator_2(client):
    """Test HCES data for indicator 2"""
    result = await call_tool(client, "get_hces_data",
                            indicator_code="2")

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_hces_data_indicator_3(client):
    """Test HCES data for indicator 3"""
    result = await call_tool(client, "get_hces_data",
                            indicator_code="3")

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_hces_data_pagination(client):
    """Test HCES data with pagination"""
    result = await call_tool(client, "get_hces_data",
                            indicator_code="1",
                            page=1)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_hces_data_csv_format(client):
    """Test HCES data with CSV format"""
    result = await call_tool(client, "get_hces_data",
                            indicator_code="1",
                            Format="CSV")

    assert result is not None
    assert isinstance(result, dict)
    assert "data" in result


# ============================================================================
# SUMMARY
# ============================================================================
# Total: 15 tests covering:
# - Indicators endpoint
# - Metadata endpoint (different indicators)
# - Data endpoint (various filters)
# - Pagination and format options
