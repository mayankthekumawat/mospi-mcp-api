"""
NFHS (National Family Health Survey) Tools
"""

from typing import Optional, Dict, Any, Literal
from ..client import mospi


def register_nfhs_tools(mcp):
    """Register all NFHS tools with the MCP server."""

    @mcp.tool()
    def get_nfhs_indicators() -> Dict[str, Any]:
        """
        Get list of NFHS (National Family Health Survey) indicators from MoSPI API.

        Returns:
            List of 21 indicators covering health, mortality, nutrition,
            family planning, women's empowerment, and more.
        """
        return mospi.get_nfhs_indicators()

    @mcp.tool()
    def get_nfhs_metadata(indicator_code: int) -> Dict[str, Any]:
        """
        Get NFHS metadata directly from MoSPI API.

        Returns available filters for the given indicator.

        Args:
            indicator_code: Indicator code 1-21 (use get_nfhs_indicators for list)

        Returns:
            Available filters: state, sub_indicator, sector, survey
        """
        return mospi.get_nfhs_filters(indicator_code=indicator_code)

    @mcp.tool()
    def get_nfhs_data(
        indicator_code: str,
        state_code: Optional[str] = None,
        sub_indicator_code: Optional[str] = None,
        sector_code: Optional[str] = None,
        survey_code: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get National Family Health Survey (NFHS) data from MoSPI.

        NFHS provides data on population, health, family planning, nutrition,
        infant mortality, women's empowerment, and more.

        Note: Available filters vary by indicator. Use get_nfhs_metadata() to see
        which filters are available for your specific indicator.

        Args:
            indicator_code: Indicator code 1-21 (use get_nfhs_indicators for list)
            state_code: State code (use get_nfhs_metadata for valid values, 99=All India)
            sub_indicator_code: Sub-indicator code (varies by indicator)
            sector_code: 1=Rural, 2=Urban, 3=Combined
            survey_code: 2=NFHS-4, 3=NFHS-5
            page: Page number
            limit: Max records per page
            Format: JSON or CSV
        """
        params = {
            "indicator_code": indicator_code,
            "state_code": state_code,
            "sub_indicator_code": sub_indicator_code,
            "sector_code": sector_code,
            "survey_code": survey_code,
            "page": page,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("NFHS", params)
