"""
Energy Statistics Tools
"""

from typing import Optional, Dict, Any, Literal
from ..client import mospi


def register_energy_tools(mcp):
    """Register all Energy tools with the MCP server."""

    @mcp.tool()
    def get_energy_indicators() -> Dict[str, Any]:
        """
        Get list of Energy indicators from MoSPI API.

        Returns:
            Indicators (KToE, PetaJoules) and use_of_energy_balance options (Supply, Consumption)
        """
        return mospi.get_energy_indicators()

    @mcp.tool()
    def get_energy_metadata(
        indicator_code: Literal[1, 2] = 1,
        use_of_energy_balance_code: Literal[1, 2] = 1
    ) -> Dict[str, Any]:
        """
        Get Energy metadata directly from MoSPI API.

        Returns available filters for the given indicator and balance type.

        Args:
            indicator_code: 1 (KToE, default) or 2 (PetaJoules)
            use_of_energy_balance_code: 1 (Supply, default) or 2 (Consumption)

        Returns:
            Available filters: year, energy_commodities, end_use_sector
        """
        return mospi.get_energy_filters(
            indicator_code=indicator_code,
            use_of_energy_balance_code=use_of_energy_balance_code
        )

    @mcp.tool()
    def get_energy_data(
        indicator_code: Literal["1", "2"] = "1",
        use_of_energy_balance_code: Literal["1", "2"] = "1",
        year: Optional[str] = None,
        energy_commodities_code: Optional[str] = None,
        energy_sub_commodities_code: Optional[str] = None,
        end_use_sector_code: Optional[str] = None,
        end_use_sub_sector_code: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get Energy Statistics data from MoSPI.

        Note: Use get_energy_metadata() to see available filter values.

        Args:
            indicator_code: "1" (KToE, default) or "2" (PetaJoules)
            use_of_energy_balance_code: "1" (Supply, default) or "2" (Consumption)
            year: Year in YYYY-YY or YYYY format (e.g., "2023-24")
            energy_commodities_code: Energy commodity code (use get_energy_metadata)
            energy_sub_commodities_code: Energy sub-commodity code
            end_use_sector_code: End use sector code (use get_energy_metadata)
            end_use_sub_sector_code: End use sub-sector code
            limit: Max records
            page: Page number
            Format: JSON or CSV
        """
        params = {
            "indicator_code": indicator_code,
            "use_of_energy_balance_code": use_of_energy_balance_code,
            "year": year,
            "energy_commodities_code": energy_commodities_code,
            "energy_sub_commodities_code": energy_sub_commodities_code,
            "end_use_sector_code": end_use_sector_code,
            "end_use_sub_sector_code": end_use_sub_sector_code,
            "limit": limit,
            "page": page,
            "Format": Format
        }

        return mospi.get_data("Energy", params)
