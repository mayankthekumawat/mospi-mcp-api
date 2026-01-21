"""
IIP (Index of Industrial Production) Tools
"""

from typing import Optional, Dict, Any, Literal
from ..client import mospi


def register_iip_tools(mcp):
    """Register all IIP tools with the MCP server."""

    @mcp.tool()
    def get_iip_metadata(
        base_year: Literal["2011-12", "2004-05", "1993-94"] = "2011-12",
        frequency: Literal["Annually", "Monthly"] = "Annually"
    ) -> Dict[str, Any]:
        """
        Get IIP metadata directly from MoSPI API.

        Returns available filters and their valid values for the given base year and frequency.

        Args:
            base_year: "2011-12" (default), "2004-05", or "1993-94"
            frequency: "Annually" (default) returns financial_year, type, category, subcategory
                       "Monthly" returns year, month, type, category, subcategory

        Returns:
            Available filters and their valid options from the API
        """
        return mospi.get_iip_filters(base_year=base_year, frequency=frequency)

    @mcp.tool()
    def get_iip_annual(
        base_year: Literal["2011-12", "2004-05", "1993-94"] = "2011-12",
        financial_year: Optional[str] = None,
        category_code: Optional[str] = None,
        subcategory_code: Optional[str] = None,
        limit: Optional[int] = None,
        type: Literal["All", "Use-based category", "Sectoral", "General"] = "All",
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get IIP (Index of Industrial Production) annual data.

        Args:
            base_year: "2011-12" (default), "2004-05", or "1993-94"
            financial_year: Year in YYYY-YY format (e.g., "2023-24")
            category_code: Category code (use get_iip_metadata for valid values)
            subcategory_code: Subcategory code (use get_iip_metadata for valid values)
            limit: Max records
            type: "All", "Use-based category", "Sectoral", or "General"
            Format: JSON or CSV
        """
        params = {
            "base_year": base_year,
            "financial_year": financial_year,
            "category_code": category_code,
            "subcategory_code": subcategory_code,
            "limit": limit,
            "type": type,
            "Format": Format
        }

        return mospi.get_data("IIP_Annual", params)

    @mcp.tool()
    def get_iip_monthly(
        base_year: Literal["2011-12", "2004-05", "1993-94"] = "2011-12",
        year: Optional[str] = None,
        month_code: Optional[str] = None,
        category_code: Optional[str] = None,
        subcategory_code: Optional[str] = None,
        limit: Optional[int] = None,
        type: Literal["All", "Use-based category", "Sectoral", "General"] = "All",
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get IIP (Index of Industrial Production) monthly data.

        Args:
            base_year: "2011-12" (default), "2004-05", or "1993-94"
            year: Year in YYYY format (e.g., "2023")
            month_code: Month 1-12
            category_code: Category code (use get_iip_metadata for valid values)
            subcategory_code: Subcategory code (use get_iip_metadata for valid values)
            limit: Max records
            type: "All", "Use-based category", "Sectoral", or "General"
            Format: JSON or CSV
        """
        params = {
            "base_year": base_year,
            "year": year,
            "month_code": month_code,
            "category_code": category_code,
            "subcategory_code": subcategory_code,
            "limit": limit,
            "type": type,
            "Format": Format
        }

        return mospi.get_data("IIP_Monthly", params)
