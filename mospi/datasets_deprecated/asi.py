"""
ASI (Annual Survey of Industries) Tools
"""

from typing import Optional, Dict, Any, Literal
from ..client import mospi


def register_asi_tools(mcp):
    """Register all ASI tools with the MCP server."""

    @mcp.tool()
    def get_asi_classification_years() -> Dict[str, Any]:
        """
        Get list of available NIC classification years from MoSPI API.

        Returns:
            List of classification years (2008, 2004, 1998, 1987) with visualization options
        """
        return mospi.get_asi_classification_years()

    @mcp.tool()
    def get_asi_metadata(
        classification_year: Literal["2008", "2004", "1998", "1987"] = "2008"
    ) -> Dict[str, Any]:
        """
        Get ASI metadata directly from MoSPI API.

        Returns available filters and their valid values for the given classification year.

        Args:
            classification_year: "2008" (default), "2004", "1998", or "1987"

        Returns:
            Available filters including years, indicators, states, and NIC codes
        """
        return mospi.get_asi_filters(classification_year=classification_year)

    @mcp.tool()
    def get_asi_data(
        classification_year: Literal["2008", "2004", "1998", "1987"] = "2008",
        sector_code: Literal["Rural", "Urban", "Combined"] = "Combined",
        financial_year: Optional[str] = None,
        indicator_code: Optional[str] = None,
        state_code: Optional[str] = None,
        nic_code: Optional[str] = None,
        limit: Optional[int] = None,
        nic_code_type: Literal["All", "2-digit", "3-digit", "4-digit"] = "All",
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get Annual Survey of Industries (ASI) data from MoSPI.

        Args:
            classification_year: "2008" (default), "2004", "1998", or "1987"
            sector_code: "Rural", "Urban", or "Combined" (default)
            financial_year: Year in YYYY-YY format (e.g., "2023-24")
            indicator_code: Indicator code 1-56 (use get_asi_metadata for valid values)
            state_code: State code 1-38, 88 (D&NH & D&D), 99 (All India)
            nic_code: NIC code (use get_asi_metadata for valid values)
            limit: Max records
            nic_code_type: "All", "2-digit", "3-digit", or "4-digit"
            Format: JSON or CSV
        """
        params = {
            "classification_year": classification_year,
            "sector_code": sector_code,
            "year": financial_year,  # API uses 'year' not 'financial_year'
            "indicator_code": indicator_code,
            "state_code": state_code,
            "nic_code": nic_code,
            "limit": limit,
            "nic_type": nic_code_type,  # API uses 'nic_type' not 'nic_code_type'
            "Format": Format
        }

        return mospi.get_data("ASI", params)
