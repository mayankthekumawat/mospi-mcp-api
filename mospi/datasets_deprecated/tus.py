"""
TUS (Time Use Survey) Tools
"""

from typing import Optional, Dict, Any, Literal
from ..client import mospi


def register_tus_tools(mcp):
    """Register all TUS tools with the MCP server."""

    @mcp.tool()
    def get_tus_indicators() -> Dict[str, Any]:
        """
        Get list of TUS (Time Use Survey) indicators from MoSPI API.

        Returns:
            List of 41 indicators (codes 4-44) covering time use patterns,
            paid/unpaid activities, and demographic breakdowns.
        """
        return mospi.get_tus_indicators()

    @mcp.tool()
    def get_tus_metadata(indicator_code: int) -> Dict[str, Any]:
        """
        Get TUS metadata directly from MoSPI API.

        Returns available filters for the given indicator.

        Args:
            indicator_code: Indicator code 4-44 (use get_tus_indicators for list)

        Returns:
            Available filters: year, sector, gender, age_group, icatus_activity, etc.
        """
        return mospi.get_tus_filters(indicator_code=indicator_code)

    @mcp.tool()
    def get_tus_data(
        indicator_code: str,
        year: Optional[str] = None,
        state_code: Optional[str] = None,
        sector_code: Optional[str] = None,
        gender_code: Optional[str] = None,
        age_group_code: Optional[str] = None,
        icatus_activity_code: Optional[str] = None,
        day_of_week_code: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get Time Use Survey (TUS) data from MoSPI.

        TUS measures how people spend their time across different activities
        including paid work, unpaid domestic work, caregiving, leisure, etc.

        Note: Available filters vary by indicator. Use get_tus_metadata() to see
        which filters are available for your specific indicator.

        Args:
            indicator_code: Indicator code 4-44 (use get_tus_indicators for list)
            year: Year ("2019" or "2024")
            state_code: State code (use get_tus_metadata for valid values)
            sector_code: 1=Rural, 2=Urban, 3=Combined
            gender_code: 1=Male, 2=Female, 4=Person
            age_group_code: Age group code (1-5)
            icatus_activity_code: ICATUS activity code
            day_of_week_code: Day type code
            page: Page number
            limit: Max records per page
            Format: JSON or CSV
        """
        params = {
            "indicator_code": indicator_code,
            "year": year,
            "state_code": state_code,
            "sector_code": sector_code,
            "gender_code": gender_code,
            "age_group_code": age_group_code,
            "icatus_activity_code": icatus_activity_code,
            "day_of_week_code": day_of_week_code,
            "page": page,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("TUS", params)
