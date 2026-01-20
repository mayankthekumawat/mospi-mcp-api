"""
NSS77 (National Sample Survey 77th Round) Dataset Module

Land and Livestock Holdings Survey (January - December 2019)

Provides access to MoSPI NSS-77 API with 33 indicators covering:
- Land holdings and possession by size class
- Agricultural household classification
- Income from various sources (wages, crops, animals, non-farm)
- Crop production expenses and receipts
- Livestock ownership
- Loan outstanding by source
- Crop insurance and loss data
"""

from typing import Dict, Any, Optional, Literal
from ..client import mospi


def register_nss77_tools(mcp):
    """Register all NSS77 tools with the MCP server."""

    @mcp.tool()
    def get_nss77_indicators() -> Dict[str, Any]:
        """
        Get list of NSS77 indicators from MoSPI API.

        Returns 33 indicators (codes 16-51) covering:
        - Land holdings by size class (16-19)
        - Crop disposal and farming resources (21-23)
        - Agricultural household income (24-25)
        - Expenditure on assets (26-27)
        - Crop production expenses (28-29)
        - Animal farming (31)
        - Non-farm business (32)
        - Loans outstanding (33)
        - Land ownership and leasing (34-37)
        - Livestock ownership (39)
        - Operational holdings (40-41)
        - Crop production and sales (42-47)
        - Crop insurance (48-51)

        Returns:
            List of indicators with codes and descriptions
        """
        return mospi.get_nss77_indicators()

    @mcp.tool()
    def get_nss77_metadata(indicator_code: int) -> Dict[str, Any]:
        """
        Get NSS77 metadata directly from MoSPI API.
        Returns available filters for the given indicator.

        IMPORTANT: Different indicators have different filters.
        Always call this before get_nss77_data() to know which filters apply.

        Common filters include:
        - state_code: State/UT code
        - visit_code: Survey visit (1 or 2)
        - land_possessed_household_code: Land size class
        - agricultural_household_code: Household type
        - caste_code: Social group (ST/SC/OBC/Others)
        - season_code: Survey period
        - sub_indicator_code: Specific sub-indicators

        Args:
            indicator_code: Indicator code 16-51 (use get_nss77_indicators for list)

        Returns:
            Available filters specific to that indicator
        """
        return mospi.get_nss77_filters(indicator_code=indicator_code)

    @mcp.tool()
    def get_nss77_data(
        indicator_code: str,
        state_code: Optional[str] = None,
        visit_code: Optional[str] = None,
        land_possessed_household_code: Optional[str] = None,
        agricultural_household_code: Optional[str] = None,
        caste_code: Optional[str] = None,
        season_code: Optional[str] = None,
        sub_indicator_code: Optional[str] = None,
        social_group_code: Optional[str] = None,
        size_class_code: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get NSS77 (Land and Livestock Holdings Survey) data from MoSPI.

        Survey period: January - December 2019

        Covers land holdings, agricultural income, crop production,
        livestock, loans, and insurance data for Indian households.

        IMPORTANT: Available filters vary significantly by indicator.
        Always call get_nss77_metadata() first to see which filters apply.

        Args:
            indicator_code: Required. Indicator code 16-51
            state_code: State/UT code (37=All India)
            visit_code: Survey visit (1 or 2)
            land_possessed_household_code: Land size class (1-8)
            agricultural_household_code: 1=Agricultural, 2=Non-agricultural, 3=All
            caste_code: 1=ST, 2=SC, 3=OBC, 4=Others, 5=All
            season_code: Survey period
            sub_indicator_code: Specific sub-indicator
            social_group_code: Social group filter
            size_class_code: Size class filter
            page: Page number
            limit: Max records per page
            Format: JSON or CSV
        """
        params = {
            "indicator_code": indicator_code,
            "state_code": state_code,
            "visit_code": visit_code,
            "land_possessed_household_code": land_possessed_household_code,
            "agricultural_household_code": agricultural_household_code,
            "caste_code": caste_code,
            "season_code": season_code,
            "sub_indicator_code": sub_indicator_code,
            "social_group_code": social_group_code,
            "size_class_code": size_class_code,
            "page": page,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("NSS77", params)
