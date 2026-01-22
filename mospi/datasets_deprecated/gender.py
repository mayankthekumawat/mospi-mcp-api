"""
Gender Statistics Dataset Module

Provides access to MoSPI Gender Statistics API with 157 indicators covering:
- Population & Demographics (sex ratio, fertility, mortality)
- Health (maternal health, HIV, diseases, BMI)
- Education (literacy, enrollment, dropout rates, GPI)
- Labour (LFPR, WPR, wages, unemployment)
- Time Use (unpaid work, domestic activities)
- Financial Inclusion (banking, insurance schemes, SHGs)
- Political Participation (elections, representation)
- Crime Against Women (rape, domestic violence, cyber crimes)
- Disability Statistics
"""

from typing import Dict, Any, Optional, Literal
from ..client import mospi


def register_gender_tools(mcp):
    """Register all Gender Statistics tools with the MCP server."""

    @mcp.tool()
    def get_gender_indicators() -> Dict[str, Any]:
        """
        Get list of Gender Statistics indicators from MoSPI API.

        Returns 157 indicators organized by themes:
        - Population & Demographics (1-7): Sex ratio, population trends
        - Fertility & Mortality (8-21): TFR, IMR, MMR, life expectancy
        - Health (22-53): Maternal care, HIV, diseases, BMI
        - Education (55-79): Literacy, enrollment, dropout, teachers
        - Labour (80-95): LFPR, WPR, wages, unemployment
        - Time Use (96-104): Unpaid work, activity participation
        - Financial Inclusion (105-122): Banking, schemes, SHGs
        - Political Participation (123-137): Elections, representation
        - Crime Against Women (140-157): Rape, domestic violence, cyber crimes

        Returns:
            List of 157 indicators with codes and descriptions
        """
        return mospi.get_gender_indicators()

    @mcp.tool()
    def get_gender_metadata(indicator_code: int) -> Dict[str, Any]:
        """
        Get Gender metadata directly from MoSPI API.
        Returns available filters for the given indicator.

        IMPORTANT: Different indicators have different filters. Always call this
        before get_gender_data() to know which filters are available.

        Common filter patterns:
        - Demographics (1-7): year, sector, gender
        - State-wise indicators (6, 7, 16, 19, 57, 108, 121): year, state
        - Labour (80-95): year, sector, gender, age_group
        - Crime (140-157): year, sub_indicator, crime_head

        Args:
            indicator_code: Indicator code 1-157 (use get_gender_indicators for list)

        Returns:
            Available filters: year, sector, gender, state, age_group, sub_indicator, crime_head, etc.
        """
        return mospi.get_gender_filters(indicator_code=indicator_code)

    @mcp.tool()
    def get_gender_data(
        indicator_code: str,
        year: Optional[str] = None,
        sector_code: Optional[str] = None,
        gender_code: Optional[str] = None,
        state_ut_code: Optional[str] = None,
        age_group_code: Optional[str] = None,
        sub_indicator_code: Optional[str] = None,
        crime_head_code: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get Gender Statistics data from MoSPI.

        Comprehensive gender-disaggregated data covering demographics, health,
        education, employment, time use, financial inclusion, political
        participation, and crimes against women.

        IMPORTANT: Available filters vary significantly by indicator.
        Always call get_gender_metadata() first to see which filters apply.

        Filter patterns by indicator type:
        - Population (1-7): year, sector, gender
        - State-wise (6,7,16,19,57): year, state_ut
        - Fertility/Mortality (8-21): year, sector, gender
        - Labour Force (80-95): year, sector, gender, age_group
        - Crime (140-157): year, sub_indicator, crime_head

        Args:
            indicator_code: Required. Indicator code 1-157
            year: Year (format varies: "2023", "2022-23", "2011", etc.)
            sector_code: 1=Rural, 2=Urban, 3=Total
            gender_code: 1=Male, 2=Female, 7=Person
            state_ut_code: State/UT code (for state-wise indicators)
            age_group_code: Age group code (for labour indicators)
            sub_indicator_code: Sub-indicator (for crime indicators)
            crime_head_code: Type of crime (for crime indicators)
            page: Page number
            limit: Max records per page
            Format: JSON or CSV
        """
        params = {
            "indicator_code": indicator_code,
            "year": year,
            "sector_code": sector_code,
            "gender_code": gender_code,
            "state_ut_code": state_ut_code,
            "age_group_code": age_group_code,
            "sub_indicator_code": sub_indicator_code,
            "crime_head_code": crime_head_code,
            "page": page,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("GENDER", params)
