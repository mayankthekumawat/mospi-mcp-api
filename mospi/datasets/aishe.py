"""
AISHE (All India Survey on Higher Education) Dataset Module

Provides access to MoSPI AISHE API with 9 indicators covering:
- Number of Universities
- Number of Colleges
- Student Enrolment
- Social Group-wise Enrolment
- PWD & Minority Enrolment
- Gross Enrolment Ratio (GER)
- Gender Parity Index (GPI)
- Pupil Teacher Ratio
- Number of Teachers
"""

from typing import Dict, Any, Optional, Literal
from ..client import mospi


def register_aishe_tools(mcp):
    """Register all AISHE tools with the MCP server."""

    @mcp.tool()
    def get_aishe_indicators() -> Dict[str, Any]:
        """
        Get list of AISHE indicators from MoSPI API.

        Returns 9 indicators covering higher education statistics:
        1. Number of Universities
        2. Number of Colleges
        3. Student Enrolment
        4. Social Group-wise Enrolment
        5. PWD & Minority Enrolment
        6. Gross Enrolment Ratio (GER)
        7. Gender Parity Index (GPI)
        8. Pupil Teacher Ratio
        9. Number of Teachers

        Returns:
            List of indicators with codes and descriptions
        """
        return mospi.get_aishe_indicators()

    @mcp.tool()
    def get_aishe_metadata(indicator_code: int) -> Dict[str, Any]:
        """
        Get AISHE metadata directly from MoSPI API.
        Returns available filters for the given indicator.

        IMPORTANT: Different indicators have different filters.
        Always call this before get_aishe_data() to know which filters apply.

        Common filters include:
        - year: Academic year
        - state_code: State/UT code

        Args:
            indicator_code: Indicator code 1-9 (use get_aishe_indicators for list)

        Returns:
            Available filters specific to that indicator
        """
        return mospi.get_aishe_filters(indicator_code=indicator_code)

    @mcp.tool()
    def get_aishe_data(
        indicator_code: str,
        year: Optional[str] = None,
        state_code: Optional[str] = None,
        sub_indicator_code: Optional[str] = None,
        university_type_code: Optional[str] = None,
        college_type_code: Optional[str] = None,
        social_group_code: Optional[str] = None,
        gender_code: Optional[str] = None,
        level_code: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get AISHE (All India Survey on Higher Education) data from MoSPI.

        Covers higher education statistics including universities, colleges,
        student enrolment, GER, GPI, and teacher data.

        IMPORTANT: Available filters vary by indicator.
        Always call get_aishe_metadata() first to see which filters apply.

        Args:
            indicator_code: Required. Indicator code 1-9
            year: Academic year (e.g., "2020-21")
            state_code: State/UT code
            sub_indicator_code: Sub-indicator code
            university_type_code: Type of university
            college_type_code: Type of college
            social_group_code: Social group (SC/ST/OBC/General)
            gender_code: Gender filter
            level_code: Education level
            page: Page number
            limit: Max records per page
            Format: JSON or CSV
        """
        params = {
            "indicator_code": indicator_code,
            "year": year,
            "state_code": state_code,
            "sub_indicator_code": sub_indicator_code,
            "university_type_code": university_type_code,
            "college_type_code": college_type_code,
            "social_group_code": social_group_code,
            "gender_code": gender_code,
            "level_code": level_code,
            "page": page,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("AISHE", params)
