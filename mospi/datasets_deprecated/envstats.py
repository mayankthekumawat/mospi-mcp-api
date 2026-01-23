"""
Environment Statistics Dataset Module

Provides access to MoSPI Environment Statistics API with 124 indicators covering:
- Climate (temperature, rainfall, seasons)
- Water Resources (wetlands, watersheds, rivers, reservoirs)
- Land (soil, degradation, land use)
- Forests & Biodiversity (forest cover, carbon stock, species)
- Pollution (air quality, water quality, noise)
- Resources (minerals, coal, power)
- Agriculture (crops, fertilizers, pesticides, organic farming)
- Livestock & Fisheries
- Waste Management (municipal, hazardous, biomedical)
- Natural Disasters (floods, cyclones, earthquakes)
- Health & Sanitation
- Environmental Expenditure
"""

from typing import Dict, Any, Optional, Literal
from ..client import mospi


def register_envstats_tools(mcp):
    """Register all Environment Statistics tools with the MCP server."""

    @mcp.tool()
    def get_envstats_indicators() -> Dict[str, Any]:
        """
        Get list of Environment Statistics indicators from MoSPI API.

        Returns 124 indicators organized by themes:
        - Climate (1-3): Temperature, rainfall
        - Water (4-8, 66-74): Wetlands, watersheds, rivers, reservoirs
        - Land (9-12, 43): Soil, degradation, land use
        - Forests (18-24): Forest cover, carbon stock, tree cover
        - Biodiversity (14, 16-17): Protected areas, species
        - Pollution (25-31): Air quality, water quality, noise
        - Resources (32-42): Minerals, coal, power
        - Agriculture (44-60): Crops, fertilizers, pesticides
        - Livestock & Fish (61-65): Animals, meat, fish
        - Environment (75-86): GHG, waste management
        - Disasters (87-95): Floods, cyclones, earthquakes
        - Health (96-122): Sanitation, diseases
        - Expenditure (123-130): Environmental spending

        Returns:
            List of 124 indicators with codes and descriptions
        """
        return mospi.get_envstats_indicators()

    @mcp.tool()
    def get_envstats_metadata(indicator_code: int) -> Dict[str, Any]:
        """
        Get Environment Statistics metadata directly from MoSPI API.
        Returns available filters for the given indicator.

        IMPORTANT: Different indicators have very different filters.
        Always call this before get_envstats_data() to know which filters apply.

        Common filter patterns:
        - Climate indicators: year, season, state
        - Biodiversity (16): sub_indicator, phylum
        - Forest indicators: year, state, forest_type
        - Pollution indicators: year, city, parameter
        - Disaster indicators: year, state, disaster_type

        Args:
            indicator_code: Indicator code 1-130 (use get_envstats_indicators for list)

        Returns:
            Available filters specific to that indicator
        """
        return mospi.get_envstats_filters(indicator_code=indicator_code)

    @mcp.tool()
    def get_envstats_data(
        indicator_code: str,
        year: Optional[str] = None,
        state_code: Optional[str] = None,
        sub_indicator_code: Optional[str] = None,
        season_code: Optional[str] = None,
        month_code: Optional[str] = None,
        city_code: Optional[str] = None,
        parameter_code: Optional[str] = None,
        forest_type_code: Optional[str] = None,
        phylum_code: Optional[str] = None,
        disaster_type_code: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        Format: Optional[Literal["JSON", "CSV"]] = "JSON"
    ) -> Dict[str, Any]:
        """
        Get Environment Statistics data from MoSPI.

        Covers climate, biodiversity, pollution, resources, disasters,
        and environmental health indicators.

        IMPORTANT: Available filters vary significantly by indicator.
        Always call get_envstats_metadata() first to see which filters apply.

        Args:
            indicator_code: Required. Indicator code 1-130
            year: Year (format varies by indicator)
            state_code: State code (for state-wise indicators)
            sub_indicator_code: Sub-indicator code
            season_code: Season (for climate indicators)
            month_code: Month (for monthly data)
            city_code: City code (for pollution indicators)
            parameter_code: Parameter code (for quality indicators)
            forest_type_code: Forest type (for forest indicators)
            phylum_code: Phylum (for biodiversity indicators)
            disaster_type_code: Disaster type (for disaster indicators)
            page: Page number
            limit: Max records per page
            Format: JSON or CSV
        """
        params = {
            "indicator_code": indicator_code,
            "year": year,
            "state_code": state_code,
            "sub_indicator_code": sub_indicator_code,
            "season_code": season_code,
            "month_code": month_code,
            "city_code": city_code,
            "parameter_code": parameter_code,
            "forest_type_code": forest_type_code,
            "phylum_code": phylum_code,
            "disaster_type_code": disaster_type_code,
            "page": page,
            "limit": limit,
            "Format": Format
        }

        return mospi.get_data("ENVSTATS", params)
