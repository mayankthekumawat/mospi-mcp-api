#!/usr/bin/env python3
"""
CPIALRL (CPI for Agricultural Labourers and Rural Labourers) Tests
Tests all CPIALRL API calls with proper validation
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
# CPIALRL INDICATORS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_cpialrl_indicators(client):
    """Test getting CPIALRL indicators list"""
    result = await call_tool(client, "get_cpialrl_indicators")
    assert result is not None
    assert "data" in result
    indicators = result["data"]["indicator"]
    assert isinstance(indicators, list)
    assert len(indicators) >= 2, f"Should have at least 2 indicators, got {len(indicators)}"


@pytest.mark.asyncio
async def test_cpialrl_indicators_structure(client):
    """Test CPIALRL indicators have correct structure"""
    result = await call_tool(client, "get_cpialrl_indicators")
    indicator = result["data"]["indicator"][0]
    assert "indicator_code" in indicator, "Should have indicator_code"


# ============================================================================
# CPIALRL METADATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_cpialrl_metadata_general_index(client):
    """Test CPIALRL metadata for General Index (indicator 1)"""
    result = await call_tool(client, "get_cpialrl_metadata", indicator_code=1)
    assert result is not None
    assert "data" in result


@pytest.mark.asyncio
async def test_cpialrl_metadata_group_index(client):
    """Test CPIALRL metadata for Group Index (indicator 2)"""
    result = await call_tool(client, "get_cpialrl_metadata", indicator_code=2)
    assert result is not None
    assert "data" in result


# ============================================================================
# CPIALRL DATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_cpialrl_data_general_index(client):
    """Test CPIALRL General Index data"""
    result = await call_tool(client, "get_cpialrl_data",
                            indicator_code="1",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_cpialrl_data_group_index(client):
    """Test CPIALRL Group Index data"""
    result = await call_tool(client, "get_cpialrl_data",
                            indicator_code="2",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_cpialrl_data_with_base_year(client):
    """Test CPIALRL data with base year filter"""
    result = await call_tool(client, "get_cpialrl_data",
                            indicator_code="1",
                            base_year="2019",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_cpialrl_data_pagination(client):
    """Test CPIALRL data with pagination"""
    result = await call_tool(client, "get_cpialrl_data",
                            indicator_code="1",
                            page=1,
                            limit=5)
    assert_valid_api_response(result)
