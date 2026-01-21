import sys
from typing import Dict, Any, Optional
from fastmcp import FastMCP
from mospi.client import mospi


def log(msg: str):
    """Print to stderr to avoid interfering with stdio transport"""
    print(msg, file=sys.stderr)

# Initialize FastMCP server
mcp = FastMCP("MoSPI Data Server")


# =============================================================================
# Generic Tools
# =============================================================================

VALID_DATASETS = [
    "PLFS", "CPI", "IIP", "ASI", "NAS", "WPI", "ENERGY", "HCES",
    "NSS78", "NSS77", "TUS", "NFHS", "ASUSE", "GENDER", "RBI",
    "ENVSTATS", "AISHE", "CPIALRL"
]

@mcp.tool()
def get_indicators(dataset: str) -> Dict[str, Any]:
    """
    Step 1: Get available indicators for a dataset.

    Use know_about_mospi_api() first if unsure which dataset to use.

    Args:
        dataset: Dataset name - one of: PLFS, CPI, IIP, ASI, NAS, WPI, ENERGY, HCES,
                 NSS78, NSS77, TUS, NFHS, ASUSE, GENDER, RBI, ENVSTATS, AISHE, CPIALRL
    """
    dataset = dataset.upper()

    indicator_methods = {
        "PLFS": mospi.get_plfs_indicators,
        "NAS": mospi.get_nas_indicators,
        "NSS78": mospi.get_nss78_indicators,
        "NSS77": mospi.get_nss77_indicators,
        "HCES": mospi.get_hces_indicators,
        "ENERGY": mospi.get_energy_indicators,
        "TUS": mospi.get_tus_indicators,
        "NFHS": mospi.get_nfhs_indicators,
        "ASUSE": lambda: mospi.get_asuse_indicators(frequency_code=1),
        "GENDER": mospi.get_gender_indicators,
        "RBI": mospi.get_rbi_indicators,
        "ENVSTATS": mospi.get_envstats_indicators,
        "AISHE": mospi.get_aishe_indicators,
        "CPIALRL": mospi.get_cpialrl_indicators,
    }

    # Datasets without traditional indicator lists
    special_datasets = {
        "CPI": "CPI uses levels (Group/Item) instead of indicators. Call get_metadata with base_year and level params.",
        "IIP": "IIP uses categories instead of indicators. Call get_metadata with base_year and frequency params.",
        "WPI": "WPI uses hierarchical commodity codes. Call get_metadata to see available groups/items.",
        "ASI": "ASI uses classification years. Call get_metadata with classification_year param.",
    }

    if dataset in special_datasets:
        return {"message": special_datasets[dataset], "dataset": dataset}

    if dataset not in indicator_methods:
        return {"error": f"Unknown dataset: {dataset}", "valid_datasets": VALID_DATASETS}

    return indicator_methods[dataset]()


