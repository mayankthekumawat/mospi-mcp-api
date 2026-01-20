#!/usr/bin/env python3
"""
NSS78 (National Sample Survey 78th Round) Tests
Tests all NSS78 API calls with proper validation
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
    assert "data" in response or "statusCode" in response or "indicator" in response, \
        f"Response should have 'data', 'statusCode', or 'indicator': {response}"


# ============================================================================
# NSS78 INDICATORS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_nss78_indicators(client):
    """Test getting NSS78 indicators list"""
    result = await call_tool(client, "get_nss78_indicators")

    assert result is not None
    assert "indicator" in result, "Should return indicator array"

    indicators = result["indicator"]
    assert isinstance(indicators, list), "Indicators should be a list"
    assert len(indicators) >= 14, f"Should have at least 14 indicators, got {len(indicators)}"


@pytest.mark.asyncio
async def test_nss78_indicators_structure(client):
    """Test NSS78 indicators have correct structure"""
    result = await call_tool(client, "get_nss78_indicators")

    indicator = result["indicator"][0]
    assert "code" in indicator, "Should have code"
    assert "name" in indicator, "Should have name"


# ============================================================================
# NSS78 METADATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_nss78_metadata(client):
    """Test NSS78 metadata for indicator 2"""
    result = await call_tool(client, "get_nss78_metadata",
                            indicator_code=2)

    assert result is not None
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_nss78_metadata_with_subindicator(client):
    """Test NSS78 metadata with sub-indicator"""
    result = await call_tool(client, "get_nss78_metadata",
                            indicator_code=2,
                            sub_indicator_code=8)

    assert result is not None
    # Should have filter arrays
    assert "sub_indicator" in result or "state" in result or "sector" in result


@pytest.mark.asyncio
async def test_nss78_metadata_has_state(client):
    """Test NSS78 metadata contains state information"""
    result = await call_tool(client, "get_nss78_metadata",
                            indicator_code=2,
                            sub_indicator_code=8)

    assert "state" in result, "Should have state filter"
    states = result["state"]
    assert isinstance(states, list), "States should be a list"


# ============================================================================
# NSS78 DATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_nss78_data_basic(client):
    """Test basic NSS78 data query"""
    result = await call_tool(client, "get_nss78_data",
                            indicator_code="2",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_nss78_data_with_state(client):
    """Test NSS78 data with state filter"""
    result = await call_tool(client, "get_nss78_data",
                            indicator_code="2",
                            state_code="1",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_nss78_data_with_sector(client):
    """Test NSS78 data with sector filter"""
    result = await call_tool(client, "get_nss78_data",
                            indicator_code="2",
                            sector_code="1",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_nss78_data_different_indicator(client):
    """Test NSS78 data for different indicator"""
    result = await call_tool(client, "get_nss78_data",
                            indicator_code="3",
                            limit=10)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_nss78_data_pagination(client):
    """Test NSS78 data with pagination"""
    result = await call_tool(client, "get_nss78_data",
                            indicator_code="2",
                            page=1,
                            limit=5)

    assert_valid_api_response(result)
    assert "data" in result


@pytest.mark.asyncio
async def test_nss78_data_csv_format(client):
    """Test NSS78 data with CSV format"""
    result = await call_tool(client, "get_nss78_data",
                            indicator_code="2",
                            Format="CSV",
                            limit=10)

    assert result is not None
    assert isinstance(result, dict)
    assert "data" in result


# ============================================================================
# SUMMARY
# ============================================================================
# Total: 12 tests covering:
# - Indicators endpoint
# - Metadata endpoint (with and without sub-indicator)
# - Data endpoint (various filters)
# - Pagination and format options
