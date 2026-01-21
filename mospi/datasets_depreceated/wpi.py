"""
WPI (Wholesale Price Index) Tools
"""

from typing import Optional, Dict, Any, Literal
from ..client import mospi


def register_wpi_tools(mcp):
    """Register all WPI tools with the MCP server."""

    @mcp.tool()
    def get_wpi_metadata() -> Dict[str, Any]:
        """
        Get WPI metadata directly from MoSPI API.

        Returns available filters and their valid values.

        Returns:
            Available filters: year, month, major_group, group, sub_group, sub_sub_group, item
        """
        return mospi.get_wpi_filters()

    @mcp.tool()
    def get_wpi_data(
        year: Optional[str] = None,
        month_code: Optional[str] = None,
        major_group_code: Optional[str] = None,
        group_code: Optional[str] = None,
        sub_group_code: Optional[str] = None,
        sub_sub_group_code: Optional[str] = None,
        item_code: Optional[str] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get Wholesale Price Index (WPI) data from MoSPI.

        Note: Use get_wpi_metadata() to see available filter values.

        Args:
            year: Year in YYYY format (e.g., "2023")
            month_code: Month 1-12
            major_group_code: Major group code (use get_wpi_metadata for values)
            group_code: Group code (use get_wpi_metadata for values)
            sub_group_code: Sub-group code (use get_wpi_metadata for values)
            sub_sub_group_code: Sub-sub-group code (use get_wpi_metadata for values)
            item_code: Item code (use get_wpi_metadata for values)
            limit: Max records
            Format: JSON or CSV
        """
        params = {
            "year": year,
            "month_code": month_code,
            "major_group_code": major_group_code,
            "group_code": group_code,
            "sub_group_code": sub_group_code,
            "sub_sub_group_code": sub_sub_group_code,
            "item_code": item_code,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("WPI", params)