@mcp.tool()
def get_metadata(
    dataset: str,
    indicator_code: Optional[int] = None,
    base_year: Optional[str] = None,
    level: Optional[str] = None,
    frequency: Optional[str] = None,
    classification_year: Optional[str] = None,
    frequency_code: Optional[int] = None,
    series: Optional[str] = None,
    use_of_energy_balance_code: Optional[int] = None,
    sub_indicator_code: Optional[int] = None
) -> Dict[str, Any]:
    """
    Step 2: Get available filter options for a dataset/indicator.

    Returns all valid filter values (states, years, categories, etc.) to use in get_data().

    Args:
        dataset: Dataset name (PLFS, GENDER, ENVSTATS, etc.)
        indicator_code: Required for most datasets (PLFS, GENDER, ENVSTATS, TUS, NFHS, etc.)
        base_year: Required for CPI ("2012"/"2010") and IIP ("2011-12"/"2004-05"/"1993-94")
        level: Required for CPI ("Group"/"Item")
        frequency: Required for IIP ("Annually"/"Monthly")
        classification_year: Required for ASI ("2008"/"2004"/"1998"/"1987")
        frequency_code: Optional for PLFS, ASUSE, NAS (1=Annually, 2=Quarterly)
        series: Optional for NAS ("Current"/"Back")
        use_of_energy_balance_code: Optional for ENERGY (1=Supply, 2=Consumption)
        sub_indicator_code: Optional for NSS78
    """
    dataset = dataset.upper()

    try:
        if dataset == "CPI":
            return mospi.get_cpi_filters(base_year=base_year or "2012", level=level or "Group")

        elif dataset == "IIP":
            return mospi.get_iip_filters(base_year=base_year or "2011-12", frequency=frequency or "Annually")

        elif dataset == "ASI":
            return mospi.get_asi_filters(classification_year=classification_year or "2008")

        elif dataset == "WPI":
            return mospi.get_wpi_filters()

        elif dataset == "PLFS":
            if indicator_code is None:
                return {"error": "indicator_code is required for PLFS"}
            return mospi.get_plfs_filters(indicator_code=indicator_code, frequency_code=frequency_code or 1)

        elif dataset == "NAS":
            if indicator_code is None:
                return {"error": "indicator_code is required for NAS"}
            return mospi.get_nas_filters(series=series or "Current", frequency_code=frequency_code or 1, indicator_code=indicator_code)

        elif dataset == "NSS78":
            if indicator_code is None:
                return {"error": "indicator_code is required for NSS78"}
            return mospi.get_nss78_filters(indicator_code=indicator_code, sub_indicator_code=sub_indicator_code)

        elif dataset == "NSS77":
            if indicator_code is None:
                return {"error": "indicator_code is required for NSS77"}
            return mospi.get_nss77_filters(indicator_code=indicator_code)

        elif dataset == "HCES":
            return mospi.get_hces_filters(indicator_code=indicator_code or 1)

        elif dataset == "ENERGY":
            return mospi.get_energy_filters(indicator_code=indicator_code or 1, use_of_energy_balance_code=use_of_energy_balance_code or 1)

        elif dataset == "TUS":
            if indicator_code is None:
                return {"error": "indicator_code is required for TUS"}
            return mospi.get_tus_filters(indicator_code=indicator_code)

        elif dataset == "NFHS":
            if indicator_code is None:
                return {"error": "indicator_code is required for NFHS"}
            return mospi.get_nfhs_filters(indicator_code=indicator_code)

        elif dataset == "ASUSE":
            if indicator_code is None:
                return {"error": "indicator_code is required for ASUSE"}
            return mospi.get_asuse_filters(indicator_code=indicator_code, frequency_code=frequency_code or 1)

        elif dataset == "GENDER":
            if indicator_code is None:
                return {"error": "indicator_code is required for GENDER"}
            return mospi.get_gender_filters(indicator_code=indicator_code)

        elif dataset == "RBI":
            if indicator_code is None:
                return {"error": "indicator_code (sub_indicator_code) is required for RBI"}
            return mospi.get_rbi_filters(sub_indicator_code=indicator_code)

        elif dataset == "ENVSTATS":
            if indicator_code is None:
                return {"error": "indicator_code is required for ENVSTATS"}
            return mospi.get_envstats_filters(indicator_code=indicator_code)

        elif dataset == "AISHE":
            if indicator_code is None:
                return {"error": "indicator_code is required for AISHE"}
            return mospi.get_aishe_filters(indicator_code=indicator_code)

        elif dataset == "CPIALRL":
            if indicator_code is None:
                return {"error": "indicator_code is required for CPIALRL"}
            return mospi.get_cpialrl_filters(indicator_code=indicator_code)

        else:
            return {"error": f"Unknown dataset: {dataset}", "valid_datasets": VALID_DATASETS}

    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_data(dataset: str, filters: Dict[str, str]) -> Dict[str, Any]:
    """
    Step 3: Fetch data from a MoSPI dataset.

    Use filter keys and values discovered from get_metadata().

    Args:
        dataset: Dataset name (PLFS, GENDER, ENVSTATS, etc.)
        filters: Key-value filter pairs from get_metadata.
                 Example: {"indicator_code": "16", "sub_indicator_code": "1", "phylum_code": "1"}
    """
    dataset = dataset.upper()

    # Map friendly names to API dataset keys
    dataset_map = {
        "ENVSTATS": "ENVSTATS",
        "GENDER": "GENDER",
        "CPI_GROUP": "CPI_Group",
        "CPI_ITEM": "CPI_Item",
        "CPI": "CPI_Group",  # Default CPI to Group
        "IIP_ANNUAL": "IIP_Annual",
        "IIP_MONTHLY": "IIP_Monthly",
        "IIP": "IIP_Annual",  # Default IIP to Annual
        "PLFS": "PLFS",
        "ASI": "ASI",
        "NAS": "NAS",
        "WPI": "WPI",
        "ENERGY": "Energy",
        "HCES": "HCES",
        "NSS78": "NSS78",
        "NSS77": "NSS77",
        "TUS": "TUS",
        "NFHS": "NFHS",
        "ASUSE": "ASUSE",
        "RBI": "RBI",
        "AISHE": "AISHE",
        "CPIALRL": "CPIALRL",
    }

    api_dataset = dataset_map.get(dataset)
    if not api_dataset:
        return {"error": f"Unknown dataset: {dataset}", "valid_datasets": VALID_DATASETS}

    return mospi.get_data(api_dataset, filters)


