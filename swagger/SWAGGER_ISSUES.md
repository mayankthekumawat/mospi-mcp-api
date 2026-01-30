# Swagger YAML Issues

## PLFS
**Swagger params:** indicator_code, frequency_code, year, month_code, state_code, gender_code, age_code, sector_code, weekly_status_code, religion_code, social_category_code, education_code, broad_industry_work_code, broad_status_employment_code, employee_contract_code, enterprise_size_code, enterprise_type_code, industry_section_code, nco_division_code, nic_group_code, quarter_code, page, Format

**Issues:**
- Add `required: true` on `indicator_code` (API fails without it)
- Fix `month_code` description: says "Financial Year" should say "Month code"
- Missing `limit` param (undocumented but works)

## CPI
**Swagger params (getCPIIndex):** base_year, series, year, month_code, state_code, group_code, subgroup_code, sector_code, page, Format

**Swagger params (getItemIndex):** base_year, year, month_code, item_code, page, Format

**Issues:**
- Missing `limit` param on both endpoints

## IIP
**Swagger params (getIIPAnnual):** base_year, financial_year, category_code, subcategory_code, page, type, Format

**Swagger params (getIIPMonthly):** base_year, year, month_code, category_code, subcategory_code, page, type, Format

**Issues:**
- Missing `limit` param on both endpoints

## ASI
**Swagger params:** classification_year, sector_code, year, indicator_code, state_code, nic_code, page, nic_type, Format

**Issues:**
- Missing `limit` param
- Verify indicator count: description says "1 to 56", should be 57

## NAS
**Swagger params:** series, frequency_code, indicator_code, quarterly_code, year, approach_code, revision_code, account_code, institutional_code, industry_code, subindustry_code, page, Format

**Issues:**
- Missing `limit` param
- `indicator_code` description is commented out (line 39)
- `frequency_code`: swagger shows strings ("Annually"/"Quarterly") - API accepts BOTH strings and integers (1/2)
- Note: `account_code` exists in swagger but appears to be IGNORED by API (tested - no filtering effect). Can be removed from swagger.

## WPI
**Swagger params (WRONG CASE):** Year, Month_code, Majorgroup_code, Group_code, Subgroup_code, Sub_subgroup_code, Item_code, Format

**Correct params (snake_case):** year, month_code, major_group_code, group_code, sub_group_code, sub_sub_group_code, item_code, Format

**Issues:**
- Missing `limit` param
- Missing `page` param
- **FIX ALL PARAM NAMES** - currently PascalCase, should be snake_case:
  - `Year` -> `year`
  - `Month_code` -> `month_code`
  - `Majorgroup_code` -> `major_group_code`
  - `Group_code` -> `group_code`
  - `Subgroup_code` -> `sub_group_code`
  - `Sub_subgroup_code` -> `sub_sub_group_code`
  - `Item_code` -> `item_code`
- Remove or uncomment `Commodity_code`

## ENERGY
**Swagger params:** indicator_code, use_of_energy_balance_code, year, energy_commodities_code, energy_sub_commodities_code, end_use_sector_code, end_use_sub_sector_code, page, Format

**Issues:**
- Missing `limit` param
- `indicator_code` and `use_of_energy_balance_code`: swagger shows string enums but API accepts BOTH strings and integers
- Remove duplicate commented `use_of_energy_balance_code` (lines 34-38)

---

## HCES
**Swagger params:** indicator_code, year, sub_indicator_code, state_code, sector_code, imputation_type_code, mpce_fractile_classes_code, item_category_code, cereal_code, employment_of_households_code, social_group_code, page, Format

**Issues:**
- `indicator_code` uses full string enums (e.g. "Average monthly per capita consumption expenditure (MPCE)") instead of integer codes - API accepts both but our server sends integers
- Missing `limit` param
- Trailing space in indicator enum value: `"Average Per Capita Monthly Quantity Consumption "` (line 29)

## NSS78
**Swagger params (WRONG CASE):** Indicator, State_code, Sector_code, Gender_code, AgeGroup_code, InternetAccess_code, Household_LeavingReason_code, Subindicator_code, Households_code, SourceOfFinance_code, Format

**Issues:**
- **FIX ALL PARAM NAMES** - PascalCase/mixed case, should be snake_case:
  - `Indicator` -> `indicator_code`
  - `State_code` -> `state_code`
  - `Sector_code` -> `sector_code`
  - `Gender_code` -> `gender_code`
  - `AgeGroup_code` -> `age_group_code`
  - `InternetAccess_code` -> `internet_access_code`
  - `Household_LeavingReason_code` -> `household_leaving_reason_code`
  - `Subindicator_code` -> `sub_indicator_code`
  - `Households_code` -> `households_code`
  - `SourceOfFinance_code` -> `source_of_finance_code`
- `Indicator` uses full string enums instead of integer codes
- Typo in indicator: "Main Reason for Leaving Last **Usaul** Place" -> should be "Usual"
- `page` param is commented out
- Missing `limit` param

