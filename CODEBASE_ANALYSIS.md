# MoSPI MCP Server - Comprehensive Codebase Analysis

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Client Query Workflow](#client-query-workflow)
4. [Tools & Their API Mappings](#tools--their-api-mappings)
5. [Dataset-Specific API Mappings](#dataset-specific-api-mappings)
6. [Complete MoSPI API Reference](#complete-mospi-api-reference)
7. [Progressive Disclosure Analysis](#progressive-disclosure-analysis)
8. [Context Issues & Recommendations](#context-issues--recommendations)

---

## Project Overview

**Project Name:** MoSPI MCP Server
**Purpose:** A Model Context Protocol (MCP) server providing unified access to 18 Indian Government statistical datasets from the Ministry of Statistics and Programme Implementation (MoSPI).

**Framework:** FastMCP 2.0 (Production Ready)
**Base API:** `https://api.mospi.gov.in`

### File Structure

```
mospi-mcp-api/
├── mospi_server.py          # Main MCP server with 5 tools (689 lines)
├── mospi/
│   ├── __init__.py          # Package exports
│   └── client.py            # MoSPI API client wrapper (778 lines)
├── tests/                   # Test suite (19 files)
├── Dockerfile               # Container deployment
└── requirements.txt         # Dependencies
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT (Claude/LLM)                          │
│                    "What's unemployment in Maharashtra?"             │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ MCP Protocol (HTTP/stdio)
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MOSPI_SERVER.PY (FastMCP 2.0)                     │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                      5 MCP TOOLS                                │ │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │ │
│  │  │ know_about_     │  │ get_indicators  │  │ get_metadata   │  │ │
│  │  │ mospi_api()     │  │ (dataset)       │  │ (dataset,      │  │ │
│  │  │ [Step 0]        │  │ [Step 1]        │  │ indicator...)  │  │ │
│  │  └─────────────────┘  └─────────────────┘  │ [Step 2]       │  │ │
│  │                                            └────────────────┘  │ │
│  │  ┌─────────────────┐  ┌─────────────────┐                      │ │
│  │  │ get_data        │  │ get_dataset_    │                      │ │
│  │  │ (dataset,       │  │ info(dataset)   │                      │ │
│  │  │ filters)        │  │ [Optional]      │                      │ │
│  │  │ [Step 3]        │  └─────────────────┘                      │ │
│  │  └─────────────────┘                                           │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ HELPER: transform_filters() - Converts user keys to API format │ │
│  │ CONSTANTS: VALID_DATASETS, DATASET_PARAMS, PARAM_ALIASES       │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MOSPI/CLIENT.PY (API Client)                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ class MoSPI:                                                    │ │
│  │   - api_endpoints: Dict mapping datasets to API paths           │ │
│  │   - get_data(dataset, params): Generic data fetcher             │ │
│  │   - get_{dataset}_indicators(): 14 indicator methods            │ │
│  │   - get_{dataset}_filters(): 14 filter/metadata methods         │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│ Global Instance: mospi = MoSPI()                                    │
└─────────────────────────────┬───────────────────────────────────────┘
                              │ HTTP GET requests (30s timeout)
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MOSPI OPEN DATA API                               │
│              https://api.mospi.gov.in/api/{dataset}/...             │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │ 18 Datasets × 3 Endpoint Types:                                 │ │
│  │   1. /get{Dataset}IndicatorList     → List indicators           │ │
│  │   2. /get{Dataset}FilterByIndicator → Get filter options        │ │
│  │   3. /get{Dataset}Records           → Fetch actual data         │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Client Query Workflow

### Example: "What's the unemployment rate in Maharashtra for 2023?"

```
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 0: Dataset Discovery (Optional)                                │
├─────────────────────────────────────────────────────────────────────┤
│ Tool: know_about_mospi_api()                                        │
│ Purpose: Get overview of 18 datasets to find the right one          │
│                                                                      │
│ Returns:                                                             │
│   - Dataset descriptions with use_for hints                         │
│   - Workflow instructions                                            │
│   - Critical rules (state codes differ, hidden data exists)         │
│                                                                      │
│ Result: PLFS is for "Jobs, unemployment, wages..."                  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 1: Get Indicators                                              │
├─────────────────────────────────────────────────────────────────────┤
│ Tool: get_indicators("PLFS")                                        │
│                                                                      │
│ Internal Call:                                                       │
│   mospi.get_plfs_indicators()                                       │
│   → GET /api/plfs/getIndicatorListByFrequency                       │
│                                                                      │
│ Returns: List of 8 indicators                                       │
│   - indicator_code: 1 → "LFPR"                                      │
│   - indicator_code: 2 → "WPR"                                       │
│   - indicator_code: 3 → "Unemployment Rate" ← USER NEEDS THIS       │
│   - indicator_code: 4 → "Wages"                                     │
│   - ... etc                                                          │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 2: Get Metadata (Filter Options)                               │
├─────────────────────────────────────────────────────────────────────┤
│ Tool: get_metadata("PLFS", indicator_code=3)                        │
│                                                                      │
│ Internal Call:                                                       │
│   mospi.get_plfs_filters(indicator_code=3, frequency_code=1)        │
│   → GET /api/plfs/getFilterByIndicatorId?indicator_code=3&...       │
│                                                                      │
│ Returns: Valid filter options                                        │
│   - states: [{id: "27", name: "Maharashtra"}, ...]                  │
│   - years: ["2023", "2022", "2021", ...]                            │
│   - sectors: [{id: "1", name: "Rural"}, {id: "2", name: "Urban"}]   │
│   - genders: [{id: "1", name: "Male"}, {id: "2", name: "Female"}]   │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ STEP 3: Fetch Data                                                  │
├─────────────────────────────────────────────────────────────────────┤
│ Tool: get_data("PLFS", {                                            │
│   "indicator_code": "3",                                            │
│   "state_code": "27",                                               │
│   "year": "2023"                                                    │
│ })                                                                   │
│                                                                      │
│ Internal Processing:                                                 │
│   1. transform_filters() converts keys if needed                    │
│   2. dataset_map["PLFS"] → "PLFS"                                   │
│   3. mospi.get_data("PLFS", transformed_filters)                    │
│   → GET /api/plfs/getData?indicator_code=3&state_code=27&year=2023  │
│                                                                      │
│ Returns: Actual unemployment data records                           │
│   [{                                                                 │
│     "indicator": "Unemployment Rate",                               │
│     "state": "Maharashtra",                                         │
│     "year": 2023,                                                   │
│     "value": 4.2,                                                   │
│     "unit": "percent"                                               │
│   }, ...]                                                            │
└─────────────────────────────────────────────────────────────────────┘
```

### Workflow Variations by Dataset Type

| Dataset Type | Step 1 | Step 2 | Step 3 |
|-------------|--------|--------|--------|
| **Standard** (PLFS, NAS, GENDER, etc.) | get_indicators → indicator list | get_metadata(indicator_code) | get_data(filters) |
| **CPI** | Returns "uses levels" message | get_metadata(base_year, level="Group"/"Item") | Auto-routes to CPI_GROUP or CPI_ITEM |
| **IIP** | Returns "uses categories" message | get_metadata(base_year, frequency="Annually"/"Monthly") | Auto-routes to IIP_ANNUAL or IIP_MONTHLY |
| **WPI** | Returns "hierarchical codes" message | get_metadata() returns full structure | get_data(group/item codes) |
| **ASI** | Returns "uses classification years" | get_metadata(classification_year="2008") | get_data(filters) |

---

## Tools & Their API Mappings

### Tool 1: `know_about_mospi_api()`

**Purpose:** Step 0 - Dataset discovery
**API Calls:** None (returns static documentation)
**Returns:**
- 18 dataset descriptions with `use_for` hints
- Workflow instructions
- Critical rules about state codes and hidden data

### Tool 2: `get_indicators(dataset)`

**Purpose:** Step 1 - List available indicators
**Location:** mospi_server.py:206-257

| Dataset | Client Method | API Endpoint |
|---------|---------------|--------------|
| PLFS | `mospi.get_plfs_indicators()` | `/api/plfs/getIndicatorListByFrequency` |
| NAS | `mospi.get_nas_indicators()` | `/api/nas/getNasIndicatorList` |
| NSS78 | `mospi.get_nss78_indicators()` | `/api/nss-78/getIndicatorList` |
| NSS77 | `mospi.get_nss77_indicators()` | `/api/nss-77/getIndicatorList` |
| HCES | `mospi.get_hces_indicators()` | `/api/hces/getHcesIndicatorList` |
| ENERGY | `mospi.get_energy_indicators()` | `/api/energy/getEnergyIndicatorList` |
| TUS | `mospi.get_tus_indicators()` | `/api/tus/getTusIndicatorList` |
| NFHS | `mospi.get_nfhs_indicators()` | `/api/nfhs/getNfhsIndicatorList` |
| ASUSE | `mospi.get_asuse_indicators()` | `/api/asuse/getAsuseIndicatorListByFrequency` |
| GENDER | `mospi.get_gender_indicators()` | `/api/gender/getGenderIndicatorList` |
| RBI | `mospi.get_rbi_indicators()` | `/api/rbi/getRbiIndicatorList` |
| ENVSTATS | `mospi.get_envstats_indicators()` | `/api/env/getEnvStatsIndicatorList` |
| AISHE | `mospi.get_aishe_indicators()` | `/api/aishe/getAisheIndicatorList` |
| CPIALRL | `mospi.get_cpialrl_indicators()` | `/api/cpialrl/getCpialrlIndicatorList` |
| **CPI** | Returns message | No indicator endpoint (uses levels) |
| **IIP** | Returns message | No indicator endpoint (uses categories) |
| **WPI** | Returns message | No indicator endpoint (hierarchical) |
| **ASI** | Returns message | Uses classification years |

### Tool 3: `get_metadata(dataset, indicator_code, ...)`

**Purpose:** Step 2 - Get filter options
**Location:** mospi_server.py:260-388

| Dataset | Required Params | Client Method | API Endpoint |
|---------|----------------|---------------|--------------|
| PLFS | `indicator_code` | `get_plfs_filters(indicator_code, frequency_code)` | `/api/plfs/getFilterByIndicatorId` |
| CPI | `base_year`, `level` | `get_cpi_filters(base_year, level)` | `/api/cpi/getCpiFilterByLevelAndBaseYear` |
| IIP | `base_year`, `frequency` | `get_iip_filters(base_year, frequency)` | `/api/iip/getIipFilter` |
| ASI | `classification_year` | `get_asi_filters(classification_year)` | `/api/asi/getAsiFilter` |
| WPI | None | `get_wpi_filters()` | `/api/wpi/getWpiData` |
| NAS | `indicator_code` | `get_nas_filters(series, frequency_code, indicator_code)` | `/api/nas/getNasFilterByIndicatorId` |
| NSS78 | `indicator_code` | `get_nss78_filters(indicator_code, sub_indicator_code)` | `/api/nss-78/getFilterByIndicatorId` |
| NSS77 | `indicator_code` | `get_nss77_filters(indicator_code)` | `/api/nss-77/getFilterByIndicatorId` |
| HCES | `indicator_code` (default 1) | `get_hces_filters(indicator_code)` | `/api/hces/getHcesFilterByIndicatorId` |
| ENERGY | `indicator_code` | `get_energy_filters(indicator_code, use_of_energy_balance_code)` | `/api/energy/getEnergyFilterByIndicatorId` |
| TUS | `indicator_code` | `get_tus_filters(indicator_code)` | `/api/tus/getTusFilterByIndicatorId` |
| NFHS | `indicator_code` | `get_nfhs_filters(indicator_code)` | `/api/nfhs/getnfhsFilterByIndicatorId` |
| ASUSE | `indicator_code` | `get_asuse_filters(indicator_code, frequency_code)` | `/api/asuse/getAsuseFilterByIndicatorId` |
| GENDER | `indicator_code` | `get_gender_filters(indicator_code)` | `/api/gender/getGenderFilterByIndicatorId` |
| RBI | `indicator_code` | `get_rbi_filters(sub_indicator_code)` | `/api/rbi/getRbiMetaData` |
| ENVSTATS | `indicator_code` | `get_envstats_filters(indicator_code)` | `/api/env/getEnvStatsFilterByIndicatorId` |
| AISHE | `indicator_code` | `get_aishe_filters(indicator_code)` | `/api/aishe/getAisheFilterByIndicatorId` |
| CPIALRL | `indicator_code` | `get_cpialrl_filters(indicator_code)` | `/api/cpialrl/getCpialrlFilterByIndicatorId` |

### Tool 4: `get_data(dataset, filters)`

**Purpose:** Step 3 - Fetch actual data
**Location:** mospi_server.py:391-452

| Dataset | API Key in Client | Data Endpoint |
|---------|-------------------|---------------|
| PLFS | `PLFS` | `/api/plfs/getData` |
| CPI (Group) | `CPI_Group` | `/api/cpi/getCPIIndex` |
| CPI (Item) | `CPI_Item` | `/api/cpi/getItemIndex` |
| IIP (Annual) | `IIP_Annual` | `/api/iip/getIIPAnnual` |
| IIP (Monthly) | `IIP_Monthly` | `/api/iip/getIIPMonthly` |
| ASI | `ASI` | `/api/asi/getASIData` |
| NAS | `NAS` | `/api/nas/getNASData` |
| WPI | `WPI` | `/api/wpi/getWpiRecords` |
| Energy | `Energy` | `/api/energy/getEnergyRecords` |
| HCES | `HCES` | `/api/hces/getHcesRecords` |
| NSS78 | `NSS78` | `/api/nss-78/getNss78Records` |
| NSS77 | `NSS77` | `/api/nss-77/getNss77Records` |
| TUS | `TUS` | `/api/tus/getTusRecords` |
| NFHS | `NFHS` | `/api/nfhs/getNfhsRecords` |
| ASUSE | `ASUSE` | `/api/asuse/getAsuseRecords` |
| GENDER | `GENDER` | `/api/gender/getGenderRecords` |
| RBI | `RBI` | `/api/rbi/getRbiRecords` |
| ENVSTATS | `ENVSTATS` | `/api/env/getEnvStatsRecords` |
| AISHE | `AISHE` | `/api/aishe/getAisheRecords` |
| CPIALRL | `CPIALRL` | `/api/cpialrl/getCpialrlRecords` |

### Tool 5: `get_dataset_info(dataset)`

**Purpose:** Get dataset description/metadata (only when explicitly requested)
**API Endpoint:** `https://api.mospi.gov.in/api/esankhyiki/cms/getMetaDataByProduct`

---

## Dataset-Specific API Mappings

### 1. PLFS (Periodic Labour Force Survey)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/plfs/getIndicatorListByFrequency` | None |
| Filters | `/api/plfs/getFilterByIndicatorId` | `indicator_code`, `frequency_code` |
| Data | `/api/plfs/getData` | `indicator_code`, `frequency_code`, `year`, `state_code`, `sector_code`, `gender_code`, `age_code`, etc. |

**Valid Parameters:** indicator_code, frequency_code, year, page, limit, Format, state_code, sector_code, gender_code, age_code, weekly_status_code, religion_code, social_category_code, education_code, broad_industry_work_code, broad_status_employment_code, employee_contract_code, enterprise_size_code, enterprise_type_code, industry_section_code, nco_division_code, nic_group_code, quarter_code, month_code

---

### 2. CPI (Consumer Price Index)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Filters | `/api/cpi/getCpiFilterByLevelAndBaseYear` | `base_year`, `level` |
| Data (Group) | `/api/cpi/getCPIIndex` | `base_year`, `series`, `year`, `month_code`, `state_code`, `group_code`, `subgroup_code`, `sector_code` |
| Data (Item) | `/api/cpi/getItemIndex` | `base_year`, `year`, `month_code`, `item_code` |

**Auto-Routing Logic:**
- If filters contain `item_code` → routes to `CPI_Item`
- Otherwise → routes to `CPI_Group`

---

### 3. IIP (Index of Industrial Production)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Filters | `/api/iip/getIipFilter` | `base_year`, `frequency` |
| Data (Annual) | `/api/iip/getIIPAnnual` | `base_year`, `financial_year`, `category_code`, `subcategory_code` |
| Data (Monthly) | `/api/iip/getIIPMonthly` | `base_year`, `year`, `month_code`, `category_code`, `subcategory_code` |

**Auto-Routing Logic:**
- If filters contain `month_code` → routes to `IIP_Monthly`
- Otherwise → routes to `IIP_Annual`

---

### 4. ASI (Annual Survey of Industries)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Classification Years | `/api/asi/getNicClassificationYear` | None |
| Filters | `/api/asi/getAsiFilter` | `classification_year` |
| Data | `/api/asi/getASIData` | `classification_year`, `sector_code`, `year`, `indicator_code`, `state_code`, `nic_code`, `nic_type` |

---

### 5. NAS (National Accounts Statistics)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/nas/getNasIndicatorList` | None |
| Filters | `/api/nas/getNasFilterByIndicatorId` | `series`, `frequency_code`, `indicator_code` |
| Data | `/api/nas/getNASData` | `series`, `frequency_code`, `year`, `indicator_code`, `quarterly_code`, `approach_code`, `revision_code`, `institutional_code`, `industry_code`, `subindustry_code` |

---

### 6. WPI (Wholesale Price Index)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Filters | `/api/wpi/getWpiData` | None |
| Data | `/api/wpi/getWpiRecords` | `year`, `month_code`, `major_group_code`, `group_code`, `sub_group_code`, `sub_sub_group_code`, `item_code` |

---

### 7. ENERGY (Energy Statistics)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/energy/getEnergyIndicatorList` | None |
| Filters | `/api/energy/getEnergyFilterByIndicatorId` | `indicator_code`, `use_of_energy_balance_code` |
| Data | `/api/energy/getEnergyRecords` | `indicator_code`, `use_of_energy_balance_code`, `year`, `energy_commodities_code`, `energy_sub_commodities_code`, `end_use_sector_code`, `end_use_sub_sector_code` |

---

### 8. HCES (Household Consumption Expenditure Survey)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/hces/getHcesIndicatorList` | None |
| Filters | `/api/hces/getHcesFilterByIndicatorId` | `indicator_code` |
| Data | `/api/hces/getHcesRecords` | `indicator_code`, `year`, `sub_indicator_code`, `state_code`, `sector_code`, `imputation_type_code`, `mpce_fractile_classes_code`, `item_category_code`, `cereal_code`, `employment_of_households_code`, `social_group_code` |

---

### 9. NSS78 (Living Conditions Survey)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/nss-78/getIndicatorList` | None |
| Filters | `/api/nss-78/getFilterByIndicatorId` | `indicator_code`, `sub_indicator_code` |
| Data | `/api/nss-78/getNss78Records` | `indicator_code`, `state_code`, `sector_code`, `gender_code`, `agegroup_code`, `internetaccess_code`, `household_leavingreason_code`, `subindicator_code`, `households_code`, `sourceoffinance_code` |

---

### 10. NSS77 (Land & Livestock Survey)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/nss-77/getIndicatorList` | None |
| Filters | `/api/nss-77/getFilterByIndicatorId` | `indicator_code` |
| Data | `/api/nss-77/getNss77Records` | `indicator_code`, `state_code`, `visit_code`, `land_possessed_household_code`, `agricultural_household_code`, `caste_code`, `season_code`, `sub_indicator_code`, `social_group_code`, `size_class_code` |

---

### 11. TUS (Time Use Survey)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/tus/getTusIndicatorList` | None |
| Filters | `/api/tus/getTusFilterByIndicatorId` | `indicator_code` |
| Data | `/api/tus/getTusRecords` | `indicator_code`, `year`, `state_code`, `sector_code`, `gender_code`, `age_group_code`, `icatus_activity_code`, `day_of_week_code` |

---

### 12. NFHS (National Family Health Survey)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/nfhs/getNfhsIndicatorList` | None |
| Filters | `/api/nfhs/getnfhsFilterByIndicatorId` | `indicator_code` |
| Data | `/api/nfhs/getNfhsRecords` | `indicator_code`, `state_code`, `sub_indicator_code`, `sector_code`, `survey_code` |

---

### 13. ASUSE (Unincorporated Enterprises Survey)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Frequencies | `/api/asuse/getAsuseFrequencyList` | None |
| Indicators | `/api/asuse/getAsuseIndicatorListByFrequency` | `frequency_code` |
| Filters | `/api/asuse/getAsuseFilterByIndicatorId` | `indicator_code`, `frequency_code` |
| Data | `/api/asuse/getAsuseRecords` | `indicator_code`, `frequency_code`, `year`, `state_code`, `sector_code`, `activity_code`, `establishment_type_code`, `broad_activity_category_code`, `sub_indicator_code`, `owner_education_level_code`, `location_establishment_code`, `operation_duration_code` |

---

### 14. GENDER (Gender Statistics)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/gender/getGenderIndicatorList` | None |
| Filters | `/api/gender/getGenderFilterByIndicatorId` | `indicator_code` |
| Data | `/api/gender/getGenderRecords` | `indicator_code`, `year`, `sector_code`, `gender_code`, `state_ut_code`, `age_group_code`, `sub_indicator_code`, `crime_head_code` |

**Special Alias:** `state` → `state_ut_code`

---

### 15. RBI (Reserve Bank Statistics)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/rbi/getRbiIndicatorList` | None |
| Filters | `/api/rbi/getRbiMetaData` | `sub_indicator_code` |
| Data | `/api/rbi/getRbiRecords` | `sub_indicator_code`, `year`, `month_code`, `quarter_code`, `country_group_code`, `country_code`, `trade_type_code`, `currency_code`, `reserve_type_code`, `reserve_currency_code`, `indicator_code` |

**Special:** Uses `sub_indicator_code` as main identifier instead of `indicator_code`

---

### 16. ENVSTATS (Environment Statistics)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/env/getEnvStatsIndicatorList` | None |
| Filters | `/api/env/getEnvStatsFilterByIndicatorId` | `indicator_code` |
| Data | `/api/env/getEnvStatsRecords` | `indicator_code`, `year`, `state_code`, `sub_indicator_code`, `season_code`, `month_code`, `city_code`, `parameter_code`, `forest_type_code`, `phylum_code`, `disaster_type_code`, `river_length_code`, `sub_basin_code` |

**Special:** Indicator 16 has global biodiversity data with `phylum_code` filter

---

### 17. AISHE (Higher Education Survey)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/aishe/getAisheIndicatorList` | None |
| Filters | `/api/aishe/getAisheFilterByIndicatorId` | `indicator_code` |
| Data | `/api/aishe/getAisheRecords` | `indicator_code`, `year`, `state_code`, `sub_indicator_code`, `university_type_code`, `college_type_code`, `social_group_code`, `gender_code`, `level_code` |

---

### 18. CPIALRL (Rural Labourers CPI)

| Operation | API Endpoint | Parameters |
|-----------|-------------|------------|
| Indicators | `/api/cpialrl/getCpialrlIndicatorList` | None |
| Filters | `/api/cpialrl/getCpialrlFilterByIndicatorId` | `indicator_code` |
| Data | `/api/cpialrl/getCpialrlRecords` | `indicator_code`, `base_year`, `year`, `month_code`, `state_code`, `group_code` |

---

## Complete MoSPI API Reference

### All API Endpoints Used (55 Total)

| # | Endpoint Category | Full URL | Purpose |
|---|------------------|----------|---------|
| 1 | PLFS Indicators | `/api/plfs/getIndicatorListByFrequency` | List PLFS indicators |
| 2 | PLFS Filters | `/api/plfs/getFilterByIndicatorId` | Get PLFS filter options |
| 3 | PLFS Data | `/api/plfs/getData` | Fetch PLFS data |
| 4 | CPI Filters | `/api/cpi/getCpiFilterByLevelAndBaseYear` | Get CPI filter options |
| 5 | CPI Group Data | `/api/cpi/getCPIIndex` | Fetch CPI group-level data |
| 6 | CPI Item Data | `/api/cpi/getItemIndex` | Fetch CPI item-level data |
| 7 | IIP Filters | `/api/iip/getIipFilter` | Get IIP filter options |
| 8 | IIP Annual Data | `/api/iip/getIIPAnnual` | Fetch annual IIP data |
| 9 | IIP Monthly Data | `/api/iip/getIIPMonthly` | Fetch monthly IIP data |
| 10 | ASI Class Years | `/api/asi/getNicClassificationYear` | List NIC classification years |
| 11 | ASI Filters | `/api/asi/getAsiFilter` | Get ASI filter options |
| 12 | ASI Data | `/api/asi/getASIData` | Fetch ASI data |
| 13 | NAS Indicators | `/api/nas/getNasIndicatorList` | List NAS indicators |
| 14 | NAS Filters | `/api/nas/getNasFilterByIndicatorId` | Get NAS filter options |
| 15 | NAS Data | `/api/nas/getNASData` | Fetch NAS data |
| 16 | WPI Filters | `/api/wpi/getWpiData` | Get WPI filter structure |
| 17 | WPI Data | `/api/wpi/getWpiRecords` | Fetch WPI data |
| 18 | Energy Indicators | `/api/energy/getEnergyIndicatorList` | List Energy indicators |
| 19 | Energy Filters | `/api/energy/getEnergyFilterByIndicatorId` | Get Energy filter options |
| 20 | Energy Data | `/api/energy/getEnergyRecords` | Fetch Energy data |
| 21 | HCES Indicators | `/api/hces/getHcesIndicatorList` | List HCES indicators |
| 22 | HCES Filters | `/api/hces/getHcesFilterByIndicatorId` | Get HCES filter options |
| 23 | HCES Data | `/api/hces/getHcesRecords` | Fetch HCES data |
| 24 | NSS78 Indicators | `/api/nss-78/getIndicatorList` | List NSS78 indicators |
| 25 | NSS78 Filters | `/api/nss-78/getFilterByIndicatorId` | Get NSS78 filter options |
| 26 | NSS78 Data | `/api/nss-78/getNss78Records` | Fetch NSS78 data |
| 27 | NSS77 Indicators | `/api/nss-77/getIndicatorList` | List NSS77 indicators |
| 28 | NSS77 Filters | `/api/nss-77/getFilterByIndicatorId` | Get NSS77 filter options |
| 29 | NSS77 Data | `/api/nss-77/getNss77Records` | Fetch NSS77 data |
| 30 | TUS Indicators | `/api/tus/getTusIndicatorList` | List TUS indicators |
| 31 | TUS Filters | `/api/tus/getTusFilterByIndicatorId` | Get TUS filter options |
| 32 | TUS Data | `/api/tus/getTusRecords` | Fetch TUS data |
| 33 | NFHS Indicators | `/api/nfhs/getNfhsIndicatorList` | List NFHS indicators |
| 34 | NFHS Filters | `/api/nfhs/getnfhsFilterByIndicatorId` | Get NFHS filter options |
| 35 | NFHS Data | `/api/nfhs/getNfhsRecords` | Fetch NFHS data |
| 36 | ASUSE Frequencies | `/api/asuse/getAsuseFrequencyList` | List ASUSE frequencies |
| 37 | ASUSE Indicators | `/api/asuse/getAsuseIndicatorListByFrequency` | List ASUSE indicators |
| 38 | ASUSE Filters | `/api/asuse/getAsuseFilterByIndicatorId` | Get ASUSE filter options |
| 39 | ASUSE Data | `/api/asuse/getAsuseRecords` | Fetch ASUSE data |
| 40 | Gender Indicators | `/api/gender/getGenderIndicatorList` | List Gender indicators |
| 41 | Gender Filters | `/api/gender/getGenderFilterByIndicatorId` | Get Gender filter options |
| 42 | Gender Data | `/api/gender/getGenderRecords` | Fetch Gender data |
| 43 | RBI Indicators | `/api/rbi/getRbiIndicatorList` | List RBI indicators |
| 44 | RBI Filters | `/api/rbi/getRbiMetaData` | Get RBI filter options |
| 45 | RBI Data | `/api/rbi/getRbiRecords` | Fetch RBI data |
| 46 | EnvStats Indicators | `/api/env/getEnvStatsIndicatorList` | List EnvStats indicators |
| 47 | EnvStats Filters | `/api/env/getEnvStatsFilterByIndicatorId` | Get EnvStats filter options |
| 48 | EnvStats Data | `/api/env/getEnvStatsRecords` | Fetch EnvStats data |
| 49 | AISHE Indicators | `/api/aishe/getAisheIndicatorList` | List AISHE indicators |
| 50 | AISHE Filters | `/api/aishe/getAisheFilterByIndicatorId` | Get AISHE filter options |
| 51 | AISHE Data | `/api/aishe/getAisheRecords` | Fetch AISHE data |
| 52 | CPIALRL Indicators | `/api/cpialrl/getCpialrlIndicatorList` | List CPIALRL indicators |
| 53 | CPIALRL Filters | `/api/cpialrl/getCpialrlFilterByIndicatorId` | Get CPIALRL filter options |
| 54 | CPIALRL Data | `/api/cpialrl/getCpialrlRecords` | Fetch CPIALRL data |
| 55 | Dataset Metadata | `/api/esankhyiki/cms/getMetaDataByProduct` | Get dataset description |

---

## Progressive Disclosure Analysis

### Current Progressive Disclosure Flow

```
Level 0: know_about_mospi_api()
├── Returns: 18 dataset summaries with use_for hints
├── Context given: Dataset names, descriptions, what they're good for
└── User learns: Which dataset to pick

Level 1: get_indicators(dataset)
├── Returns: List of indicators with codes and names
├── Context given: What metrics are available
└── User learns: Which indicator code to use

Level 2: get_metadata(dataset, indicator_code, ...)
├── Returns: All valid filter values (states, years, categories)
├── Context given: Valid codes for each filter dimension
└── User learns: What parameters are available and their valid values

Level 3: get_data(dataset, filters)
├── Returns: Actual data records
├── Context given: The data itself
└── User learns: The answer to their query
```

### Strengths of Current Disclosure

1. **Clear 4-Step Workflow**
   - Each step has a clear purpose
   - User can't skip steps (data needs metadata, metadata needs indicators)

2. **Good Hints in `know_about_mospi_api()`**
   - `use_for` field helps dataset selection
   - Critical rules warn about state code differences
   - Mentions hidden data (ENVSTATS global biodiversity)

3. **Tool Docstrings Guide Behavior**
   - Clear step numbering ("Step 1", "Step 2", "Step 3")
   - Warnings about when to ask vs. when to fetch
   - Special cases documented

4. **Smart Auto-Routing**
   - CPI automatically routes to Group/Item based on filters
   - IIP automatically routes to Annual/Monthly based on filters

---

## Context Issues & Recommendations

### Issues Identified

#### 1. **INSUFFICIENT: Indicator Descriptions Missing**

**Location:** `get_indicators()` return value
**Problem:** Returns indicator codes and names, but not descriptions of what data each indicator actually contains.

**Example:** PLFS indicator 3 is "Unemployment Rate" but doesn't explain:
- Is it by usual status or current weekly status?
- What age groups does it cover?
- What breakdowns are available?

**Recommendation:** Add `description` field to indicator list, or return it if the API provides it.

```python
# Current return:
{"indicator_code": 3, "name": "Unemployment Rate"}

# Better:
{"indicator_code": 3, "name": "Unemployment Rate",
 "description": "Unemployment rate by usual principal activity status (upss) for age 15+"}
```

---

#### 2. **INSUFFICIENT: No Guidance on Required vs Optional Filters**

**Location:** `get_metadata()` return value
**Problem:** Returns all available filters but doesn't indicate:
- Which filters are required vs optional
- Default values if filters are omitted
- How filters interact with each other

**Recommendation:** Add a `required` flag or return structure:

```python
{
    "required_filters": ["indicator_code", "year"],
    "optional_filters": ["state_code", "sector_code", "gender_code"],
    "filter_options": {...}
}
```

---

#### 3. **REDUNDANT: `know_about_mospi_api()` vs `get_dataset_info()` Overlap**

**Problem:** These two tools have overlapping purposes:
- `know_about_mospi_api()` gives brief descriptions of all 18 datasets
- `get_dataset_info()` gives detailed info about one dataset

**Recommendation:** Clarify in docstrings:
- `know_about_mospi_api()` = "Which dataset do I need?" (comparison)
- `get_dataset_info()` = "Tell me more about this dataset" (deep dive)

---

#### 4. **INSUFFICIENT: Parameter Transformation Not Transparent**

**Location:** `transform_filters()` and `PARAM_ALIASES`
**Problem:** The LLM doesn't know that:
- `state` transforms to `state_code` for most datasets
- `state` transforms to `state_ut_code` for GENDER
- RBI uses `sub_indicator_code` instead of `indicator_code`

**Recommendation:** Document aliases in `get_metadata()` return or add helper tool.

---

#### 5. **INSUFFICIENT: Error Messages Not Actionable**

**Location:** Various error returns
**Problem:** Error messages don't tell user how to fix the issue.

```python
# Current:
{"error": "indicator_code is required for PLFS"}

# Better:
{"error": "indicator_code is required for PLFS",
 "suggestion": "Call get_indicators('PLFS') first to see available indicators"}
```

---

#### 6. **INSUFFICIENT: Special Datasets Not Well Explained**

**Location:** `get_indicators()` special_datasets messages
**Problem:** Messages like "CPI uses levels (Group/Item) instead of indicators" are vague.

**Recommendation:** Expand special dataset messages:

```python
"CPI": {
    "message": "CPI uses levels instead of indicators",
    "levels": {
        "Group": "State-level CPI by commodity groups",
        "Item": "All-India level for 600+ individual items"
    },
    "next_step": "Call get_metadata(dataset='CPI', base_year='2012', level='Group')"
}
```

---

#### 7. **REDUNDANT: Critical Rules Only in One Place**

**Location:** `know_about_mospi_api()` critical_rules
**Problem:** If LLM doesn't call this tool, it misses important warnings about state codes.

**Recommendation:** Include relevant warnings in each tool's response:

```python
# In get_metadata() for datasets with state filters:
{
    "filters": {...},
    "warnings": ["State codes differ across datasets. Always use codes from this response."]
}
```

---

#### 8. **MISSING: No Data Availability Indicator**

**Problem:** `get_metadata()` returns all possible filter combinations, but not all have data.

**Recommendation:** Either:
1. Return data availability hints in metadata, OR
2. Add a `check_data_availability(dataset, filters)` tool

---

### Summary of Recommendations

| Priority | Issue | Recommendation |
|----------|-------|----------------|
| **High** | Indicator descriptions missing | Add descriptions to indicator list returns |
| **High** | No required vs optional filter guidance | Add required_filters field to metadata |
| **Medium** | Error messages not actionable | Include "next step" suggestions in errors |
| **Medium** | Special datasets poorly explained | Expand special_datasets messages with examples |
| **Medium** | Parameter aliases not transparent | Document aliases in metadata or add helper tool |
| **Low** | Tool overlap (know_about vs get_info) | Clarify distinct purposes in docstrings |
| **Low** | Critical rules only in one place | Repeat relevant warnings in each response |
| **Low** | No data availability indicator | Consider adding availability check tool |

---

## Appendix: Quick Reference Card

### Dataset → Use For

| Dataset | Use For |
|---------|---------|
| PLFS | Unemployment, jobs, wages, workforce |
| CPI | Consumer inflation, price indices |
| IIP | Industrial production |
| ASI | Factory sector statistics |
| NAS | GDP, economic growth |
| WPI | Wholesale inflation |
| ENERGY | Energy supply/consumption |
| HCES | Consumer spending, poverty |
| NSS78 | Living conditions, digital access |
| NSS77 | Agriculture, land, livestock |
| TUS | Time use, unpaid work |
| NFHS | Health, nutrition |
| ASUSE | Informal sector |
| GENDER | Gender gaps, women's welfare |
| RBI | Trade, forex, external debt |
| ENVSTATS | Environment, biodiversity |
| AISHE | Higher education |
| CPIALRL | Rural laborer inflation |

### Common Gotchas

1. **State codes differ** - Always call get_metadata() to get correct state codes
2. **RBI uses sub_indicator_code** - Not indicator_code like others
3. **CPI has two modes** - Group (state-level) vs Item (All-India only)
4. **IIP has two frequencies** - Annual vs Monthly (auto-routed)
5. **ENVSTATS has global data** - Indicator 16 has world species counts
