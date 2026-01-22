"""
NSS78 (National Sample Survey 78th Round) Tools
"""

from typing import Optional, Dict, Any, Literal
from ..client import mospi


def register_nss78_tools(mcp):
    """Register all NSS78 tools with the MCP server."""

    @mcp.tool()
    def get_nss78_indicators() -> Dict[str, Any]:
        """
        Get list of NSS78 indicators from MoSPI API.

        Returns:
            List of 14 indicators with codes (2-15) and names
        """
        return mospi.get_nss78_indicators()

    @mcp.tool()
    def get_nss78_metadata(
        indicator_code: int,
        sub_indicator_code: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get NSS78 metadata directly from MoSPI API.

        Returns available filters for the given indicator.

        Args:
            indicator_code: Indicator code 2-15 (use get_nss78_indicators for list)
            sub_indicator_code: Sub-indicator code (optional)

        Returns:
            Available filters: sub_indicator, state, sector
        """
        return mospi.get_nss78_filters(
            indicator_code=indicator_code,
            sub_indicator_code=sub_indicator_code
        )

    @mcp.tool()
    def get_nss78_data(
        indicator_code: str,
        state_code: Optional[str] = None,
        sector_code: Optional[str] = None,
        gender_code: Optional[str] = None,
        agegroup_code: Optional[str] = None,
        internetaccess_code: Optional[str] = None,
        household_leavingreason_code: Optional[str] = None,
        subindicator_code: Optional[str] = None,
        households_code: Optional[str] = None,
        sourceoffinance_code: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get National Sample Survey (NSS 78th Round) data from MoSPI.

        Note: Available filters vary by indicator. Use get_nss78_metadata() to see
        which filters are available for your specific indicator.

        Args:
            indicator_code: Indicator code 2-15 (use get_nss78_indicators for list)
            state_code: State code 1-39
            sector_code: Sector code 1-3
            gender_code: Gender code 1-3
            agegroup_code: Age group code 1-2
            internetaccess_code: Internet access code 1-2
            household_leavingreason_code: Household leaving reason code 1-18
            subindicator_code: Sub-indicator code 1-34
            households_code: Households code 1-3
            sourceoffinance_code: Source of finance code 1-5
            page: Page number
            limit: Max records per page
            Format: JSON or CSV
        """
        params = {
            "indicator_code": indicator_code,
            "state_code": state_code,
            "sector_code": sector_code,
            "gender_code": gender_code,
            "agegroup_code": agegroup_code,
            "internetaccess_code": internetaccess_code,
            "household_leavingreason_code": household_leavingreason_code,
            "subindicator_code": subindicator_code,
            "households_code": households_code,
            "sourceoffinance_code": sourceoffinance_code,
            "page": page,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("NSS78", params)