## NSS77
**Swagger params:** indicator_code, state_code, gender_code, visit_code, land_possessed_hosehold_code, agricultural_household_code, caste_code, household_employment_code, household_employment_sub_code, major_disposal_code, agency_code, experienced_crop_code, crop_code, sub_experienced_crop_code, operational_holding_code, season_code, sub_satisfactory_code, satisfactory_code, sub_major_procurement_code, major_procurement_code, resource_code, sub_resource_code, agency_procurement_code, seed_procurements_code, sub_seed_procurements_code, expenditure_recipt_code, business_type_code, productive_assets_code, expenses_recipt_code, crop_production_code, farming_animals_code, expenses_imputed_code, receipts_type_code, loan_outstanding_code, ownership_holding_code, ownership_holding_area_code, terms_lease_code, livestock_owned_code, stock_code, possession_code, possession_holding_code, harvested_code, sub_harvested_code, crop_agency_code, crop_satisfaction_code, crop_procurement_code, crop_insurance_code, crop_experienced_code, quality_seeds_code, insurance_awareness_code, crop_loss_code, msp_awareness_code, sub_indicator_code, Format

**Issues:**
- `indicator_code` uses full string enums instead of integer codes
- **Typo:** `land_possessed_hosehold_code` -> should be `land_possessed_household_code` (missing 'u')
- **Typo:** `expenditure_recipt_code` -> should be `expenditure_receipt_code`
- **Typo:** `expenses_recipt_code` -> should be `expenses_receipt_code`
- One indicator is commented out (too long for YAML line?)
- `page` param is commented out
- Missing `limit` param
- Massive param count (53 params) - many are indicator-specific

## TUS
**Swagger params:** indicator_code, year, sub_indicator_code, state_code, sector_code, gender_code, day_of_week_code, household_member_code, age_group_code, icatus_activity_code, activity_code, usual_principal_activity_code, broad_principal_activity_status_code, place_of_activity_code, sna_activity_code, marital_status_code, quintile_class_of_umpce_code, level_of_education_code, employment_status_code, social_group_code, page, Format

**Issues:**
- `indicator_code` uses full string enums instead of integer codes
- Multiple typos in indicator names: "activtities" (should be "activities"), "activites" (should be "activities")
- `social_group_code` description says "Social  code" (missing word "Group", double space)
- Missing `limit` param

## NFHS
**Swagger params:** indicator_code, sub_indicator_code, state_code, survey_code, limit, page, format

**Issues:**
- **Different swagger structure** than other datasets (concise format, added by us not MoSPI?)
- Tag says "MFHS" instead of "NFHS" (typo in tag name, line 8)
- `format` is lowercase (other datasets use `Format` PascalCase)
- Format accepts `xlsx` not JSON/CSV enum - different pattern from all other datasets
- Has `limit` (default 20) - one of the few datasets that includes it
- Missing filter params in swagger that exist in API description (line 16 mentions `_code` orphan)

## ASUSE
**Swagger params:** indicator_code, year, state_ut_code, sub_indicator_code, activity_category_code, sector_code, gender_code, ownership_type_code, establishment_type_code, general_education_level_code, social_group_of_owner_major_partner_code, broad_activity_category_code, other_economic_activitycount_code, account_holder_code, location_of_establishments_code, nature_of_operation_code, no_of_months_operated_code, no_of_working_hours_code, audit_status_code, npi_status_code, acts_agency_of_registration_code, services_contract_code, nature_of_employment_code, type_of_worker_code, hired_worker_code, fixed_assets_code, usage_of_internet_code, worker_characteristics_code, worker_number_code, frequency_code, page, Format

**Issues:**
- Uses `state_ut_code` instead of `state_code` (inconsistent with other datasets)
- Missing `limit` param
- `frequency_code` description just says "Annually,monthly,quaterly" - typo "quaterly" -> "quarterly"

## GENDER
**Swagger params:** indicator_code, year, quarter_code, sub_indicator_code, state_ut_code, sector_code, gender_code, age_group_code, birth_order_code, education_level_code, survey_code, family_planning_method_code, ayush_category_code, discipline_code, nco_division_code, employment_category_code, industry_code, bank_group_code, activity_code, broad_activity_category_code, type_of_establishment_code, deposit_code, scheme_code, lok_sabha_election_code, police_code, court_code, service_code, crime_head_code, category_code, page, Format

**Issues:**
- `indicator_code` uses full string enums (100+ indicators!) instead of integer codes
- Uses `state_ut_code` instead of `state_code` (inconsistent with other datasets)
- Typo in indicator: "Meningococcal Meningitis Infection**v**" (extra "v" at end, line 67)
- Missing `limit` param
- Massive indicator list - could break LLM context if sent as enum

## RBI
**Swagger params:** sub_indicator_code, year, limit, page, format

