#!/usr/bin/env python3
"""
ASUSE (Annual Survey of Unincorporated Sector Enterprises) Tests
Tests all ASUSE API calls with proper validation
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
# ASUSE FREQUENCIES TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_asuse_frequencies(client):
    """Test getting ASUSE frequencies list"""
    result = await call_tool(client, "get_asuse_frequencies")

    assert result is not None
    assert "data" in result, "Should return data array"

    frequencies = result["data"]
    assert isinstance(frequencies, list), "Data should be a list"
    assert len(frequencies) >= 1, "Should have at least 1 frequency"


# ============================================================================
# ASUSE INDICATORS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_asuse_indicators(client):
    """Test getting ASUSE indicators list"""
    result = await call_tool(client, "get_asuse_indicators")

    assert result is not None
    assert "data" in result, "Should return data array"

    indicators = result["data"]
    assert isinstance(indicators, list), "Data should be a list"
    assert len(indicators) >= 30, f"Should have at least 30 indicators, got {len(indicators)}"


@pytest.mark.asyncio
async def test_asuse_indicators_structure(client):
    """Test ASUSE indicators have correct structure"""
    result = await call_tool(client, "get_asuse_indicators")

    indicator = result["data"][0]
    assert "indicator_code" in indicator, "Should have indicator_code"
    assert "description" in indicator, "Should have description"


@pytest.mark.asyncio
async def test_asuse_indicators_quarterly(client):
    """Test getting ASUSE quarterly indicators"""
    result = await call_tool(client, "get_asuse_indicators", frequency_code=2)

    assert result is not None
    assert "data" in result, "Should return data array"


# ============================================================================
# ASUSE METADATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_asuse_metadata_indicator_1(client):
    """Test ASUSE metadata for indicator 1 (has activity filter)"""
    result = await call_tool(client, "get_asuse_metadata",
                            indicator_code=1)

    assert result is not None
    assert isinstance(result, dict)
    assert "data" in result

    data = result["data"]
    assert "activity" in data, "Indicator 1 should have activity filter"


@pytest.mark.asyncio
async def test_asuse_metadata_has_sector(client):
    """Test ASUSE metadata contains sector filter"""
    result = await call_tool(client, "get_asuse_metadata",
                            indicator_code=1)

    assert "data" in result
    data = result["data"]
    assert "sector" in data, "Should have sector filter"

    sectors = data["sector"]
    assert isinstance(sectors, list), "Sectors should be a list"
    assert len(sectors) >= 2, "Should have at least 2 sectors"


@pytest.mark.asyncio
async def test_asuse_metadata_has_year(client):
    """Test ASUSE metadata contains year filter"""
    result = await call_tool(client, "get_asuse_metadata",
                            indicator_code=1)

    assert "data" in result
    data = result["data"]
    assert "year" in data, "Should have year filter"

    years = data["year"]
    assert isinstance(years, list), "Years should be a list"
    assert len(years) >= 2, "Should have at least 2 years"


@pytest.mark.asyncio
async def test_asuse_metadata_indicator_20(client):
    """Test ASUSE metadata for indicator 20 (has sub_indicator and broad_activity_category)"""
    result = await call_tool(client, "get_asuse_metadata",
                            indicator_code=20)

    assert result is not None
    assert "data" in result

    data = result["data"]
    assert "sub_indicator" in data, "Indicator 20 should have sub_indicator filter"
    assert "broad_activity_category" in data, "Indicator 20 should have broad_activity_category filter"


@pytest.mark.asyncio
async def test_asuse_metadata_indicator_15(client):
    """Test ASUSE metadata for indicator 15 (has state and operation_duration)"""
    result = await call_tool(client, "get_asuse_metadata",
                            indicator_code=15)

    assert result is not None
    assert "data" in result

    data = result["data"]
    assert "state" in data, "Indicator 15 should have state filter"


# ============================================================================
# ASUSE DATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_asuse_data_basic(client):
    """Test basic ASUSE data query"""
    result = await call_tool(client, "get_asuse_data",
                            indicator_code="1",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_asuse_data_with_sector(client):
    """Test ASUSE data with sector filter"""
    result = await call_tool(client, "get_asuse_data",
                            indicator_code="1",
                            sector_code="3",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_asuse_data_with_establishment_type(client):
    """Test ASUSE data with establishment type filter"""
    result = await call_tool(client, "get_asuse_data",
                            indicator_code="1",
                            establishment_type_code="3",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_asuse_data_with_year(client):
    """Test ASUSE data with year filter"""
    result = await call_tool(client, "get_asuse_data",
                            indicator_code="1",
                            year="2022-23",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_asuse_data_indicator_20_with_sub_indicator(client):
    """Test ASUSE data for indicator 20 with sub_indicator"""
    result = await call_tool(client, "get_asuse_data",
                            indicator_code="20",
                            sub_indicator_code="5",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_asuse_data_indicator_20_with_broad_activity(client):
    """Test ASUSE data for indicator 20 with broad_activity_category"""
    result = await call_tool(client, "get_asuse_data",
                            indicator_code="20",
                            broad_activity_category_code="1",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_asuse_data_pagination(client):
    """Test ASUSE data with pagination"""
    result = await call_tool(client, "get_asuse_data",
                            indicator_code="1",
                            page=1,
                            limit=5)

    assert_valid_api_response(result)
    assert "data" in result


# ============================================================================
# SUMMARY
# ============================================================================
# Total: 18 tests covering:
# - Frequencies endpoint
# - Indicators endpoint (annual and quarterly)
# - Metadata endpoint (various indicators with different filters)
# - Data endpoint (various filters including sector, establishment_type, year)
# - Special indicators (20 with sub_indicator and broad_activity_category)
# - Pagination
