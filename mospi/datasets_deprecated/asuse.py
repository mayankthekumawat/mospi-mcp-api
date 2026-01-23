"""
ASUSE (Annual Survey of Unincorporated Sector Enterprises) Tools
"""

from typing import Optional, Dict, Any, Literal
from ..client import mospi


def register_asuse_tools(mcp):
    """Register all ASUSE tools with the MCP server."""

    @mcp.tool()
    def get_asuse_frequencies() -> Dict[str, Any]:
        """
        Get list of ASUSE frequencies from MoSPI API.

        Returns:
            List of frequencies: 1=Annually, 2=Quarterly
        """
        return mospi.get_asuse_frequencies()

    @mcp.tool()
    def get_asuse_indicators(frequency_code: int = 1) -> Dict[str, Any]:
        """
        Get list of ASUSE indicators from MoSPI API.

        Args:
            frequency_code: 1=Annually (default), 2=Quarterly

        Returns:
            List of 35+ indicators covering establishments, workers,
            GVA, emoluments, and enterprise characteristics.
        """
        return mospi.get_asuse_indicators(frequency_code=frequency_code)

    @mcp.tool()
    def get_asuse_metadata(
        indicator_code: int,
        frequency_code: int = 1
    ) -> Dict[str, Any]:
        """
        Get ASUSE metadata directly from MoSPI API.

        Returns available filters for the given indicator.

        Args:
            indicator_code: Indicator code (use get_asuse_indicators for list)
            frequency_code: 1=Annually (default), 2=Quarterly

        Returns:
            Available filters: year, sector, activity, state, establishment_type, etc.
        """
        return mospi.get_asuse_filters(
            indicator_code=indicator_code,
            frequency_code=frequency_code
        )

    @mcp.tool()
    def get_asuse_data(
        indicator_code: str,
        frequency_code: str = "1",
        year: Optional[str] = None,
        state_code: Optional[str] = None,
        sector_code: Optional[str] = None,
        activity_code: Optional[str] = None,
        establishment_type_code: Optional[str] = None,
        broad_activity_category_code: Optional[str] = None,
        sub_indicator_code: Optional[str] = None,
        owner_education_level_code: Optional[str] = None,
        location_establishment_code: Optional[str] = None,
        operation_duration_code: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get Annual Survey of Unincorporated Sector Enterprises (ASUSE) data from MoSPI.

        ASUSE covers non-agricultural unincorporated enterprises including
        manufacturing, trade, and services in the informal sector.

        IMPORTANT: Available filters vary by indicator. Use get_asuse_metadata() to see
        which filters are available for your specific indicator before querying.

        Common filter patterns:
        - Most indicators: year, sector, establishment_type
        - Indicator 1-4: activity (50 detailed categories)
        - Indicator 5-9: owner_education_level
        - Indicator 10+: location_establishment, operation_duration
        - Indicator 15+: state, broad_activity_category
        - Indicator 20+: sub_indicator, broad_activity_category

        Args:
            indicator_code: Indicator code (use get_asuse_indicators for list)
            frequency_code: "1"=Annually (default), "2"=Quarterly
            year: Year in YYYY-YY format (e.g., "2022-23")
            state_code: State code (only for some indicators)
            sector_code: 1=Rural, 2=Urban, 3=Combined
            activity_code: Detailed economic activity (50 categories, some indicators)
            establishment_type_code: 1=HWE, 2=OAE, 3=All
            broad_activity_category_code: 1=Manufacturing, 2=Trade, 3=Other Services, 4=All
            sub_indicator_code: Sub-indicator (e.g., 5=Using Computer, 6=Using Internet)
            owner_education_level_code: Education level of owner (some indicators)
            location_establishment_code: Location type (some indicators)
            operation_duration_code: Duration of operation (some indicators)
            page: Page number
            limit: Max records per page
            Format: JSON or CSV
        """
        params = {
            "indicator_code": indicator_code,
            "frequency_code": frequency_code,
            "year": year,
            "state_code": state_code,
            "sector_code": sector_code,
            "activity_code": activity_code,
            "establishment_type_code": establishment_type_code,
            "broad_activity_category_code": broad_activity_category_code,
            "sub_indicator_code": sub_indicator_code,
            "owner_education_level_code": owner_education_level_code,
            "location_establishment_code": location_establishment_code,
            "operation_duration_code": operation_duration_code,
            "page": page,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("ASUSE", params)
