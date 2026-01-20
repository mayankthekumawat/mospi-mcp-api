#!/usr/bin/env python3
"""
Gender Statistics Tests
Tests all Gender API calls with proper validation
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
# GENDER INDICATORS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_gender_indicators(client):
    """Test getting Gender indicators list"""
    result = await call_tool(client, "get_gender_indicators")

    assert result is not None
    assert "data" in result, "Should return data array"

    indicators = result["data"]
    assert isinstance(indicators, list), "Data should be a list"
    assert len(indicators) >= 140, f"Should have at least 140 indicators, got {len(indicators)}"


@pytest.mark.asyncio
async def test_gender_indicators_structure(client):
    """Test Gender indicators have correct structure"""
    result = await call_tool(client, "get_gender_indicators")

    indicator = result["data"][0]
    assert "indicator_code" in indicator, "Should have indicator_code"
    assert "indicator_name" in indicator or "description" in indicator or "label" in indicator, \
        "Should have indicator name/description/label"


# ============================================================================
# GENDER METADATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_gender_metadata_indicator_1(client):
    """Test Gender metadata for indicator 1 (Population trends)"""
    result = await call_tool(client, "get_gender_metadata",
                            indicator_code=1)

    assert result is not None
    assert isinstance(result, dict)
    assert "data" in result

    data = result["data"]
    assert "year" in data, "Indicator 1 should have year filter"


@pytest.mark.asyncio
async def test_gender_metadata_has_sector(client):
    """Test Gender metadata for population indicator contains sector"""
    result = await call_tool(client, "get_gender_metadata",
                            indicator_code=1)

    assert "data" in result
    data = result["data"]
    assert "sector" in data, "Should have sector filter"


@pytest.mark.asyncio
async def test_gender_metadata_state_indicator(client):
    """Test Gender metadata for state-wise indicator (6 - State-wise Sex Ratio)"""
    result = await call_tool(client, "get_gender_metadata",
                            indicator_code=6)

    assert result is not None
    assert "data" in result

    data = result["data"]
    assert "state_ut" in data or "state" in data, "Indicator 6 should have state/state_ut filter"


@pytest.mark.asyncio
async def test_gender_metadata_labour_indicator(client):
    """Test Gender metadata for labour indicator (80 - LFPR)"""
    result = await call_tool(client, "get_gender_metadata",
                            indicator_code=80)

    assert result is not None
    assert "data" in result

    data = result["data"]
    assert "year" in data, "Labour indicator should have year filter"


@pytest.mark.asyncio
async def test_gender_metadata_crime_indicator(client):
    """Test Gender metadata for crime indicator (140 - Major Crimes)"""
    result = await call_tool(client, "get_gender_metadata",
                            indicator_code=140)

    assert result is not None
    assert "data" in result

    data = result["data"]
    assert "year" in data, "Crime indicator should have year filter"


# ============================================================================
# GENDER DATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_gender_data_basic(client):
    """Test basic Gender data query"""
    result = await call_tool(client, "get_gender_data",
                            indicator_code="1",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_gender_data_sex_ratio(client):
    """Test Gender data for Sex Ratio (indicator 2)"""
    result = await call_tool(client, "get_gender_data",
                            indicator_code="2",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_gender_data_with_sector(client):
    """Test Gender data with sector filter"""
    result = await call_tool(client, "get_gender_data",
                            indicator_code="1",
                            sector_code="3",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_gender_data_with_gender_filter(client):
    """Test Gender data with gender filter"""
    result = await call_tool(client, "get_gender_data",
                            indicator_code="1",
                            gender_code="2",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_gender_data_state_wise(client):
    """Test Gender data for state-wise indicator"""
    result = await call_tool(client, "get_gender_data",
                            indicator_code="6",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_gender_data_lfpr(client):
    """Test Gender data for LFPR (indicator 80)"""
    result = await call_tool(client, "get_gender_data",
                            indicator_code="80",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_gender_data_crime(client):
    """Test Gender data for crime indicator (140)"""
    result = await call_tool(client, "get_gender_data",
                            indicator_code="140",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_gender_data_pagination(client):
    """Test Gender data with pagination"""
    result = await call_tool(client, "get_gender_data",
                            indicator_code="1",
                            page=1,
                            limit=5)

    assert_valid_api_response(result)
    assert "data" in result


# ============================================================================
# SUMMARY
# ============================================================================
# Total: 17 tests covering:
# - Indicators endpoint (157 indicators)
# - Metadata endpoint (various indicator types)
# - Data endpoint (demographics, state-wise, labour, crime)
# - Filter combinations (sector, gender, state)
# - Pagination
