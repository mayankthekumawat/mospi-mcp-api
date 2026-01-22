"""
CPI (Consumer Price Index) Tools
"""

from typing import Optional, Dict, Any, Literal
from ..client import mospi


def register_cpi_tools(mcp):
    """Register all CPI tools with the MCP server."""

    @mcp.tool()
    def get_cpi_metadata(
        base_year: Literal["2012", "2010"] = "2012",
        level: Literal["Group", "Item"] = "Group"
    ) -> Dict[str, Any]:
        """
        Get CPI metadata directly from MoSPI API.

        Returns available filters and their valid values for the given base year and level.

        Args:
            base_year: "2012" (default) or "2010" - determines available data range
            level: "Group" (default) returns series/year/month/state/sector/group/subgroup filters
                   "Item" returns year/month/item filters

        Returns:
            Available filters and their valid options from the API
        """
        return mospi.get_cpi_filters(base_year=base_year, level=level)

    @mcp.tool()
    def get_cpi_group_index(
        base_year: Literal["2012", "2010"] = "2012",
        series: Literal["Current", "Back"] = "Current",
        year: Optional[str] = None,
        month_code: Optional[str] = None,
        state_code: Optional[str] = None,
        group_code: Optional[str] = None,
        subgroup_code: Optional[str] = None,
        sector_code: Optional[str] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get CPI (Consumer Price Index) data by group/subgroup.

        Args:
            base_year: "2012" (default) or "2010"
            series: "Current" (default) or "Back"
            year: Year in YYYY format (e.g., "2023")
            month_code: Month 1-12
            state_code: State code (use get_cpi_metadata for valid values)
            group_code: Group code (use get_cpi_metadata for valid values)
            subgroup_code: Subgroup code (use get_cpi_metadata for valid values)
            sector_code: 1=Rural, 2=Urban, 3=Combined
            limit: Max records
            Format: JSON or CSV
        """
        params = {
            "base_year": base_year,
            "series": series,
            "year": year,
            "month_code": month_code,
            "state_code": state_code,
            "group_code": group_code,
            "subgroup_code": subgroup_code,
            "sector_code": sector_code,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("CPI_Group", params)

    @mcp.tool()
    def get_cpi_item_index(
        base_year: Literal["2012", "2010"] = "2012",
        year: Optional[str] = None,
        month_code: Optional[str] = None,
        item_code: Optional[str] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get CPI (Consumer Price Index) data by specific item.

        Args:
            base_year: "2012" (default) or "2010"
            year: Year in YYYY format (e.g., "2023")
            month_code: Month 1-12
            item_code: Item code (use get_cpi_metadata with level="Item" for valid values)
            limit: Max records
            Format: JSON or CSV
        """
        params = {
            "base_year": base_year,
            "year": year,
            "month_code": month_code,
            "item_code": item_code,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("CPI_Item", params)
