#!/usr/bin/env python3
"""
TUS (Time Use Survey) Tests
Tests all TUS API calls with proper validation
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
# TUS INDICATORS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_tus_indicators(client):
    """Test getting TUS indicators list"""
    result = await call_tool(client, "get_tus_indicators")

    assert result is not None
    assert "data" in result, "Should return data array"

    indicators = result["data"]
    assert isinstance(indicators, list), "Data should be a list"
    assert len(indicators) >= 40, f"Should have at least 40 indicators, got {len(indicators)}"


@pytest.mark.asyncio
async def test_tus_indicators_structure(client):
    """Test TUS indicators have correct structure"""
    result = await call_tool(client, "get_tus_indicators")

    indicator = result["data"][0]
    assert "indicator_code" in indicator, "Should have indicator_code"
    assert "description" in indicator, "Should have description"


# ============================================================================
# TUS METADATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_tus_metadata(client):
    """Test TUS metadata for indicator 4"""
    result = await call_tool(client, "get_tus_metadata",
                            indicator_code=4)

    assert result is not None
    assert isinstance(result, dict)
    assert "data" in result


@pytest.mark.asyncio
async def test_tus_metadata_has_filters(client):
    """Test TUS metadata contains expected filters"""
    result = await call_tool(client, "get_tus_metadata",
                            indicator_code=4)

    data = result["data"]
    # TUS should have year, sector, gender, age_group filters
    assert "year" in data or "sector" in data or "gender" in data, \
        "Should have standard filters"


@pytest.mark.asyncio
async def test_tus_metadata_has_gender(client):
    """Test TUS metadata contains gender filter"""
    result = await call_tool(client, "get_tus_metadata",
                            indicator_code=4)

    assert "data" in result
    data = result["data"]
    assert "gender" in data, "Should have gender filter"

    genders = data["gender"]
    assert isinstance(genders, list), "Genders should be a list"
    assert len(genders) >= 2, "Should have at least Male and Female"


# ============================================================================
# TUS DATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_tus_data_basic(client):
    """Test basic TUS data query"""
    result = await call_tool(client, "get_tus_data",
                            indicator_code="4",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_tus_data_with_year(client):
    """Test TUS data with year filter"""
    result = await call_tool(client, "get_tus_data",
                            indicator_code="4",
                            year="2019",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_tus_data_with_sector(client):
    """Test TUS data with sector filter"""
    result = await call_tool(client, "get_tus_data",
                            indicator_code="4",
                            sector_code="1",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_tus_data_with_gender(client):
    """Test TUS data with gender filter"""
    result = await call_tool(client, "get_tus_data",
                            indicator_code="4",
                            gender_code="1",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_tus_data_different_indicator(client):
    """Test TUS data for different indicator"""
    result = await call_tool(client, "get_tus_data",
                            indicator_code="9",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_tus_data_pagination(client):
    """Test TUS data with pagination"""
    result = await call_tool(client, "get_tus_data",
                            indicator_code="4",
                            page=1,
                            limit=5)

    assert_valid_api_response(result)
    assert "data" in result


# ============================================================================
# SUMMARY
# ============================================================================
# Total: 12 tests covering:
# - Indicators endpoint
# - Metadata endpoint (filters validation)
# - Data endpoint (various filters)
# - Pagination
