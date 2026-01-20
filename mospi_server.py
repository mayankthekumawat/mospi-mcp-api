import os
import sys
from typing import Dict, Any
from fastmcp import FastMCP
# Register dataset tools from modules
from mospi.datasets import register_plfs_tools, register_cpi_tools, register_iip_tools, register_asi_tools, register_nas_tools, register_wpi_tools, register_energy_tools, register_hces_tools, register_nss78_tools, register_tus_tools, register_nfhs_tools, register_asuse_tools, register_gender_tools, register_rbi_tools, register_envstats_tools, register_aishe_tools, register_cpialrl_tools, register_nss77_tools


def log(msg: str):
    """Print to stderr to avoid interfering with stdio transport"""
    print(msg, file=sys.stderr)

# No Auth Setup
auth_provider = None

# Initialize FastMCP server with optional authentication
mcp = FastMCP("MoSPI Data Server", auth=auth_provider)


register_plfs_tools(mcp)
register_cpi_tools(mcp)
register_iip_tools(mcp)
register_asi_tools(mcp)
register_nas_tools(mcp)
register_wpi_tools(mcp)
register_energy_tools(mcp)
register_hces_tools(mcp)
register_nss78_tools(mcp)
register_tus_tools(mcp)
register_nfhs_tools(mcp)
register_asuse_tools(mcp)
register_gender_tools(mcp)
register_rbi_tools(mcp)
register_envstats_tools(mcp)
register_aishe_tools(mcp)
register_cpialrl_tools(mcp)
register_nss77_tools(mcp)

