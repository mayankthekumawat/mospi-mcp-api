#!/usr/bin/env python3
"""
AISHE (All India Survey on Higher Education) Tests
Tests all AISHE API calls with proper validation
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
# AISHE INDICATORS TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_aishe_indicators(client):
    """Test getting AISHE indicators list"""
    result = await call_tool(client, "get_aishe_indicators")
    assert result is not None
    assert "data" in result
    indicators = result["data"]
    assert isinstance(indicators, list)
    assert len(indicators) >= 9, f"Should have at least 9 indicators, got {len(indicators)}"


@pytest.mark.asyncio
async def test_aishe_indicators_structure(client):
    """Test AISHE indicators have correct structure"""
    result = await call_tool(client, "get_aishe_indicators")
    indicator = result["data"][0]
    assert "indicator_code" in indicator, "Should have indicator_code"


# ============================================================================
# AISHE METADATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_aishe_metadata_universities(client):
    """Test AISHE metadata for Number of Universities (indicator 1)"""
    result = await call_tool(client, "get_aishe_metadata", indicator_code=1)
    assert result is not None
    assert "data" in result


@pytest.mark.asyncio
async def test_aishe_metadata_colleges(client):
    """Test AISHE metadata for Number of Colleges (indicator 2)"""
    result = await call_tool(client, "get_aishe_metadata", indicator_code=2)
    assert result is not None
    assert "data" in result


@pytest.mark.asyncio
async def test_aishe_metadata_enrolment(client):
    """Test AISHE metadata for Student Enrolment (indicator 3)"""
    result = await call_tool(client, "get_aishe_metadata", indicator_code=3)
    assert result is not None
    assert "data" in result


@pytest.mark.asyncio
async def test_aishe_metadata_ger(client):
    """Test AISHE metadata for Gross Enrolment Ratio (indicator 6)"""
    result = await call_tool(client, "get_aishe_metadata", indicator_code=6)
    assert result is not None
    assert "data" in result


# ============================================================================
# AISHE DATA TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_aishe_data_universities(client):
    """Test AISHE Number of Universities data"""
    result = await call_tool(client, "get_aishe_data",
                            indicator_code="1",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_aishe_data_colleges(client):
    """Test AISHE Number of Colleges data"""
    result = await call_tool(client, "get_aishe_data",
                            indicator_code="2",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_aishe_data_enrolment(client):
    """Test AISHE Student Enrolment data"""
    result = await call_tool(client, "get_aishe_data",
                            indicator_code="3",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_aishe_data_ger(client):
    """Test AISHE Gross Enrolment Ratio data"""
    result = await call_tool(client, "get_aishe_data",
                            indicator_code="6",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_aishe_data_teachers(client):
    """Test AISHE Number of Teachers data"""
    result = await call_tool(client, "get_aishe_data",
                            indicator_code="9",
                            limit=10)
    assert_valid_api_response(result)


@pytest.mark.asyncio
async def test_aishe_data_pagination(client):
    """Test AISHE data with pagination"""
    result = await call_tool(client, "get_aishe_data",
                            indicator_code="1",
                            page=1,
                            limit=5)
    assert_valid_api_response(result)
