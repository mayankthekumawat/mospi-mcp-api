#!/usr/bin/env python3
"""
Environment Statistics Tests
Tests all EnvStats API calls with proper validation
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
# ENVSTATS INDICATORS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_envstats_indicators(client):
    """Test getting EnvStats indicators list"""
    result = await call_tool(client, "get_envstats_indicators")
    assert result is not None
    assert "data" in result
    indicators = result["data"]
    assert isinstance(indicators, list)
    assert len(indicators) >= 100, f"Should have at least 100 indicators, got {len(indicators)}"


@pytest.mark.asyncio
async def test_envstats_indicators_structure(client):
    """Test EnvStats indicators have correct structure"""
    result = await call_tool(client, "get_envstats_indicators")
    indicator = result["data"][0]
    assert "indicator_code" in indicator, "Should have indicator_code"


# ============================================================================
# ENVSTATS METADATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_envstats_metadata_climate(client):
    """Test EnvStats metadata for climate indicator (1)"""
    result = await call_tool(client, "get_envstats_metadata", indicator_code=1)
    assert result is not None
    assert "data" in result


@pytest.mark.asyncio
async def test_envstats_metadata_biodiversity(client):
    """Test EnvStats metadata for biodiversity indicator (16)"""
    result = await call_tool(client, "get_envstats_metadata", indicator_code=16)
    assert result is not None
    assert "data" in result


@pytest.mark.asyncio
async def test_envstats_metadata_forest(client):
    """Test EnvStats metadata for forest indicator (18)"""
    result = await call_tool(client, "get_envstats_metadata", indicator_code=18)
    assert result is not None
    assert "data" in result


# ============================================================================
# ENVSTATS DATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_envstats_data_basic(client):
    """Test basic EnvStats data query"""
    result = await call_tool(client, "get_envstats_data",
                            indicator_code="1",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_envstats_data_forest(client):
    """Test EnvStats forest data"""
    result = await call_tool(client, "get_envstats_data",
                            indicator_code="18",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_envstats_data_pollution(client):
    """Test EnvStats air quality data"""
    result = await call_tool(client, "get_envstats_data",
                            indicator_code="25",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_envstats_data_disaster(client):
    """Test EnvStats disaster data"""
    result = await call_tool(client, "get_envstats_data",
                            indicator_code="87",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_envstats_data_pagination(client):
    """Test EnvStats data with pagination"""
    result = await call_tool(client, "get_envstats_data",
                            indicator_code="1",
                            page=1,
                            limit=5)
    assert_valid_api_response(result)
