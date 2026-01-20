#!/usr/bin/env python3
"""
NSS77 (Land and Livestock Holdings Survey) Tests
Tests all NSS77 API calls with proper validation
"""

import pytest
import pytest_asyncio
from fastmcp import Client

MCP_SERVER_URL = "http://localhost:8000/mcp"


@pytest_asyncio.fixture
async def client():
    async with Client(MCP_SERVER_URL) as c:
        yield c


async def call_tool(client, tool_name, **params):
    result = await client.call_tool(tool_name, params)
    return result.data if hasattr(result, 'data') else result


def assert_valid_api_response(response):
    assert response is not None
    assert isinstance(response, dict)
    if "error" in response and response.get("statusCode") is False:
        pytest.fail(f"API returned error: {response.get('error')}")
    assert "data" in response or "statusCode" in response or "count" in response


# ============================================================================
# NSS77 INDICATORS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_nss77_indicators(client):
    """Test getting NSS77 indicators list"""
    result = await call_tool(client, "get_nss77_indicators")
    assert result is not None
    assert "data" in result
    indicators = result["data"]
    assert isinstance(indicators, list)
    assert len(indicators) >= 30, f"Should have at least 30 indicators, got {len(indicators)}"


@pytest.mark.asyncio
async def test_nss77_indicators_structure(client):
    """Test NSS77 indicators have correct structure"""
    result = await call_tool(client, "get_nss77_indicators")
    indicator = result["data"][0]
    assert "indicator_code" in indicator, "Should have indicator_code"


# ============================================================================
# NSS77 METADATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_nss77_metadata_land_holdings(client):
    """Test NSS77 metadata for land holdings indicator (16)"""
    result = await call_tool(client, "get_nss77_metadata", indicator_code=16)
    assert result is not None
    assert "data" in result


@pytest.mark.asyncio
async def test_nss77_metadata_income(client):
    """Test NSS77 metadata for income indicator (24)"""
    result = await call_tool(client, "get_nss77_metadata", indicator_code=24)
    assert result is not None
    assert "data" in result


@pytest.mark.asyncio
async def test_nss77_metadata_livestock(client):
    """Test NSS77 metadata for livestock indicator (39)"""
    result = await call_tool(client, "get_nss77_metadata", indicator_code=39)
    assert result is not None
    assert "data" in result


# ============================================================================
# NSS77 DATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_nss77_data_land_holdings(client):
    """Test NSS77 land holdings data"""
    result = await call_tool(client, "get_nss77_data",
                            indicator_code="16",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_nss77_data_income(client):
    """Test NSS77 agricultural income data"""
    result = await call_tool(client, "get_nss77_data",
                            indicator_code="24",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_nss77_data_livestock(client):
    """Test NSS77 livestock ownership data"""
    result = await call_tool(client, "get_nss77_data",
                            indicator_code="39",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_nss77_data_crop_insurance(client):
    """Test NSS77 crop insurance data"""
    result = await call_tool(client, "get_nss77_data",
                            indicator_code="48",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_nss77_data_with_state(client):
    """Test NSS77 data with state filter"""
    result = await call_tool(client, "get_nss77_data",
                            indicator_code="16",
                            state_code="37",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_nss77_data_pagination(client):
    """Test NSS77 data with pagination"""
    result = await call_tool(client, "get_nss77_data",
                            indicator_code="16",
                            page=1,
                            limit=5)
    assert_valid_api_response(result)
