"""
HCES (Household Consumption Expenditure Survey) Tools
"""

from typing import Optional, Dict, Any, Literal
from ..client import mospi


def register_hces_tools(mcp):
    """Register all HCES tools with the MCP server."""

    @mcp.tool()
    def get_hces_indicators() -> Dict[str, Any]:
        """
        Get list of HCES indicators from MoSPI API.

        Returns:
            List of 9 indicators with codes and descriptions
        """
        return mospi.get_hces_indicators()

    @mcp.tool()
    def get_hces_metadata(
        indicator_code: int = 1
    ) -> Dict[str, Any]:
        """
        Get HCES metadata directly from MoSPI API.

        Returns available filters for the given indicator.

        Args:
            indicator_code: 1-9 (use get_hces_indicators for list)

        Returns:
            Available filters: year, state, sector, imputation_type (varies by indicator)
        """
        return mospi.get_hces_filters(indicator_code=indicator_code)

    @mcp.tool()
    def get_hces_data(
        indicator_code: str = "1",
        year: Optional[str] = None,
        sub_indicator_code: Optional[str] = None,
        state_code: Optional[str] = None,
        sector_code: Optional[str] = None,
        imputation_type_code: Optional[str] = None,
        mpce_fractile_classes_code: Optional[str] = None,
        item_category_code: Optional[str] = None,
        cereal_code: Optional[str] = None,
        employment_of_households_code: Optional[str] = None,
        social_group_code: Optional[str] = None,
        page: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get Household Consumption Expenditure Survey (HCES) data from MoSPI.

        Note: Available filters vary by indicator. Use get_hces_metadata() to see
        which filters are available for your specific indicator.

        Args:
            indicator_code: 1-9 (use get_hces_indicators for descriptions)
            year: Year in YYYY-YY format (e.g., "2022-23")
            sub_indicator_code: Sub indicator code 1-3
            state_code: State code 1-37
            sector_code: Sector code 1-3
            imputation_type_code: Imputation type code 1-2
            mpce_fractile_classes_code: MPCE fractile classes code 1-13
            item_category_code: Item category code 1-31
            cereal_code: Cereal code 1-5
            employment_of_households_code: Employment of households code 1-11
            social_group_code: Social group code 1-5
            page: Page number
            Format: JSON or CSV
        """
        params = {
            "indicator_code": indicator_code,
            "year": year,
            "sub_indicator_code": sub_indicator_code,
            "state_code": state_code,
            "sector_code": sector_code,
            "imputation_type_code": imputation_type_code,
            "mpce_fractile_classes_code": mpce_fractile_classes_code,
            "item_category_code": item_category_code,
            "cereal_code": cereal_code,
            "employment_of_households_code": employment_of_households_code,
            "social_group_code": social_group_code,
            "page": page,
            "Format": Format
        }

        return mospi.get_data("HCES", params)
