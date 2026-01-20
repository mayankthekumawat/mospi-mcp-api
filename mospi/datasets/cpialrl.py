"""
CPIALRL (CPI for Agricultural Labourers and Rural Labourers) Dataset Module

Provides access to MoSPI CPIALRL API with 2 indicators:
- General Index: Overall CPI for agricultural and rural labourers
- Group Index: CPI by commodity groups

Covers price indices for agricultural labourers (AL) and rural labourers (RL)
across Indian states with monthly data.
"""

from typing import Dict, Any, Optional, Literal
from ..client import mospi


def register_cpialrl_tools(mcp):
    """Register all CPIALRL tools with the MCP server."""

    @mcp.tool()
    def get_cpialrl_indicators() -> Dict[str, Any]:
        """
        Get list of CPIALRL indicators from MoSPI API.

        Returns 2 indicators:
        1. General Index - Overall CPI for agricultural/rural labourers
        2. Group Index - CPI by commodity groups

        Returns:
            List of indicators with codes and descriptions
        """
        return mospi.get_cpialrl_indicators()

    @mcp.tool()
    def get_cpialrl_metadata(indicator_code: int) -> Dict[str, Any]:
        """
        Get CPIALRL metadata directly from MoSPI API.
        Returns available filters for the given indicator.

        Common filters include:
        - base_year: Base year for index (1986-1987 or 2019)
        - year: Data year
        - month_code: Month (1-12)
        - state_code: State/UT code

        Args:
            indicator_code: Indicator code (1=General Index, 2=Group Index)

        Returns:
            Available filters specific to that indicator
        """
        return mospi.get_cpialrl_filters(indicator_code=indicator_code)

    @mcp.tool()
    def get_cpialrl_data(
        indicator_code: str,
        base_year: Optional[str] = None,
        year: Optional[str] = None,
        month_code: Optional[str] = None,
        state_code: Optional[str] = None,
        group_code: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get CPI for Agricultural Labourers and Rural Labourers data from MoSPI.

        Provides monthly consumer price indices for agricultural labourers (AL)
        and rural labourers (RL) across Indian states.

        IMPORTANT: Available filters vary by indicator.
        Always call get_cpialrl_metadata() first to see which filters apply.

        Args:
            indicator_code: Required. 1=General Index, 2=Group Index
            base_year: Base year for index (e.g., "1986-1987" or "2019")
            year: Data year (e.g., "2023-2024")
            month_code: Month code 1-12
            state_code: State/UT code (use get_cpialrl_metadata for codes)
            group_code: Commodity group code (for Group Index)
            page: Page number
            limit: Max records per page
            Format: JSON or CSV
        """
        params = {
            "indicator_code": indicator_code,
            "base_year": base_year,
            "year": year,
            "month_code": month_code,
            "state_code": state_code,
            "group_code": group_code,
            "page": page,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("CPIALRL", params)
