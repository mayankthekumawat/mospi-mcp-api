#!/usr/bin/env python3
"""
RBI Statistics Tests
Tests all RBI API calls with proper validation
"""

import pytest
import pytest_asyncio
from fastmcp import Client

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
    if "error" in response and response.get("statusCode") is False:
        pytest.fail(f"API returned error: {response.get('error')}")
    assert "data" in response or "statusCode" in response or "count" in response, \
        f"Response should have 'data', 'statusCode', or 'count': {response}"


# ============================================================================
# RBI INDICATORS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_rbi_indicators(client):
    """Test getting RBI indicators list"""
    result = await call_tool(client, "get_rbi_indicators")
    assert result is not None
    assert "data" in result
    indicators = result["data"]
    assert isinstance(indicators, list)
    assert len(indicators) >= 35, f"Should have at least 35 indicators, got {len(indicators)}"


@pytest.mark.asyncio
async def test_rbi_indicators_structure(client):
    """Test RBI indicators have correct structure"""
    result = await call_tool(client, "get_rbi_indicators")
    indicator = result["data"][0]
    assert "sub_indicator_code" in indicator or "indicator_code" in indicator, "Should have indicator code"


# ============================================================================
# RBI METADATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_rbi_metadata_foreign_trade(client):
    """Test RBI metadata for foreign trade indicator (1)"""
    result = await call_tool(client, "get_rbi_metadata", sub_indicator_code=1)
    assert result is not None
    assert "data" in result
    data = result["data"]
    assert isinstance(data, list) and len(data) > 0, "Should have data array"
    dimensions = data[0].get("dimensions", {})
    assert "year" in dimensions, "Foreign trade should have year filter in dimensions"


@pytest.mark.asyncio
async def test_rbi_metadata_forex_reserves(client):
    """Test RBI metadata for forex reserves indicator (47)"""
    result = await call_tool(client, "get_rbi_metadata", sub_indicator_code=47)
    assert result is not None
    assert "data" in result
    data = result["data"]
    assert isinstance(data, list) and len(data) > 0, "Should have data array"
    dimensions = data[0].get("dimensions", {})
    assert "year" in dimensions, "Forex reserves should have year filter in dimensions"


@pytest.mark.asyncio
async def test_rbi_metadata_exchange_rates(client):
    """Test RBI metadata for exchange rates indicator (33)"""
    result = await call_tool(client, "get_rbi_metadata", sub_indicator_code=33)
    assert result is not None
    assert "data" in result
    assert isinstance(result["data"], list), "Should have data array"


# ============================================================================
# RBI DATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_rbi_data_basic(client):
    """Test basic RBI data query"""
    result = await call_tool(client, "get_rbi_data",
                            sub_indicator_code="1",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_rbi_data_forex_reserves(client):
    """Test RBI forex reserves data"""
    result = await call_tool(client, "get_rbi_data",
                            sub_indicator_code="47",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_rbi_data_exchange_rates(client):
    """Test RBI exchange rates data"""
    result = await call_tool(client, "get_rbi_data",
                            sub_indicator_code="33",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_rbi_data_bop(client):
    """Test RBI balance of payments data"""
    result = await call_tool(client, "get_rbi_data",
                            sub_indicator_code="5",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_rbi_data_external_debt(client):
    """Test RBI external debt data"""
    result = await call_tool(client, "get_rbi_data",
                            sub_indicator_code="25",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_rbi_data_pagination(client):
    """Test RBI data with pagination"""
    result = await call_tool(client, "get_rbi_data",
                            sub_indicator_code="1",
                            page=1,
                            limit=5)
    assert_valid_api_response(result)