# Comprehensive API documentation tool
@mcp.tool()
def know_about_mospi_api() -> Dict[str, Any]:
    """
    ALWAYS USE THIS FIRST FOR EVERY QUERY RELATED TO MOSPI

    Get complete MoSPI API documentation, parameter details, and usage guidelines.
    
    CRITICAL: ALWAYS CALL THIS FIRST FOR EVERY QUERY RELATED TO MOSPI. Call this tool FIRST to understand the API structure before making any data requests.
    This provides all parameter categories, code ranges, and optimization strategies.
    
    Returns:
        Complete API documentation with parameter details for all 9 datasets
    """
    api_docs = {
        "overview": {
            "total_datasets": 18,
            "base_url": "https://api.mospi.gov.in",
            "output_formats": ["JSON", "CSV"],
            "available_datasets": ["PLFS", "CPI", "IIP", "ASI", "NAS", "WPI", "Energy", "HCES", "NSS78", "TUS", "NFHS", "ASUSE", "Gender", "RBI", "EnvStats", "AISHE", "CPIALRL", "NSS77"]
        },
        "optimization_strategy": {
            "CRITICAL_RULE": "Use get_X_indicators() and get_X_metadata() to discover available codes before making data calls",
            "steps": [
                "1. Understand what data you need (state, time period, indicators)",
                "2. Call get_X_indicators() to see available indicators for your dataset",
                "3. Call get_X_metadata() with indicator_code to get available filter codes",
                "4. Use the returned codes to construct your data API call"
            ],
            "efficiency_tips": [
                "State codes differ across datasets - always use get_X_metadata() to get correct codes",
                "Use comma-separated values for multiple codes in same parameter",
                "Most numeric ranges start from 1, some from 01",
                "Code 99 typically means 'All India' for geographic data"
            ]
        },
        "datasets": {
            "PLFS": {
                "name": "Periodic Labour Force Survey",
                "description": "Employment and unemployment statistics",
                "endpoint": "/api/plfs/getData",
                "categories_available": ["State", "Gender", "Age", "Sector", "Weekly_status", "Religion", "Social_category", "Education", "Broad_industry_work", "Broad_status_employment", "Employee_contract", "Enterprise_size", "Enterprise_type", "Industry_section", "NCO_division", "NIC_group", "Quarter"],
                "parameters": {
                    "indicator_code": {
                        "required": True,
                        "type": "enum",
                        "options": [
                            "LFPR (Labour Force Participation Rate, in per cent)",
                            "WPR (Worker Population Ratio, in per cent)",
                            "UR (Unemployment Rate, in per cent)",
                            "Percentage distribution of workers",
                            "Percentage of regular wage/ salaried employees with employment condition as",
                            "Average wage/salary earnings (Rs. 0.00) during the preceding calendar month from regular wage/salaried employment",
                            "Average wage earnings (Rs. 0.00) per day from casual labour work other than public works",
                            "Average gross earnings (Rs. 0.00) during last 30 days from self-employment"
                        ],
                        "default": "UR (Unemployment Rate, in per cent)"
                    },
                    "year": {"required": False, "format": "YYYY-YY", "example": "2023-24", "multi_value": True},
                    "state_code": {"required": False, "range": "1-38", "multi_value": True, "note": "Use get_plfs_metadata() to get state codes"},
                    "sector_code": {"required": False, "range": "1-3", "multi_value": True, "codes": {"1": "Rural", "2": "Urban", "3": "Combined"}},
                    "gender_code": {"required": False, "range": "1-3", "multi_value": True, "codes": {"1": "Male", "2": "Female", "3": "Person"}},
                    "age_code": {"required": False, "range": "1-4", "multi_value": True},
                    "weekly_status_code": {"required": False, "range": "1-2", "multi_value": True},
                    "religion_code": {"required": False, "range": "1-5", "multi_value": True},
                    "social_category_code": {"required": False, "range": "1-5", "multi_value": True},
                    "education_code": {"required": False, "range": "1-10", "multi_value": True},
                    "broad_industry_work_code": {"required": False, "range": "1-4", "multi_value": True},
                    "broad_status_employment_code": {"required": False, "range": "1-6", "multi_value": True},
                    "employee_contract_code": {"required": False, "range": "1-5", "multi_value": True},
                    "enterprise_size_code": {"required": False, "range": "1-6", "multi_value": True},
                    "enterprise_type_code": {"required": False, "range": "1-9", "multi_value": True},
                    "industry_section_code": {"required": False, "range": "1-22", "multi_value": True},
                    "nco_division_code": {"required": False, "range": "1-11", "multi_value": True},
                    "nic_group_code": {"required": False, "range": "1-14", "multi_value": True},
                    "quarter_code": {"required": False, "range": "1-29", "multi_value": True},
                    "page": {"required": False, "range": "1-n", "note": "Page number for pagination"},
                    "limit": {"required": False, "type": "int", "note": "UNDOCUMENTED: Maximum number of records to fetch (e.g., 50)"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "CPI_Group": {
                "name": "Consumer Price Index by Group",
                "description": "Inflation data by commodity groups. Use this for state-specific CPI queries (supports state_code parameter unlike CPI_Item)",
                "endpoint": "/api/cpi/getCPIIndex",
                "categories_available": ["State_code", "Group_code", "Subgroup_code"],
                "parameters": {
                    "base_year": {"required": True, "options": ["2012", "2010"], "default": "2012"},
                    "series": {"required": True, "options": ["Current", "Back"], "default": "Current"},
                    "year": {"required": False, "format": "YYYY", "example": "2023", "multi_value": True},
                    "month_code": {"required": False, "range": "1-12", "multi_value": True},
                    "state_code": {"required": False, "range": "1-36 & 99", "multi_value": True, "note": "Use get_cpi_metadata() - codes differ from PLFS!"},
                    "group_code": {"required": False, "multi_value": True, "note": "Use get_cpi_metadata() to get group codes"},
                    "subgroup_code": {"required": False, "multi_value": True, "note": "Use get_cpi_metadata() to get subgroup codes"},
                    "sector_code": {"required": False, "range": "1-3", "multi_value": True, "codes": {"1": "Rural", "2": "Urban", "3": "Combined"}},
                    "page": {"required": False, "range": "1-n"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "CPI_Item": {
                "name": "Consumer Price Index by Item",
                "description": "Inflation data for specific items (600+ available)",
                "endpoint": "/api/cpi/getItemIndex",
                "categories_available": ["Item"],
                "CRITICAL_LIMITATION": "⚠️ NO STATE-LEVEL DATA AVAILABLE - This endpoint does NOT support state_code parameter. For state-specific CPI data, you MUST use CPI_Group instead!",
                "parameters": {
                    "base_year": {"required": True, "options": ["2012", "2010"], "default": "2012"},
                    "year": {"required": False, "format": "YYYY", "example": "2023", "multi_value": True},
                    "month_code": {"required": False, "range": "1-12", "multi_value": True},
                    "item_code": {"required": False, "note": "Use get_cpi_metadata() - 600+ items available"},
                    "page": {"required": False, "range": "1-n"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                },
                "use_cases": {
                    "CORRECT": "All-India item-level CPI (e.g., 'CPI for Rice', 'CPI for Petrol')",
                    "INCORRECT": "State-specific item CPI (e.g., 'CPI for Rice in Maharashtra') - Use CPI_Group instead!"
                }
            },
            "ASI": {
                "name": "Annual Survey of Industries",
                "description": "Industrial statistics and performance",
                "endpoint": "/api/asi/getASIData",
                "categories_available": ["State_code", "Indicator", "NIC"],
                "parameters": {
                    "classification_year": {"required": True, "options": ["2008", "2004", "1998", "1987"], "default": "2008"},
                    "sector_code": {"required": True, "options": ["Rural", "Urban", "Combined"], "default": "Combined"},
                    "financial_year": {"required": False, "format": "YYYY-YY", "example": "2023-24", "multi_value": True},
                    "indicator_code": {"required": False, "range": "1-56", "multi_value": True, "note": "Use get_asi_metadata() - 57 indicators total"},
                    "state_code": {"required": False, "range": "1-38, 88, 99", "multi_value": True, "note": "88=Dadra & N Haveli & Daman & Diu, 99=All India"},
                    "nic_code": {"required": False, "multi_value": True, "note": "Use get_asi_metadata() for NIC codes"},
                    "page": {"required": False, "range": "1-n"},
                    "nic_code_type": {"required": True, "options": ["All", "2-digit", "3-digit", "4-digit"], "default": "All"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "IIP_Annual": {
                "name": "Index of Industrial Production (Annual)",
                "description": "Yearly industrial production indices",
                "endpoint": "/api/iip/getIIPAnnual",
                "categories_available": ["Category", "Subcategory"],
                "parameters": {
                    "base_year": {"required": True, "options": ["2011-12", "2004-05", "1993-94"], "default": "2011-12"},
                    "financial_year": {"required": False, "format": "YYYY-YY", "example": "2023-24", "multi_value": True},
                    "category_code": {"required": False, "range": "01-11", "multi_value": True, "note": "Use get_iip_metadata() for category codes"},
                    "subcategory_code": {"required": False, "note": "Use get_iip_metadata() for subcategory codes"},
                    "page": {"required": False, "range": "1-n"},
                    "type": {"required": True, "options": ["All", "Use-based category", "Sectoral", "General"], "default": "All"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "IIP_Monthly": {
                "name": "Index of Industrial Production (Monthly)",
                "description": "Monthly industrial production indices",
                "endpoint": "/api/iip/getIIPMonthly",
                "categories_available": ["Category", "Subcategory"],
                "parameters": {
                    "base_year": {"required": True, "options": ["2011-12", "2004-05", "1993-94"], "default": "2011-12"},
                    "year": {"required": False, "format": "YYYY", "example": "2023", "multi_value": True},
                    "month_code": {"required": False, "range": "1-12", "multi_value": True},
                    "category_code": {"required": False, "range": "01-11", "multi_value": True, "note": "Use get_iip_metadata() for category codes"},
                    "subcategory_code": {"required": False, "note": "Use get_iip_metadata() for subcategory codes"},
                    "page": {"required": False, "range": "1-n"},
                    "type": {"required": True, "options": ["All", "Use-based category", "Sectoral", "General"], "default": "All"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "NAS": {
                "name": "National Accounts Statistics",
                "description": "GDP and economic indicators",
                "endpoint": "/api/nas/getNASData",
                "categories_available": ["Indicator", "Approach", "Revision", "Account", "Institutional", "Industry", "Subindustry"],
                "parameters": {
                    "series": {"required": True, "options": ["Current", "Back"], "default": "Current"},
                    "frequency_code": {"required": True, "options": ["Annually", "Quarterly"], "default": "Annually"},
                    "year": {"required": False, "format": "YYYY-YY", "example": "2023-24", "multi_value": True},
                    "indicator_code": {"required": True, "range": "1-22", "multi_value": True, "note": "Use get_nas_indicators() for indicator list"},
                    "approach_code": {"required": False, "range": "01-03", "multi_value": True, "codes": {"01": "Production", "02": "Expenditure", "03": "Income"}},
                    "revision_code": {"required": False, "range": "01-07", "multi_value": True},
                    "account_code": {"required": False, "range": "01-02", "multi_value": True},
                    "institutional_code": {"required": False, "range": "01-11", "multi_value": True},
                    "industry_code": {"required": False, "range": "01-17", "multi_value": True},
                    "subindustry_code": {"required": False, "range": "01-18", "multi_value": True},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "WPI": {
                "name": "Wholesale Price Index",
                "description": "Wholesale price inflation data",
                "endpoint": "/api/wpi/getWpiRecords",
                "categories_available": ["major_group_code", "group_code", "sub_group_code", "sub_sub_group_code", "item_code"],
                "parameters": {
                    "year": {"required": False, "format": "YYYY", "example": "2023", "multi_value": True},
                    "month_code": {"required": False, "range": "1-12", "multi_value": True},
                    "major_group_code": {"required": False, "multi_value": True, "note": "Use get_wpi_metadata() for codes"},
                    "group_code": {"required": False, "multi_value": True, "note": "Use get_wpi_metadata() for codes"},
                    "sub_group_code": {"required": False, "multi_value": True, "note": "Use get_wpi_metadata() for codes"},
                    "sub_sub_group_code": {"required": False, "multi_value": True, "note": "Use get_wpi_metadata() for codes"},
                    "item_code": {"required": False, "multi_value": True, "note": "Use get_wpi_metadata() - 600+ items"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "Energy": {
                "name": "Energy Statistics",
                "description": "Year-Wise Energy Statistics including balance, supply, and consumption data",
                "endpoint": "/api/energy/getEnergyRecords",
                "categories_available": ["Energy_Commodities", "Energy_Sub_Commodities", "End_Use_Sector", "End_Use_Sub_Sector"],
                "parameters": {
                    "indicator_code": {
                        "required": True,
                        "type": "enum",
                        "options": [
                            "Energy Balance ( in KToE )",
                            "Energy Balance ( in PetaJoules )"
                        ],
                        "default": "Energy Balance ( in KToE )"
                    },
                    "use_of_energy_balance_code": {
                        "required": True,
                        "type": "enum",
                        "options": ["Supply", "Consumption"],
                        "default": "Supply"
                    },
                    "year": {"required": False, "format": "YYYY-YY/YYYY", "example": "2023-24 or 2023", "multi_value": True, "description": "Enter the Year (format YYYY-YY/YYYY. Comma separated for multiple values)"},
                    "energy_commodities_code": {"required": False, "range": "1-10", "multi_value": True, "description": "Enter the Energy Commodities code (from 1 to 10. Comma separated for multiple values)", "note": "Use lookup_mospi_codes('Energy', 'Energy_Commodities')"},
                    "energy_sub_commodities_code": {"required": False, "range": "1-12", "multi_value": True, "description": "Enter the Energy Sub_commodities code (from 1 to 12. Comma separated for multiple values)", "note": "Use lookup_mospi_codes('Energy', 'Energy_Sub_Commodities')"},
                    "end_use_sector_code": {"required": False, "range": "1-10", "multi_value": True, "description": "Enter the End Use Sector code (from 1 to 10. Comma separated for multiple values)", "note": "Use lookup_mospi_codes('Energy', 'End_Use_Sector')"},
                    "end_use_sub_sector_code": {"required": False, "range": "1-22", "multi_value": True, "description": "Enter the End Use Sub_sector code (from 1 to 22. Comma separated for multiple values)", "note": "Use lookup_mospi_codes('Energy', 'End_Use_Sub_Sector')"},
                    "page": {"required": False, "range": "1-n", "description": "Enter the page no. (from 1 to n.)"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "HCES": {
                "name": "Household Consumption Expenditure Survey",
                "description": "Year-Wise Household Consumption Expenditure Survey",
                "endpoint": "/api/hces/getHcesRecords",
                "categories_available": ["indicator", "sub_indicator", "state", "sector", "cereal", "employment_of_households", "imputation_type", "mpce_fractile_classes", "item_category", "social_group"],
                "parameters": {
                    "indicator_code": {"required": True, "type": "enum", "options": [
                        "Average monthly per capita consumption expenditure (MPCE)",
                        "Average monthly per capita consumption expenditure (MPCE) Over 12 Fractile Classes",
                        "Monthly Per Capita Consumption Expenditure (MPCE) over Broad Categories in 30 Days",
                        "Percentage Share of Monthly Per Capita Consumption Expenditure (MPCE) over Broad Categories in 30 Days",
                        "Average Per Capita Monthly Quantity Consumption ",
                        "Average Monthly Per Capita Value of Consumption (Rs.)",
                        "Average Monthly Per Capita Consumption Expenditure (MPCE) across different Household Type",
                        "Average Monthly Per Capita Consumption Expenditure (MPCE) across different Social Group",
                        "Gini Coefficient for Per Capita Consumption Expenditure"
                    ], "default": "Average monthly per capita consumption expenditure (MPCE)"},
                    "year": {"required": False, "format": "YYYY-YY/YYYY", "multi_value": True, "description": "Enter the Year (format YYYY-YY/YYYY. Comma separated for multiple values)"},
                    "sub_indicator_code": {"required": False, "range": "1-3", "multi_value": True, "description": "Enter the Sub Indicator code (from 1 to 3. Comma separated for multiple values)"},
                    "state_code": {"required": False, "range": "1-37", "multi_value": True, "description": "Enter the State code (from 1 to 37. Comma separated for multiple values)"},
                    "sector_code": {"required": False, "range": "1-3", "multi_value": True, "description": "Enter the Sector code (from 1 to 3. Comma separated for multiple values)"},
                    "imputation_type_code": {"required": False, "range": "1-2", "multi_value": True, "description": "Enter the Imputation Type code (from 1 to 2. Comma separated for multiple values)"},
                    "mpce_fractile_classes_code": {"required": False, "range": "1-13", "multi_value": True, "description": "Enter the MPCE Fractile Classes code (from 1 to 13. Comma separated for multiple values)"},
                    "item_category_code": {"required": False, "range": "1-31", "multi_value": True, "description": "Enter the Item Category code (from 1 to 31. Comma separated for multiple values)"},
                    "cereal_code": {"required": False, "range": "1-5", "multi_value": True, "description": "Enter the Cereal code (from 1 to 5. Comma separated for multiple values)"},
                    "employment_of_households_code": {"required": False, "range": "1-11", "multi_value": True, "description": "Enter the Employment of Households code (from 1 to 11. Comma separated for multiple values)"},
                    "social_group_code": {"required": False, "range": "1-5", "multi_value": True, "description": "Enter the Social Group code (from 1 to 5. Comma separated for multiple values)"},
                    "page": {"required": False, "range": "1-n", "description": "Enter the page no. (from 1 to n.)"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "NSS78": {
                "name": "National Sample Survey (NSS 78 ROUND)",
                "description": "Indicator-wise National Sample Survey (NSS 78 ROUND)",
                "endpoint": "/api/nss-78/getNss78Records",
                "categories_available": ["Indicator_code", "Subindicator_code", "State_code", "Sector_code", "Gender_code", "AgeGroup_code", "InternetAccess_code", "Household_LeavingReason_code", "Households_code", "SourceOfFinance_code"],
                "parameters": {
                    "Indicator": {"required": True, "type": "enum", "options": [
                        "Usage of Mobile Phone",
                        "Access to Mass Media and Broadband",
                        "Main Reason for Leaving Last Usaul Place of Residence",
                        "Improved Latrine and Hand Washing Facilities Within Household",
                        "Exclusive Access to Improved Latrine",
                        "Income Change Due to Migration",
                        "Household Assets",
                        "Improved Source of Drinking Water Within Household",
                        "Availability of Basic Transport and Public Facility",
                        "Different Sources of Finance",
                        "Usual Place of Residence Different From Current Place",
                        "Possession of Air Conditioner and Air Cooler",
                        "Main Reason for Migration",
                        "Access to Improved Source of Drinking Water"
                    ], "default": "Usage of Mobile Phone"},
                    "State_code": {"required": False, "range": "1-39", "multi_value": True, "description": "Enter the State code (from 1 to 39. Comma separated for multiple values)"},
                    "Sector_code": {"required": False, "range": "1-3", "multi_value": True, "description": "Enter the Sector code (from 1 to 3. Comma separated for multiple values)"},
                    "Gender_code": {"required": False, "range": "1-3", "multi_value": True, "description": "Enter the Gender code (from 1 to 3. Comma separated for multiple values)"},
                    "AgeGroup_code": {"required": False, "range": "1-2", "multi_value": True, "description": "Enter the AgeGroup code (from 1 to 2. Comma separated for multiple values)"},
                    "InternetAccess_code": {"required": False, "range": "1-2", "multi_value": True, "description": "Enter the InternetAccess code (from 1 to 2. Comma separated for multiple values)"},
                    "Household_LeavingReason_code": {"required": False, "range": "1-18", "multi_value": True, "description": "Enter the Household_LeavingReason code (from 1 to 18. Comma separated for multiple values)"},
                    "Subindicator_code": {"required": False, "range": "1-34", "multi_value": True, "description": "Enter the Subindicator code (from 1 to 34. Comma separated for multiple values)"},
                    "Households_code": {"required": False, "range": "1-3", "multi_value": True, "description": "Enter the Households code (from 1 to 3. Comma separated for multiple values)"},
                    "SourceOfFinance_code": {"required": False, "range": "1-5", "multi_value": True, "description": "Enter the SourceOfFinance code (from 1 to 5. Comma separated for multiple values)"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "TUS": {
                "name": "Time Use Survey",
                "description": "How people spend their time across paid work, unpaid domestic work, caregiving, leisure, etc.",
                "endpoint": "/api/tus/getTusRecords",
                "categories_available": ["indicator", "year", "state", "sector", "gender", "age_group", "icatus_activity", "day_of_week"],
                "parameters": {
                    "indicator_code": {"required": True, "range": "4-44", "note": "Use get_tus_indicators() for full list of 41 indicators"},
                    "year": {"required": False, "options": ["2019", "2024"], "multi_value": True},
                    "state_code": {"required": False, "multi_value": True, "note": "Use get_tus_metadata() for state codes"},
                    "sector_code": {"required": False, "range": "1-3", "codes": {"1": "Rural", "2": "Urban", "3": "Combined"}},
                    "gender_code": {"required": False, "codes": {"1": "Male", "2": "Female", "4": "Person"}},
                    "age_group_code": {"required": False, "range": "1-5", "note": "1=6-14yrs, 2=15-29yrs, 3=15-59yrs, 4=60+, 5=All 6+"},
                    "icatus_activity_code": {"required": False, "note": "ICATUS activity classification - use get_tus_metadata()"},
                    "day_of_week_code": {"required": False, "note": "Day type filter"},
                    "page": {"required": False, "range": "1-n"},
                    "limit": {"required": False, "type": "int"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "NFHS": {
                "name": "National Family Health Survey",
                "description": "Health, mortality, nutrition, family planning, women's empowerment data",
                "endpoint": "/api/nfhs/getNfhsRecords",
                "categories_available": ["indicator", "state", "sub_indicator", "sector", "survey"],
                "parameters": {
                    "indicator_code": {"required": True, "range": "1-21", "note": "Use get_nfhs_indicators() for full list"},
                    "state_code": {"required": False, "multi_value": True, "note": "Use get_nfhs_metadata() - 99=All India"},
                    "sub_indicator_code": {"required": False, "multi_value": True, "note": "Varies by indicator - use get_nfhs_metadata()"},
                    "sector_code": {"required": False, "range": "1-3", "codes": {"1": "Rural", "2": "Urban", "3": "Combined"}},
                    "survey_code": {"required": False, "codes": {"2": "NFHS-4", "3": "NFHS-5"}},
                    "page": {"required": False, "range": "1-n"},
                    "limit": {"required": False, "type": "int"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "ASUSE": {
                "name": "Annual Survey of Unincorporated Sector Enterprises",
                "description": "Statistics on non-agricultural unincorporated enterprises (informal sector)",
                "endpoint": "/api/asuse/getAsuseRecords",
                "categories_available": ["frequency", "indicator", "year", "state", "sector", "activity", "establishment_type", "broad_activity_category", "sub_indicator", "owner_education_level", "location_establishment", "operation_duration"],
                "important_note": "Available filters vary by indicator - ALWAYS call get_asuse_metadata() first!",
                "filter_patterns": {
                    "most_indicators": ["year", "sector", "establishment_type"],
                    "indicators_1_4": ["activity (50 detailed categories)"],
                    "indicators_5_9": ["owner_education_level"],
                    "indicators_10_plus": ["location_establishment", "operation_duration"],
                    "indicators_15_plus": ["state", "broad_activity_category"],
                    "indicators_20_plus": ["sub_indicator", "broad_activity_category"]
                },
                "parameters": {
                    "indicator_code": {"required": True, "note": "Use get_asuse_indicators() for list of 35+ indicators"},
                    "frequency_code": {"required": True, "codes": {"1": "Annually", "2": "Quarterly"}, "default": "1"},
                    "year": {"required": False, "format": "YYYY-YY", "example": "2022-23"},
                    "state_code": {"required": False, "multi_value": True, "note": "Only for some indicators - use get_asuse_metadata()"},
                    "sector_code": {"required": False, "range": "1-3", "codes": {"1": "Rural", "2": "Urban", "3": "Combined"}},
                    "activity_code": {"required": False, "note": "Detailed 50 categories - use get_asuse_metadata()"},
                    "establishment_type_code": {"required": False, "codes": {"1": "HWE", "2": "OAE", "3": "All"}},
                    "broad_activity_category_code": {"required": False, "codes": {"1": "Manufacturing", "2": "Trade", "3": "Other Services", "4": "All"}},
                    "sub_indicator_code": {"required": False, "note": "e.g., 5=Using Computer, 6=Using Internet"},
                    "owner_education_level_code": {"required": False, "note": "Education level of owner"},
                    "location_establishment_code": {"required": False, "note": "Location type"},
                    "operation_duration_code": {"required": False, "note": "Duration of operation"},
                    "page": {"required": False, "range": "1-n"},
                    "limit": {"required": False, "type": "int"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "Gender": {
                "name": "Gender Statistics",
                "description": "Comprehensive gender-disaggregated data covering demographics, health, education, labour, time use, financial inclusion, political participation, and crimes against women",
                "endpoint": "/api/gender/getGenderRecords",
                "total_indicators": 157,
                "categories_available": ["year", "sector", "gender", "state", "age_group", "sub_indicator", "crime_head"],
                "important_note": "Available filters vary significantly by indicator - ALWAYS call get_gender_metadata() first!",
                "indicator_themes": {
                    "population_demographics": "Indicators 1-7: Sex ratio, population trends",
                    "fertility_mortality": "Indicators 8-21: TFR, IMR, MMR, life expectancy",
                    "health": "Indicators 22-53: Maternal care, HIV, diseases, BMI",
                    "education": "Indicators 55-79: Literacy, enrollment, dropout, GPI",
                    "labour": "Indicators 80-95: LFPR, WPR, wages, unemployment",
                    "time_use": "Indicators 96-104: Unpaid work, activity participation",
                    "financial_inclusion": "Indicators 105-122: Banking, schemes, SHGs",
                    "political_participation": "Indicators 123-137: Elections, representation",
                    "crime_against_women": "Indicators 140-157: Rape, domestic violence, cyber crimes"
                },
                "parameters": {
                    "indicator_code": {"required": True, "range": "1-157", "note": "Use get_gender_indicators() for full list"},
                    "year": {"required": False, "note": "Format varies by indicator (YYYY or YYYY-YY)"},
                    "sector_code": {"required": False, "codes": {"1": "Rural", "2": "Urban", "3": "Total"}},
                    "gender_code": {"required": False, "codes": {"1": "Male", "2": "Female", "7": "Person"}},
                    "state_ut_code": {"required": False, "note": "For state-wise indicators only"},
                    "age_group_code": {"required": False, "note": "For labour indicators"},
                    "sub_indicator_code": {"required": False, "note": "For crime and other multi-part indicators"},
                    "crime_head_code": {"required": False, "note": "For crime indicators (140-157)"},
                    "page": {"required": False, "range": "1-n"},
                    "limit": {"required": False, "type": "int"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "RBI": {
                "name": "RBI Statistics",
                "description": "Reserve Bank of India data - foreign trade, balance of payments, forex rates, external debt",
                "endpoint": "/api/rbi/getRbiRecords",
                "total_indicators": 39,
                "categories_available": ["year", "month", "quarter", "country_group", "country", "trade_type", "currency", "reserve_type"],
                "important_note": "Available filters vary significantly by indicator - ALWAYS call get_rbi_metadata() first!",
                "indicator_themes": {
                    "foreign_trade": "Indicators 1,2,11-17,20,24,42-46: Direction, exports, imports by commodity/country",
                    "balance_of_payments": "Indicators 4-10,14,22: BoP quarterly/annual, invisibles",
                    "external_debt": "Indicators 25-27: USD/Rupees, quarterly",
                    "forex_rates": "Indicators 29,31-37: Exchange rates monthly/annual, 155 currencies",
                    "forex_reserves": "Indicators 47-48: Monthly/annual reserves",
                    "rbi_operations": "Indicators 28,30,40: USD sale/purchase, forex turnover, NRI deposits"
                },
                "parameters": {
                    "sub_indicator_code": {"required": True, "range": "1-48", "note": "Use get_rbi_indicators() for full list"},
                    "year": {"required": False, "note": "Format varies (YYYY or YYYY-YY)"},
                    "month_code": {"required": False, "note": "For monthly indicators"},
                    "quarter_code": {"required": False, "note": "For quarterly BoP indicators"},
                    "country_group_code": {"required": False, "note": "Africa, Asia, OECD, OPEC, etc."},
                    "country_code": {"required": False, "note": "Specific country"},
                    "trade_type_code": {"required": False, "codes": {"1": "Export", "2": "Import"}},
                    "currency_code": {"required": False, "note": "For forex rate indicators"},
                    "reserve_type_code": {"required": False, "note": "For forex reserve indicators"},
                    "page": {"required": False, "range": "1-n"},
                    "limit": {"required": False, "type": "int"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "AISHE": {
                "name": "All India Survey on Higher Education",
                "description": "Higher education statistics - universities, colleges, enrolment, GER, GPI, teachers",
                "endpoint": "/api/aishe/getAisheRecords",
                "total_indicators": 9,
                "categories_available": ["year", "state", "university_type", "college_type", "social_group", "gender", "level"],
                "important_note": "Available filters vary by indicator - ALWAYS call get_aishe_metadata() first!",
                "indicator_list": {
                    "1": "Number of Universities",
                    "2": "Number of Colleges",
                    "3": "Student Enrolment",
                    "4": "Social Group-wise Enrolment",
                    "5": "PWD & Minority Enrolment",
                    "6": "Gross Enrolment Ratio (GER)",
                    "7": "Gender Parity Index (GPI)",
                    "8": "Pupil Teacher Ratio",
                    "9": "Number of Teachers"
                },
                "parameters": {
                    "indicator_code": {"required": True, "range": "1-9", "note": "Use get_aishe_indicators() for full list"},
                    "year": {"required": False, "format": "YYYY-YY", "example": "2020-21"},
                    "state_code": {"required": False, "note": "State/UT code"},
                    "sub_indicator_code": {"required": False, "note": "Sub-indicator"},
                    "university_type_code": {"required": False, "note": "Type of university"},
                    "college_type_code": {"required": False, "note": "Type of college"},
                    "social_group_code": {"required": False, "note": "SC/ST/OBC/General"},
                    "gender_code": {"required": False, "note": "Gender filter"},
                    "level_code": {"required": False, "note": "Education level"},
                    "page": {"required": False, "range": "1-n"},
                    "limit": {"required": False, "type": "int"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "CPIALRL": {
                "name": "CPI for Agricultural Labourers and Rural Labourers",
                "description": "Consumer Price Index for agricultural labourers (AL) and rural labourers (RL)",
                "endpoint": "/api/cpialrl/getCpialrlRecords",
                "total_indicators": 2,
                "categories_available": ["base_year", "year", "month", "state", "group"],
                "indicator_list": {
                    "1": "General Index - Overall CPI for agricultural/rural labourers",
                    "2": "Group Index - CPI by commodity groups"
                },
                "parameters": {
                    "indicator_code": {"required": True, "range": "1-2", "note": "1=General Index, 2=Group Index"},
                    "base_year": {"required": False, "options": ["1986-1987", "2019"]},
                    "year": {"required": False, "format": "YYYY-YYYY", "example": "2023-2024"},
                    "month_code": {"required": False, "range": "1-12"},
                    "state_code": {"required": False, "note": "31 states + All India"},
                    "group_code": {"required": False, "note": "Commodity group (for Group Index)"},
                    "page": {"required": False, "range": "1-n"},
                    "limit": {"required": False, "type": "int"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            },
            "NSS77": {
                "name": "NSS 77th Round - Land and Livestock Holdings Survey",
                "description": "Land holdings, agricultural income, crop production, livestock, and insurance data (Jan-Dec 2019)",
                "endpoint": "/api/nss-77/getNss77Records",
                "total_indicators": 33,
                "categories_available": ["state", "visit", "land_possessed_household", "agricultural_household", "caste", "season", "sub_indicator"],
                "important_note": "Available filters vary significantly by indicator - ALWAYS call get_nss77_metadata() first!",
                "indicator_themes": {
                    "land_holdings": "Indicators 16-19, 34-37, 40-41: Land possession, ownership, leasing",
                    "income": "Indicators 24-25: Agricultural household income",
                    "expenses": "Indicators 26-29, 31-32: Farm and non-farm expenses",
                    "crops": "Indicators 21-23, 42-47: Crop production, sales, farming resources",
                    "loans_insurance": "Indicators 33, 48-51: Loans outstanding, crop insurance",
                    "livestock": "Indicator 39: Livestock ownership"
                },
                "parameters": {
                    "indicator_code": {"required": True, "range": "16-51", "note": "Use get_nss77_indicators() for full list"},
                    "state_code": {"required": False, "note": "37=All India, 38=Group of NE States, 39=Group of UTs"},
                    "visit_code": {"required": False, "options": ["1", "2"]},
                    "land_possessed_household_code": {"required": False, "range": "1-8", "note": "Land size class"},
                    "agricultural_household_code": {"required": False, "codes": {"1": "Agricultural", "2": "Non-agricultural", "3": "All"}},
                    "caste_code": {"required": False, "codes": {"1": "ST", "2": "SC", "3": "OBC", "4": "Others", "5": "All"}},
                    "season_code": {"required": False, "note": "Survey period"},
                    "sub_indicator_code": {"required": False, "note": "Specific sub-indicators"},
                    "page": {"required": False, "range": "1-n"},
                    "limit": {"required": False, "type": "int"},
                    "Format": {"required": True, "options": ["JSON", "CSV"], "default": "JSON"}
                }
            }
        },
        "critical_notes": {
            "state_codes_warning": "⚠️ CRITICAL: State codes are DIFFERENT across datasets! Rajasthan is code 19 in PLFS but code 8 in CPI/ASI!",
            "cpi_endpoint_limitation": "⚠️ CRITICAL: CPI_Item does NOT support state_code! For ANY state-specific CPI query (e.g., 'CPI for Rice in Maharashtra'), you MUST use CPI_Group, NOT CPI_Item. CPI_Item is only for All-India item-level data.",
            "planning_strategy": "Before making ANY API calls: 1) Identify which dataset(s) you need, 2) List all parameter categories you'll need codes for, 3) Make strategic batch_lookup_codes calls to get all codes at once, 4) Then make your data API calls, 5) Use Limits to get a lot of data for multi year queries",
            "multi_value_support": "Most parameters support comma-separated values for multiple selections (e.g., '1,2,3')",
            "pagination": "Use 'page' parameter for large result sets"
        },
        "efficiency_guidelines": {
            "DO": [
                "Call get_X_indicators() first to see available indicators",
                "Call get_X_metadata() to get filter codes before data calls",
                "Use comma-separated values for multiple codes",
                "Use 'limit' parameter to control response size"
            ],
            "AVOID": [
                "Guessing state codes without verification",
                "Starting data calls without understanding API structure",
                "Assuming parameter combinations work across datasets"
            ]
        },
    }
    
    return api_docs

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