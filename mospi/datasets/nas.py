"""
NAS (National Accounts Statistics) Tools
"""

from typing import Optional, Dict, Any, Literal
from ..client import mospi


def register_nas_tools(mcp):
    """Register all NAS tools with the MCP server."""

    @mcp.tool()
    def get_nas_indicators() -> Dict[str, Any]:
        """
        Get list of all NAS indicators from MoSPI API.

        Returns indicators organized by series (Current/Back) and frequency (Annual/Quarterly).

        Returns:
            List of indicators with codes and descriptions
        """
        return mospi.get_nas_indicators()

    @mcp.tool()
    def get_nas_metadata(
        series: Literal["Current", "Back"] = "Current",
        frequency_code: Literal[1, 2] = 1,
        indicator_code: int = 1
    ) -> Dict[str, Any]:
        """
        Get NAS metadata directly from MoSPI API.

        Returns available filters and their valid values for the given series/frequency/indicator.

        Args:
            series: "Current" (default) or "Back"
            frequency_code: 1 (Annually, default) or 2 (Quarterly - Current series only)
            indicator_code: Indicator code (1-22 for Annual, 1-11 for Quarterly)

        Returns:
            Available filters including years, approaches, revisions, industries, etc.
        """
        return mospi.get_nas_filters(
            series=series,
            frequency_code=frequency_code,
            indicator_code=indicator_code
        )

    @mcp.tool()
    def get_nas_data(
        indicator_code: str,
        series: Literal["Current", "Back"] = "Current",
        frequency_code: Literal["Annually", "Quarterly"] = "Annually",
        year: Optional[str] = None,
        quarterly_code: Optional[str] = None,
        approach_code: Optional[str] = None,
        revision_code: Optional[str] = None,
        institutional_code: Optional[str] = None,
        industry_code: Optional[str] = None,
        subindustry_code: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get National Accounts Statistics (NAS) data from MoSPI.

        Note: Available filters vary by indicator. Use get_nas_metadata to see
        which filters are available for your specific indicator/series/frequency.

        Args:
            indicator_code: Required. Indicator code 1-22 (use get_nas_indicators for list)
            series: "Current" (default) or "Back"
            frequency_code: "Annually" (default) or "Quarterly"
            year: Year in YYYY-YY format (e.g., "2023-24")
            quarterly_code: Quarter 1-4 (use with frequency_code=Quarterly)
            approach_code: Use get_nas_metadata for valid values
            revision_code: Use get_nas_metadata for valid values
            institutional_code: Use get_nas_metadata for valid values
            industry_code: Use get_nas_metadata for valid values
            subindustry_code: Use get_nas_metadata for valid values
            limit: Max records
            page: Page number
            Format: JSON or CSV
        """
        # Strip leading zeros from codes (API expects 1 not 01), preserving
        # support for comma-separated multi-value inputs.
        def _normalize_code(value: str) -> str:
            tokens = []
            for token in value.split(","):
                token = token.strip()
                if token.isdigit():
                    tokens.append(token.lstrip("0") or "0")
                elif token:
                    tokens.append(token)
            return ",".join(tokens)

        indicator_code = _normalize_code(indicator_code)
        if industry_code:
            industry_code = _normalize_code(industry_code)

        params = {
            "series": series,
            "frequency_code": frequency_code,
            "year": year,
            "indicator_code": indicator_code,
            "quarterly_code": quarterly_code,
            "approach_code": approach_code,
            "revision_code": revision_code,
            "institutional_code": institutional_code,
            "industry_code": industry_code,
            "subindustry_code": subindustry_code,
            "limit": limit,
            "page": page,
            "Format": Format
        }

        return mospi.get_data("NAS", params)