**Issues:**
- **Different swagger structure** than other datasets (concise format)
- Primary key is `sub_indicator_code` NOT `indicator_code` (unique among all datasets)
- `format` is lowercase (other datasets use `Format` PascalCase)
- Format accepts `xlsx` not JSON/CSV enum
- Has `limit` (default 20)
- Very few filter params - description mentions state_code, survey_code but they're not in params
- Description on line 16 has orphan `_code` text

## ENVSTATS
**Swagger params:** indicator_code, year, month_code, quarter_code, state_code, region_code, sector_code, sub_indicator_code, livestock_marine_products_code, wetland_type_area_code, limit, page, format

**Issues:**
- **Different swagger structure** (concise format)
- `format` is lowercase (other datasets use `Format` PascalCase)
- Format accepts `xlsx` not JSON/CSV enum
- Has `limit` (default 20)
- **MASSIVE missing params** - description lists 50+ filter params but only 10 are defined in parameters section. Missing params include: river_code, soil_code, land_degradation_code, land_use_category_code, land_cover_code, phylum_code, risk_status_code, risk_category_code, carbon_pool_code, cities_code, emission_source_code, area_code, area_type_code, monitoring_station_code, minerals_metal_code, fuel_mineral_sub_cate_code, basin_code, commodity_code, cultivated_area_code, fertilizer_code, foodgrain_code, fuel_type_code, hazardous_waste_code, lenght_of_road_code, major_discipline_code, metalic_mineral_sub_cate_code, minerals_category_code, movement_by_road_transport_code, nfhs_round_code, nonmetalic_minerl_sub_cate_code, ore_code, ozone_depleting_substance_code, pesticides_insecticides_code, revenue_realised_code, river_length_code, scheme_code, slums_code, source_drinking_water_code, source_irrigation_code, source_power_generation_code, species_code, sub_basin_code, subsidy_scheme_code, type_of_coal_code, vehicles_registered_code, site_code, causes_code, broad_discipline_code, zone_code, land_use_sub_category_code
- Typo in description: `wetland_type_area_code` listed twice

## AISHE
**Swagger params:** indicator_code, limit, page, format

**Issues:**
- **Different swagger structure** (concise format)
- `format` is lowercase (other datasets use `Format` PascalCase)
- Format accepts `xlsx` not JSON/CSV enum
- Has `limit` (default 20)
- **MASSIVE missing params** - description lists filter params (sub_indicator_code, gender_code, state_code, category_code, social_group_code, institution_type_code, faculty_type_code, learning_mode_code, year) but NONE are in the parameters section

## CPIALRL
**Swagger params:** indicator_code, base_year_code, year, month_code, state_code, groups_code, page, Format

**Issues:**
- `indicator_code` uses full string enums ("General Index", "Group Index") instead of integer codes
- Missing `limit` param

---

## Cross-Dataset Patterns

### Inconsistent `format` / `Format` casing
- **PascalCase `Format` (JSON/CSV):** PLFS, CPI, IIP, ASI, NAS, WPI, ENERGY, HCES, NSS78, NSS77, TUS, ASUSE, GENDER, CPIALRL
- **Lowercase `format` (xlsx):** NFHS, RBI, ENVSTATS, AISHE

### Inconsistent `state_code` naming
- **`state_code`:** PLFS, CPI, IIP, ASI, NAS, HCES, NSS78, NSS77, TUS, NFHS, ENVSTATS, CPIALRL
- **`state_ut_code`:** ASUSE, GENDER

### Datasets with `limit` param
- **Has `limit`:** NFHS, RBI, ENVSTATS, AISHE (all use default: 20)
- **Missing `limit`:** PLFS, CPI, IIP, ASI, NAS, WPI, ENERGY, HCES, NSS78, NSS77, TUS, ASUSE, GENDER, CPIALRL

### Datasets using string enums for `indicator_code`
- **String enums:** HCES, NSS78, NSS77, TUS, GENDER, ENERGY, CPIALRL
- **Integer codes:** PLFS, CPI (uses base_year), IIP (uses base_year), ASI, NAS, NFHS, ASUSE, ENVSTATS, AISHE
- **Sub_indicator as primary:** RBI

### PascalCase param issues (need snake_case)
- **WPI:** Year, Month_code, Majorgroup_code, Group_code, Subgroup_code, Sub_subgroup_code, Item_code
- **NSS78:** Indicator, State_code, Sector_code, Gender_code, AgeGroup_code, InternetAccess_code, Household_LeavingReason_code, Subindicator_code, Households_code, SourceOfFinance_code

### Different swagger structure
- **Standard (verbose, MoSPI-authored):** PLFS, CPI, IIP, ASI, NAS, WPI, ENERGY, HCES, NSS78, NSS77, TUS, ASUSE, GENDER, CPIALRL
- **Concise (custom-authored?):** NFHS, RBI, ENVSTATS, AISHE
