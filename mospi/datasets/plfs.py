"""
PLFS (Periodic Labour Force Survey) Tools
"""

from typing import Optional, Dict, Any, Literal
from ..client import mospi


def register_plfs_tools(mcp):
    """Register all PLFS tools with the MCP server."""

    @mcp.tool()
    def get_plfs_data(
        indicator_code: int = 3,
        frequency_code: int = 1,
        year: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON",
        state_code: Optional[str] = None,
        sector_code: Optional[str] = None,
        gender_code: Optional[str] = None,
        age_code: Optional[str] = None,
        weekly_status_code: Optional[str] = None,
        religion_code: Optional[str] = None,
        social_category_code: Optional[str] = None,
        education_code: Optional[str] = None,
        broad_industry_work_code: Optional[str] = None,
        broad_status_employment_code: Optional[str] = None,
        employee_contract_code: Optional[str] = None,
        enterprise_size_code: Optional[str] = None,
        enterprise_type_code: Optional[str] = None,
        industry_section_code: Optional[str] = None,
        nco_division_code: Optional[str] = None,
        nic_group_code: Optional[str] = None,
        quarter_code: Optional[str] = None,
        month_code: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get PLFS (Periodic Labour Force Survey) data.

        Args:
            indicator_code: 1=LFPR, 2=WPR, 3=UR (default), 4=Distribution, 5-8=Wages
            frequency_code: 1=Annual (default), 2=Quarterly, 3=Monthly
            year: Format YYYY-YY for Annual/Quarterly, YYYY for Monthly
            page: Page number
            limit: Max records
            Format: JSON or CSV

            Filters (use get_plfs_metadata for valid values):
            state_code, sector_code, gender_code, age_code, weekly_status_code,
            religion_code, social_category_code, education_code, broad_industry_work_code,
            broad_status_employment_code, employee_contract_code, enterprise_size_code,
            enterprise_type_code, industry_section_code, nco_division_code, nic_group_code,
            quarter_code, month_code
        """
        params = {
            "indicator_code": indicator_code,
            "frequency_code": frequency_code,
            "year": year,
            "page": page,
            "limit": limit,
            "Format": Format,
            "state_code": state_code,
            "sector_code": sector_code,
            "gender_code": gender_code,
            "age_code": age_code,
            "weekly_status_code": weekly_status_code,
            "religion_code": religion_code,
            "social_category_code": social_category_code,
            "education_code": education_code,
            "broad_industry_work_code": broad_industry_work_code,
            "broad_status_employment_code": broad_status_employment_code,
            "employee_contract_code": employee_contract_code,
            "enterprise_size_code": enterprise_size_code,
            "enterprise_type_code": enterprise_type_code,
            "industry_section_code": industry_section_code,
            "nco_division_code": nco_division_code,
            "nic_group_code": nic_group_code,
            "quarter_code": quarter_code,
            "month_code": month_code,
        }

        return mospi.get_data("PLFS", params)

    @mcp.tool()
    def get_plfs_metadata(
        indicator_code: int = 3,
        frequency_code: int = 1,
        year: Optional[str] = None,
        month_code: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get PLFS metadata directly from MoSPI API.

        Returns available filters and their valid values for the given parameters.

        Args:
            indicator_code: Indicator (1-8), default 3 (Unemployment Rate)
            frequency_code: 1=Annual (default), 2=Quarterly, 3=Monthly
            year: Year to get metadata for (e.g., "2022-23" or "2025")
            month_code: Month code for monthly data (1-12)

        Returns:
            Available filters and their valid options from the API
        """
        return mospi.get_plfs_filters(
            indicator_code=indicator_code,
            frequency_code=frequency_code,
            year=year,
            month_code=month_code
        )

    @mcp.tool()
    def get_plfs_indicators() -> Dict[str, Any]:
        """
        Get list of all PLFS indicators from MoSPI API.

        Returns:
            List of indicators with codes and descriptions
        """
        return mospi.get_plfs_indicators()
