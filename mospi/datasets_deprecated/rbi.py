"""
RBI (Reserve Bank of India) Statistics Dataset Module

Provides access to MoSPI RBI API with 39 indicators covering:
- Foreign Trade (Direction, Exports, Imports by commodity/country)
- Balance of Payments (Quarterly, Annual, Key Components)
- External Debt (USD, Rupees, Quarterly)
- Forex Rates (Monthly, Annual, High/Low, 155 currencies)
- Foreign Exchange Reserves (Monthly, Annual)
- NRI Deposits
"""

from typing import Dict, Any, Optional, Literal
from ..client import mospi


def register_rbi_tools(mcp):
    """Register all RBI Statistics tools with the MCP server."""

    @mcp.tool()
    def get_rbi_indicators() -> Dict[str, Any]:
        """
        Get list of RBI indicators from MoSPI API.

        Returns 39 indicators organized by themes:
        - Foreign Trade (1, 2, 11-17, 20, 24, 42-46): Direction, exports, imports
        - Balance of Payments (4-10, 14, 22): BoP quarterly/annual, invisibles
        - External Debt (25-27): USD/Rupees, quarterly
        - Forex Rates (29, 31-37): Exchange rates, forward premia
        - Forex Reserves (47-48): Monthly/Annual reserves
        - RBI Operations (28, 30, 40): USD sale/purchase, forex turnover, NRI deposits

        Returns:
            List of 39 indicators with codes and descriptions
        """
        return mospi.get_rbi_indicators()

    @mcp.tool()
    def get_rbi_metadata(sub_indicator_code: int) -> Dict[str, Any]:
        """
        Get RBI metadata directly from MoSPI API.
        Returns available filters for the given indicator.

        IMPORTANT: Different indicators have very different filters.
        Always call this before get_rbi_data() to know which filters apply.

        Common filter patterns:
        - Foreign Trade (1, 11): year, country_group, trade_type, country
        - BoP indicators: year, quarter (for quarterly), indicator_type
        - Forex Rates (33, 36, 37): year, month, currency
        - Forex Reserves (47): year, month, reserve_type, reserve_currency

        Args:
            sub_indicator_code: Indicator code 1-48 (use get_rbi_indicators for list)

        Returns:
            Available filters specific to that indicator
        """
        return mospi.get_rbi_filters(sub_indicator_code=sub_indicator_code)

    @mcp.tool()
    def get_rbi_data(
        sub_indicator_code: str,
        year: Optional[str] = None,
        month_code: Optional[str] = None,
        quarter_code: Optional[str] = None,
        country_group_code: Optional[str] = None,
        country_code: Optional[str] = None,
        trade_type_code: Optional[str] = None,
        currency_code: Optional[str] = None,
        reserve_type_code: Optional[str] = None,
        reserve_currency_code: Optional[str] = None,
        indicator_code: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get RBI Statistics data from MoSPI.

        Covers foreign trade, balance of payments, forex rates, external debt,
        and foreign exchange reserves from RBI.

        IMPORTANT: Available filters vary significantly by indicator.
        Always call get_rbi_metadata() first to see which filters apply.

        Filter patterns by indicator type:
        - Foreign Trade (1, 2, 11, 20): year, country_group, trade_type, country
        - BoP Quarterly (4, 10): year, quarter
        - BoP Annual (5-8): year
        - Forex Rates Monthly (33, 36, 37): year, month, currency
        - Forex Reserves (47): year, month, reserve_type, reserve_currency
        - External Debt (25-27): year

        Args:
            sub_indicator_code: Required. Indicator code 1-48
            year: Year (format varies: "2023-24", "2023", etc.)
            month_code: Month code (for monthly indicators)
            quarter_code: Quarter code (for quarterly BoP)
            country_group_code: Country group (Africa, Asia, OECD, etc.)
            country_code: Specific country code
            trade_type_code: Export or Import
            currency_code: Currency code (for forex rates)
            reserve_type_code: Reserve type (for forex reserves)
            reserve_currency_code: Currency for reserves (USD, Rupees, SDR)
            indicator_code: Sub-indicator within BoP
            page: Page number
            limit: Max records per page
            Format: JSON or CSV
        """
        params = {
            "sub_indicator_code": sub_indicator_code,
            "year": year,
            "month_code": month_code,
            "quarter_code": quarter_code,
            "country_group_code": country_group_code,
            "country_code": country_code,
            "trade_type_code": trade_type_code,
            "currency_code": currency_code,
            "reserve_type_code": reserve_type_code,
            "reserve_currency_code": reserve_currency_code,
            "indicator_code": indicator_code,
            "page": page,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("RBI", params)