# Comprehensive API documentation tool
@mcp.tool()
def know_about_mospi_api() -> Dict[str, Any]:
    """
    Step 0 (optional): Get overview of all 18 datasets to find the right one for your query.

    Use this if unsure which dataset contains the data you need. Skip if you already know the dataset.

    Workflow:
    0. know_about_mospi_api() - find which dataset to use (optional)
    1. get_indicators(dataset) - list available indicators
    2. get_metadata(dataset, indicator_code) - get filter options
    3. get_data(dataset, filters) - fetch data

    Returns:
        Dataset descriptions with use_for hints, and critical rules
    """
    return {
        "total_datasets": 18,
        "datasets": {
            "PLFS": {
                "name": "Periodic Labour Force Survey",
                "description": "Employment and unemployment statistics including LFPR, WPR, unemployment rate, wages, worker distribution by industry/sector",
                "use_for": "Jobs, unemployment, wages, workforce participation queries"
            },
            "CPI": {
                "name": "Consumer Price Index",
                "description": "Inflation data by commodity groups and 600+ individual items. CPI_Group supports state-level, CPI_Item is All-India only",
                "use_for": "Inflation, price indices, cost of living queries"
            },
            "IIP": {
                "name": "Index of Industrial Production",
                "description": "Industrial output indices - annual and monthly. Covers manufacturing, mining, electricity by use-based categories",
                "use_for": "Industrial growth, manufacturing output, sectoral production"
            },
            "ASI": {
                "name": "Annual Survey of Industries",
                "description": "Factory sector statistics - output, employment, wages, capital, productivity across 57 indicators by NIC codes",
                "use_for": "Factory performance, industrial employment, manufacturing deep-dive"
            },
            "NAS": {
                "name": "National Accounts Statistics",
                "description": "GDP and macroeconomic aggregates - production, expenditure, income approaches. Annual and quarterly frequency",
                "use_for": "GDP, economic growth, national income, sectoral contribution"
            },
            "WPI": {
                "name": "Wholesale Price Index",
                "description": "Wholesale price inflation with hierarchical commodity classification - major groups, groups, sub-groups, 600+ items",
                "use_for": "Wholesale inflation, producer prices, commodity price trends"
            },
            "Energy": {
                "name": "Energy Statistics",
                "description": "Energy balance in KToE/PetaJoules - supply and consumption by commodity (coal, oil, gas, renewables) and end-use sector",
                "use_for": "Energy production, consumption patterns, fuel mix, sectoral energy use"
            },
            "HCES": {
                "name": "Household Consumption Expenditure Survey",
                "description": "Monthly per capita expenditure (MPCE) across item categories, fractile classes, household types, social groups. Includes Gini coefficient",
                "use_for": "Consumer spending, poverty analysis, inequality, expenditure patterns"
            },
            "NSS78": {
                "name": "NSS 78th Round - Living Conditions",
                "description": "Household amenities, migration, sanitation, drinking water, mobile/internet usage, transport access, asset ownership",
                "use_for": "Living standards, migration, digital access, household amenities"
            },
            "NSS77": {
                "name": "NSS 77th Round - Land & Livestock",
                "description": "Agricultural holdings, farm income/expenses, crop production, livestock ownership, agricultural loans and insurance (33 indicators)",
                "use_for": "Agriculture, land holdings, farm economics, rural livelihoods"
            },
            "TUS": {
                "name": "Time Use Survey",
                "description": "How people spend time - paid work, unpaid domestic work, caregiving, leisure. 41 indicators by ICATUS activity classification",
                "use_for": "Unpaid work, gender time gap, work-life patterns, caregiving burden"
            },
            "NFHS": {
                "name": "National Family Health Survey",
                "description": "Health indicators - maternal/child health, nutrition, immunization, fertility, family planning, women's empowerment (21 indicators)",
                "use_for": "Health outcomes, maternal care, child nutrition, fertility rates"
            },
            "ASUSE": {
                "name": "Annual Survey of Unincorporated Enterprises",
                "description": "Informal sector statistics - employment, GVA, expenses across 50 activity categories for OAEs and establishments (35 indicators)",
                "use_for": "Informal economy, small enterprises, unorganized sector"
            },
            "Gender": {
                "name": "Gender Statistics",
                "description": "147 indicators covering sex ratio, fertility, mortality, health, education, labour, time use, financial inclusion, political participation, crimes against women",
                "use_for": "Gender gaps, women's welfare, sex-disaggregated analysis"
            },
            "RBI": {
                "name": "RBI Statistics",
                "description": "External sector data - foreign trade by country/commodity, balance of payments, forex rates (155 currencies), external debt, forex reserves (39 indicators)",
                "use_for": "Trade, forex rates, BoP, external debt, currency analysis"
            },
            "EnvStats": {
                "name": "Environment Statistics",
                "description": "124 indicators on air/water quality, forest cover, waste, biodiversity, climate, environmental expenditure",
                "use_for": "Pollution, forests, climate data, environmental indicators"
            },
            "AISHE": {
                "name": "All India Survey on Higher Education",
                "description": "Universities, colleges, student enrollment, GER, GPI, teacher counts by institution type, social group, gender (9 indicators)",
                "use_for": "Higher education access, enrollment, gender parity in education"
            },
            "CPIALRL": {
                "name": "CPI for Agricultural/Rural Labourers",
                "description": "Separate CPI series for agricultural labourers (AL) and rural labourers (RL) - general index and commodity group indices",
                "use_for": "Rural inflation, agricultural worker cost of living"
            }
        },
        "workflow": [
            "1. get_indicators(dataset) → list available indicators (ALWAYS do this first)",
            "2. get_metadata(dataset, indicator_code) → get ALL filter options (states, sub-indicators, phylum, etc.)",
            "3. get_data(dataset, filters) → fetch data with filters dict from step 2"
        ],
        "critical_rules": [
            "NEVER assume data doesn't exist - ALWAYS check indicators and metadata first",
            "NEVER say 'not available' without calling get_indicators() and get_metadata()",
            "Metadata reveals hidden dimensions (e.g., ENVSTATS indicator 16 has phylum filter with PROTOZOA, MAMMALIA, etc.)",
            "State codes DIFFER across datasets (e.g., Maharashtra=27 in PLFS, =15 in CPI) - always check metadata",
            "Different indicators have different filters - some have sub_indicator, phylum, crime_head, etc.",
            "Comma-separated values work for multiple codes (e.g., '1,2,3')",
            "Code 99 typically = 'All India' for geographic aggregates"
        ]
    }

if __name__ == "__main__":

    # Startup banner with creator info
    log("\n" + "="*75)
    log("🚀 MoSPI MCP Server - Starting...")
    log("="*75)
    log("📊 Serving Indian Government Statistical Data")
    log("🔧 Framework: FastMCP 2.0 (Production Ready)")
    log("📦 Datasets: 18 (PLFS, CPI, IIP, ASI, NAS, WPI, Energy, HCES, NSS78, TUS, NFHS, ASUSE, Gender, RBI, EnvStats, AISHE, CPIALRL, NSS77)")
    log("="*75)

    log("="*75)
    log("📡 Server will be available at http://localhost:8000/mcp")
    log("💡 Use 'fastmcp run mospi_server.py:mcp' for CLI control")
    log("="*75 + "\n")

    # Run with HTTP transport for remote access
    # For stdio (local MCP clients): mcp.run()
    # For HTTP (remote/web access): mcp.run(transport="http", port=8000)
    mcp.run(transport="http", port=8000)