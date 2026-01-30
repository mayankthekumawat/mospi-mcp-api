# MoSPI Swagger Validation Report

Generated: 2026-01-29 14:24:06

Datasets tested: 20

## Summary

| Dataset | Baseline | Swagger Params | Accepted | Variants | Undocumented | Case Issues |
|---------|----------|----------------|----------|----------|--------------|-------------|
| PLFS | PASS | 23/23 | 23/23 | 4 | 2/2 | - |
| CPI_Group | PASS | 10/10 | 10/10 | 3 | 2/2 | - |
| CPI_Item | PASS | 6/6 | 6/6 | 1 | 2/2 | - |
| IIP_Annual | PASS | 7/7 | 7/7 | 3 | 2/2 | - |
| IIP_Monthly | PASS | 8/8 | 8/8 | 2 | 2/2 | - |
| ASI | FAIL (200) | 0/0 | 0/0 | - | - | - |
| NAS | PASS | 13/13 | 13/13 | 4 | 2/2 | - |
| WPI | PASS | 8/8 | 8/8 | - | 3/3 | 0 |
| ENERGY | PASS | 9/9 | 9/9 | 3 | 2/2 | - |
| HCES | PASS | 13/13 | 13/13 | 3 | 2/2 | - |
| NSS78 | PASS | 10/11 | 10/11 | 3 | 3/3 | 0 |
| NFHS | PASS | 7/7 | 7/7 | 3 | 1/1 | - |
| ASUSE | PASS | 32/32 | 32/32 | 2 | 2/2 | - |
| TUS | PASS | 22/22 | 22/22 | 2 | 2/2 | - |
| GENDER | PASS | 31/31 | 31/31 | 3 | 2/2 | - |
| RBI | PASS | 5/5 | 5/5 | 2 | 1/1 | - |
| ENVSTATS | PASS | 13/13 | 13/13 | 3 | 1/1 | - |
| AISHE | PASS | 4/4 | 4/4 | 2 | 1/1 | - |
| CPIALRL | PASS | 8/8 | 8/8 | 2 | 2/2 | - |
| NSS77 | PASS | 54/54 | 54/54 | 3 | 3/3 | - |

---

## PLFS

- **Endpoint:** `/api/plfs/getData`
- **Swagger:** `swagger_user_plfs.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (23 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `indicator_code` |  | integer | Yes |  | in baseline |
| `frequency_code` |  | string | Yes |  | in baseline |
| `year` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `month_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `state_code` |  | string | Yes |  |  |
| `gender_code` |  | string | Yes |  |  |
| `age_code` |  | string | Yes |  |  |
| `sector_code` |  | string | Yes |  |  |
| `weekly_status_code` |  | string | Yes |  |  |
| `religion_code` |  | string | Yes |  |  |
| `social_category_code` |  | string | Yes |  |  |
| `education_code` |  | string | Yes |  |  |
| `broad_industry_work_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `broad_status_employment_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `employee_contract_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `enterprise_size_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `enterprise_type_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `industry_section_code` |  | string | Yes |  |  |
| `nco_division_code` |  | string | Yes |  |  |
| `nic_group_code` |  | string | Yes |  |  |
| `quarter_code` |  | string | Yes |  |  |
| `page` |  | string | Yes |  |  |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (4 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **Ind1+Annual** (indicator_code=1, frequency_code=1): PASS, 10 records, metadata: 9 filters
  - Metadata filters: `year`, `age`, `education`, `gender`, `religion`, `sector`, `social_category`, `state`, `weekly_status`
- **Ind2+Annual** (indicator_code=2, frequency_code=1): PASS, 10 records, metadata: 9 filters
  - Metadata filters: `year`, `age`, `education`, `gender`, `religion`, `sector`, `social_category`, `state`, `weekly_status`
- **Ind3+Annual** (indicator_code=3, frequency_code=1): PASS, 10 records, metadata: 9 filters
  - Metadata filters: `year`, `age`, `education`, `gender`, `religion`, `sector`, `social_category`, `state`, `weekly_status`
- **Ind1+Quarterly** (indicator_code=1, frequency_code=2): PASS, 10 records, metadata: 6 filters
  - Metadata filters: `year`, `quarter`, `age`, `gender`, `sector`, `state`

| Parameter | In Swagger | Ind1+Annual | Ind2+Annual | Ind3+Annual | Ind1+Quarterly |
|-----------|------------|------|------|------|------|
| `age_code` | Yes | OK(10) | OK(10) | OK(10) | OK(10) |
| `broad_industry_work_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `broad_status_employment_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `education_code` | Yes | OK(10) | OK(10) | OK(10) | FILTERS(0) |
| `employee_contract_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `enterprise_size_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `enterprise_type_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `frequency_code` | Yes | (baseline) | (baseline) | (baseline) | (baseline) |
| `gender_code` | Yes | OK(10) | OK(10) | OK(10) | OK(10) |
| `indicator_code` | Yes | (baseline) | (baseline) | (baseline) | (baseline) |
| `industry_section_code` | Yes | OK(10) | OK(10) | OK(10) | FILTERS(0) |
| `month_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `nco_division_code` | Yes | OK(10) | OK(10) | OK(10) | FILTERS(0) |
| `nic_group_code` | Yes | OK(10) | OK(10) | OK(10) | FILTERS(0) |
| `page` | Yes | OK(10) | OK(10) | OK(10) | OK(10) |
| `quarter_code` | Yes | OK(10) | OK(10) | OK(10) | FILTERS(0) |
| `religion_code` | Yes | OK(10) | OK(10) | OK(10) | FILTERS(0) |
| `sector_code` | Yes | OK(10) | OK(10) | OK(10) | OK(10) |
| `social_category_code` | Yes | OK(10) | OK(10) | OK(10) | FILTERS(0) |
| `state_code` | Yes | OK(10) | OK(10) | OK(10) | OK(10) |
| `weekly_status_code` | Yes | OK(10) | OK(10) | OK(10) | FILTERS(0) |
| `year` | Yes | OKM(10) | OKM(10) | OKM(10) | OKM(10) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **Ind1+Annual**: Swagger-only (not in metadata): `age_code`, `broad_industry_work_code`, `broad_status_employment_code`, `education_code`, `employee_contract_code`, `enterprise_size_code`, `enterprise_type_code`, `gender_code`, `industry_section_code`, `month_code`, `nco_division_code`, `nic_group_code`, `quarter_code`, `religion_code`, `sector_code`, `social_category_code`, `state_code`, `weekly_status_code`
- **Ind1+Annual**: Metadata-only (not in swagger): `age`, `education`, `gender`, `religion`, `sector`, `social_category`, `state`, `weekly_status`
- **Ind2+Annual**: Swagger-only (not in metadata): `age_code`, `broad_industry_work_code`, `broad_status_employment_code`, `education_code`, `employee_contract_code`, `enterprise_size_code`, `enterprise_type_code`, `gender_code`, `industry_section_code`, `month_code`, `nco_division_code`, `nic_group_code`, `quarter_code`, `religion_code`, `sector_code`, `social_category_code`, `state_code`, `weekly_status_code`
- **Ind2+Annual**: Metadata-only (not in swagger): `age`, `education`, `gender`, `religion`, `sector`, `social_category`, `state`, `weekly_status`
- **Ind3+Annual**: Swagger-only (not in metadata): `age_code`, `broad_industry_work_code`, `broad_status_employment_code`, `education_code`, `employee_contract_code`, `enterprise_size_code`, `enterprise_type_code`, `gender_code`, `industry_section_code`, `month_code`, `nco_division_code`, `nic_group_code`, `quarter_code`, `religion_code`, `sector_code`, `social_category_code`, `state_code`, `weekly_status_code`
- **Ind3+Annual**: Metadata-only (not in swagger): `age`, `education`, `gender`, `religion`, `sector`, `social_category`, `state`, `weekly_status`
- **Ind1+Quarterly**: Swagger-only (not in metadata): `age_code`, `broad_industry_work_code`, `broad_status_employment_code`, `education_code`, `employee_contract_code`, `enterprise_size_code`, `enterprise_type_code`, `gender_code`, `industry_section_code`, `month_code`, `nco_division_code`, `nic_group_code`, `quarter_code`, `religion_code`, `sector_code`, `social_category_code`, `state_code`, `weekly_status_code`
- **Ind1+Quarterly**: Metadata-only (not in swagger): `age`, `gender`, `quarter`, `sector`, `state`

**Hierarchy-dependent params** (behave differently across variants):
- `education_code`: Ind1+Annual: OK(10) [NOT in meta] | Ind2+Annual: OK(10) [NOT in meta] | Ind3+Annual: OK(10) [NOT in meta] | Ind1+Quarterly: filters(0) [NOT in meta]
- `industry_section_code`: Ind1+Annual: OK(10) [NOT in meta] | Ind2+Annual: OK(10) [NOT in meta] | Ind3+Annual: OK(10) [NOT in meta] | Ind1+Quarterly: filters(0) [NOT in meta]
- `nco_division_code`: Ind1+Annual: OK(10) [NOT in meta] | Ind2+Annual: OK(10) [NOT in meta] | Ind3+Annual: OK(10) [NOT in meta] | Ind1+Quarterly: filters(0) [NOT in meta]
- `nic_group_code`: Ind1+Annual: OK(10) [NOT in meta] | Ind2+Annual: OK(10) [NOT in meta] | Ind3+Annual: OK(10) [NOT in meta] | Ind1+Quarterly: filters(0) [NOT in meta]
- `quarter_code`: Ind1+Annual: OK(10) [NOT in meta] | Ind2+Annual: OK(10) [NOT in meta] | Ind3+Annual: OK(10) [NOT in meta] | Ind1+Quarterly: filters(0) [NOT in meta]
- `religion_code`: Ind1+Annual: OK(10) [NOT in meta] | Ind2+Annual: OK(10) [NOT in meta] | Ind3+Annual: OK(10) [NOT in meta] | Ind1+Quarterly: filters(0) [NOT in meta]
- `social_category_code`: Ind1+Annual: OK(10) [NOT in meta] | Ind2+Annual: OK(10) [NOT in meta] | Ind3+Annual: OK(10) [NOT in meta] | Ind1+Quarterly: filters(0) [NOT in meta]
- `weekly_status_code`: Ind1+Annual: OK(10) [NOT in meta] | Ind2+Annual: OK(10) [NOT in meta] | Ind3+Annual: OK(10) [NOT in meta] | Ind1+Quarterly: filters(0) [NOT in meta]

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

Integer indicator only (string 'test_string_name' -> 500: {'error': 'Please check the input parameters passed'})

---

## CPI_Group

- **Endpoint:** `/api/cpi/getCPIIndex`
- **Swagger:** `swagger_user_cpi.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (10 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `base_year` | Yes | string | Yes |  | in baseline |
| `series` | Yes | string | Yes |  | in baseline |
| `year` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `month_code` |  | string | Yes |  |  |
| `state_code` |  | string | Yes |  |  |
| `group_code` |  | string | Yes |  |  |
| `subgroup_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sector_code` |  | string | Yes |  |  |
| `page` |  | string | Yes |  |  |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (3 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **2012+Current** (base_year=2012, series=Current): PASS, 10 records, metadata: 7 filters
  - Metadata filters: `series`, `year`, `month`, `state`, `sector`, `group`, `subgroup`
- **2012+Back** (base_year=2012, series=Back): PASS, 10 records, metadata: 7 filters
  - Metadata filters: `series`, `year`, `month`, `state`, `sector`, `group`, `subgroup`
- **2010+Current** (base_year=2010, series=Current): PASS, 10 records, metadata: 7 filters
  - Metadata filters: `series`, `year`, `month`, `state`, `sector`, `group`, `subgroup`

| Parameter | In Swagger | 2012+Current | 2012+Back | 2010+Current |
|-----------|------------|------|------|------|
| `base_year` | Yes | (baseline) | (baseline) | (baseline) |
| `group_code` | Yes | OK(10) | OK(10) | FILTERS(0) |
| `month_code` | Yes | OK(10) | OK(10) | OK(10) |
| `page` | Yes | OK(10) | OK(10) | OK(10) |
| `sector_code` | Yes | OK(10) | OK(10) | OK(10) |
| `series` | Yes | (baseline) | (baseline) | (baseline) |
| `state_code` | Yes | OK(10) | OK(10) | OK(10) |
| `subgroup_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `year` | Yes | OKM(10) | FILTERSM(0) | OKM(10) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **2012+Current**: Swagger-only (not in metadata): `group_code`, `month_code`, `sector_code`, `state_code`, `subgroup_code`
- **2012+Current**: Metadata-only (not in swagger): `group`, `month`, `sector`, `state`, `subgroup`
- **2012+Back**: Swagger-only (not in metadata): `group_code`, `month_code`, `sector_code`, `state_code`, `subgroup_code`
- **2012+Back**: Metadata-only (not in swagger): `group`, `month`, `sector`, `state`, `subgroup`
- **2010+Current**: Swagger-only (not in metadata): `group_code`, `month_code`, `sector_code`, `state_code`, `subgroup_code`
- **2010+Current**: Metadata-only (not in swagger): `group`, `month`, `sector`, `state`, `subgroup`

**Hierarchy-dependent params** (behave differently across variants):
- `group_code`: 2012+Current: OK(10) [NOT in meta] | 2012+Back: OK(10) [NOT in meta] | 2010+Current: filters(0) [NOT in meta]
- `year`: 2012+Current: OK(10) [in meta] | 2012+Back: filters(0) [in meta] | 2010+Current: OK(10) [in meta]

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

No indicator param found

---

## CPI_Item

- **Endpoint:** `/api/cpi/getItemIndex`
- **Swagger:** `swagger_user_cpi.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (6 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `base_year` | Yes | string | Yes |  | in baseline |
| `year` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `month_code` |  | string | Yes |  |  |
| `item_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `page` |  | string | Yes |  |  |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (1 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **2012** (base_year=2012): PASS, 10 records, metadata: 3 filters
  - Metadata filters: `year`, `month`, `item`

| Parameter | In Swagger | 2012 |
|-----------|------------|------|
| `base_year` | Yes | (baseline) |
| `item_code` | Yes | FILTERS(0) |
| `month_code` | Yes | OK(10) |
| `page` | Yes | OK(10) |
| `year` | Yes | OKM(10) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **2012**: Swagger-only (not in metadata): `item_code`, `month_code`
- **2012**: Metadata-only (not in swagger): `item`, `month`

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

No indicator param found

---

## IIP_Annual

- **Endpoint:** `/api/iip/getIIPAnnual`
- **Swagger:** `swagger_user_iip.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (7 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `base_year` | Yes | string | Yes |  | in baseline |
| `financial_year` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `category_code` |  | string | Yes |  |  |
| `subcategory_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `page` |  | string | Yes |  |  |
| `type` | Yes | string | Yes |  | in baseline |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (3 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **2011-12+All** (base_year=2011-12, type=All): PASS, 10 records, metadata: 4 filters
  - Metadata filters: `financial_year`, `type`, `category`, `subcategory`
- **2011-12+Sectoral** (base_year=2011-12, type=Sectoral): PASS, 10 records, metadata: 4 filters
  - Metadata filters: `financial_year`, `type`, `category`, `subcategory`
- **2004-05+All** (base_year=2004-05, type=All): PASS, 10 records, metadata: 4 filters
  - Metadata filters: `financial_year`, `type`, `category`, `subcategory`

| Parameter | In Swagger | 2011-12+All | 2011-12+Sectoral | 2004-05+All |
|-----------|------------|------|------|------|
| `base_year` | Yes | (baseline) | (baseline) | (baseline) |
| `category_code` | Yes | OK(10) | OK(10) | OK(10) |
| `financial_year` | Yes | OKM(10) | OKM(10) | OKM(10) |
| `page` | Yes | OK(10) | OK(10) | OK(10) |
| `subcategory_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `type` | Yes | (baseline) | (baseline) | (baseline) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **2011-12+All**: Swagger-only (not in metadata): `category_code`, `subcategory_code`
- **2011-12+All**: Metadata-only (not in swagger): `category`, `subcategory`
- **2011-12+Sectoral**: Swagger-only (not in metadata): `category_code`, `subcategory_code`
- **2011-12+Sectoral**: Metadata-only (not in swagger): `category`, `subcategory`
- **2004-05+All**: Swagger-only (not in metadata): `category_code`, `subcategory_code`
- **2004-05+All**: Metadata-only (not in swagger): `category`, `subcategory`

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

No indicator param found

---

## IIP_Monthly

- **Endpoint:** `/api/iip/getIIPMonthly`
- **Swagger:** `swagger_user_iip.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (8 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `base_year` | Yes | string | Yes |  | in baseline |
| `year` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `month_code` |  | string | Yes |  |  |
| `category_code` |  | string | Yes |  |  |
| `subcategory_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `page` |  | string | Yes |  |  |
| `type` | Yes | string | Yes |  | in baseline |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (2 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **2011-12+All** (base_year=2011-12, type=All): PASS, 10 records, metadata: 5 filters
  - Metadata filters: `year`, `month`, `type`, `category`, `subcategory`
- **2011-12+Sectoral** (base_year=2011-12, type=Sectoral): PASS, 10 records, metadata: 5 filters
  - Metadata filters: `year`, `month`, `type`, `category`, `subcategory`

| Parameter | In Swagger | 2011-12+All | 2011-12+Sectoral |
|-----------|------------|------|------|
| `base_year` | Yes | (baseline) | (baseline) |
| `category_code` | Yes | OK(10) | OK(10) |
| `month_code` | Yes | OK(10) | OK(10) |
| `page` | Yes | OK(10) | OK(10) |
| `subcategory_code` | Yes | FILTERS(0) | FILTERS(0) |
| `type` | Yes | (baseline) | (baseline) |
| `year` | Yes | OKM(10) | OKM(10) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **2011-12+All**: Swagger-only (not in metadata): `category_code`, `month_code`, `subcategory_code`
- **2011-12+All**: Metadata-only (not in swagger): `category`, `month`, `subcategory`
- **2011-12+Sectoral**: Swagger-only (not in metadata): `category_code`, `month_code`, `subcategory_code`
- **2011-12+Sectoral**: Metadata-only (not in swagger): `category`, `month`, `subcategory`

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

No indicator param found

---

## ASI

- **Endpoint:** `/api/asi/getASIData`
- **Swagger:** `swagger_user_asi.yaml`
- **Baseline:** FAIL (status=200, records=0)
- **Baseline Error:** 200 OK but 0 records returned

> Baseline failed - param tests skipped.


---

## NAS

- **Endpoint:** `/api/nas/getNASData`
- **Swagger:** `swagger_user_nas.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (13 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `series` | Yes | string | Yes |  | in baseline |
| `frequency_code` | Yes | string | Yes |  | in baseline |
| `indicator_code` | Yes | string | Yes |  | in baseline |
| `quarterly_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `year` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `approach_code` |  | string | Yes |  |  |
| `revision_code` |  | string | Yes |  |  |
| `account_code` |  | string | Yes |  |  |
| `institutional_code` |  | string | Yes |  |  |
| `industry_code` |  | string | Yes |  |  |
| `subindustry_code` |  | string | Yes |  |  |
| `page` |  | string | Yes |  |  |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (4 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **Ind1+Annual+Current** (series=Current, frequency_code=1, indicator_code=1): PASS, 10 records, metadata: 6 filters
  - Metadata filters: `year`, `approach`, `revision`, `industry`, `subindustry`, `institutional_sector`
- **Ind5+Annual+Current** (series=Current, frequency_code=1, indicator_code=5): PASS, 10 records, metadata: 3 filters
  - Metadata filters: `year`, `approach`, `revision`
- **Ind1+Quarterly+Current** (series=Current, frequency_code=2, indicator_code=1): PASS, 10 records, metadata: 3 filters
  - Metadata filters: `year`, `quarterly`, `industry`
- **Ind1+Annual+Back** (series=Back, frequency_code=1, indicator_code=1): PASS, 10 records, metadata: 3 filters
  - Metadata filters: `year`, `industry`, `subindustry`

| Parameter | In Swagger | Ind1+Annual+Current | Ind5+Annual+Current | Ind1+Quarterly+Current | Ind1+Annual+Back |
|-----------|------------|------|------|------|------|
| `account_code` | Yes | OK(10) | OK(10) | OK(10) | OK(10) |
| `approach_code` | Yes | OK(10) | OK(10) | OK(10) | OK(10) |
| `frequency_code` | Yes | (baseline) | (baseline) | (baseline) | (baseline) |
| `indicator_code` | Yes | (baseline) | (baseline) | (baseline) | (baseline) |
| `industry_code` | Yes | OK(10) | FILTERS(0) | OK(10) | OK(10) |
| `institutional_code` | Yes | OK(10) | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `page` | Yes | OK(10) | OK(10) | OK(10) | OK(10) |
| `quarterly_code` | Yes | FILTERS(0) | FILTERS(0) | OK(10) | FILTERS(0) |
| `revision_code` | Yes | OK(10) | OK(10) | FILTERS(0) | FILTERS(0) |
| `series` | Yes | (baseline) | (baseline) | (baseline) | (baseline) |
| `subindustry_code` | Yes | OK(10) | FILTERS(0) | FILTERS(0) | OK(10) |
| `year` | Yes | FILTERSM(9) | FILTERSM(1) | OKM(10) | OKM(10) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **Ind1+Annual+Current**: Swagger-only (not in metadata): `account_code`, `approach_code`, `industry_code`, `institutional_code`, `quarterly_code`, `revision_code`, `subindustry_code`
- **Ind1+Annual+Current**: Metadata-only (not in swagger): `approach`, `industry`, `institutional_sector`, `revision`, `subindustry`
- **Ind5+Annual+Current**: Swagger-only (not in metadata): `account_code`, `approach_code`, `industry_code`, `institutional_code`, `quarterly_code`, `revision_code`, `subindustry_code`
- **Ind5+Annual+Current**: Metadata-only (not in swagger): `approach`, `revision`
- **Ind1+Quarterly+Current**: Swagger-only (not in metadata): `account_code`, `approach_code`, `industry_code`, `institutional_code`, `quarterly_code`, `revision_code`, `subindustry_code`
- **Ind1+Quarterly+Current**: Metadata-only (not in swagger): `industry`, `quarterly`
- **Ind1+Annual+Back**: Swagger-only (not in metadata): `account_code`, `approach_code`, `industry_code`, `institutional_code`, `quarterly_code`, `revision_code`, `subindustry_code`
- **Ind1+Annual+Back**: Metadata-only (not in swagger): `industry`, `subindustry`

**Hierarchy-dependent params** (behave differently across variants):
- `industry_code`: Ind1+Annual+Current: OK(10) [NOT in meta] | Ind5+Annual+Current: filters(0) [NOT in meta] | Ind1+Quarterly+Current: OK(10) [NOT in meta] | Ind1+Annual+Back: OK(10) [NOT in meta]
- `institutional_code`: Ind1+Annual+Current: OK(10) [NOT in meta] | Ind5+Annual+Current: filters(0) [NOT in meta] | Ind1+Quarterly+Current: filters(0) [NOT in meta] | Ind1+Annual+Back: filters(0) [NOT in meta]
- `quarterly_code`: Ind1+Annual+Current: filters(0) [NOT in meta] | Ind5+Annual+Current: filters(0) [NOT in meta] | Ind1+Quarterly+Current: OK(10) [NOT in meta] | Ind1+Annual+Back: filters(0) [NOT in meta]
- `revision_code`: Ind1+Annual+Current: OK(10) [NOT in meta] | Ind5+Annual+Current: OK(10) [NOT in meta] | Ind1+Quarterly+Current: filters(0) [NOT in meta] | Ind1+Annual+Back: filters(0) [NOT in meta]
- `subindustry_code`: Ind1+Annual+Current: OK(10) [NOT in meta] | Ind5+Annual+Current: filters(0) [NOT in meta] | Ind1+Quarterly+Current: filters(0) [NOT in meta] | Ind1+Annual+Back: OK(10) [NOT in meta]
- `year`: Ind1+Annual+Current: filters(9) [in meta] | Ind5+Annual+Current: filters(1) [in meta] | Ind1+Quarterly+Current: OK(10) [in meta] | Ind1+Annual+Back: OK(10) [in meta]

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

Integer indicator only (string 'test_string_name' -> 500: Please check the input parameters passed)

---

## WPI

- **Endpoint:** `/api/wpi/getWpiRecords`
- **Swagger:** `swagger_user_wpi.yaml`
- **Baseline:** PASS (status=200, records=20)

### Swagger Parameters (8 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `Year` |  | string | Yes |  |  |
| `Month_code` |  | string | Yes |  |  |
| `Majorgroup_code` |  | string | Yes |  |  |
| `Group_code` |  | string | Yes |  |  |
| `Subgroup_code` |  | string | Yes |  |  |
| `Sub_subgroup_code` |  | string | Yes |  |  |
| `Item_code` |  | string | Yes |  |  |
| `Format` | Yes | string | Yes |  | in baseline |

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes | Yes | 200 | UNDOCUMENTED - filtered: 20 -> 10 |
| `page` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Case Sensitivity

| Original | Alternative | Original Works | Alt Works | Case Sensitive |
|----------|-------------|----------------|-----------|----------------|
| `Year` | `year` | True | True | False |
| `Month_code` | `month_code` | True | True | False |
| `Majorgroup_code` | `majorgroup_code` | True | True | False |
| `Group_code` | `group_code` | True | True | False |
| `Subgroup_code` | `subgroup_code` | True | True | False |
| `Sub_subgroup_code` | `sub_subgroup_code` | True | True | False |
| `Item_code` | `item_code` | True | True | False |

### Indicator Format

No indicator param found

---

## ENERGY

- **Endpoint:** `/api/energy/getEnergyRecords`
- **Swagger:** `swagger_user_energy.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (9 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `indicator_code` | Yes | string | Yes |  | in baseline |
| `use_of_energy_balance_code` | Yes | string | Yes |  | in baseline |
| `year` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `energy_commodities_code` |  | string | Yes |  |  |
| `energy_sub_commodities_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `end_use_sector_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `end_use_sub_sector_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `page` |  | string | Yes |  |  |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (3 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **KToE+Supply** (indicator_code=1, use_of_energy_balance_code=1): PASS, 10 records, metadata: 3 filters
  - Metadata filters: `year`, `energy_commodities`, `end_use_sector`
- **KToE+Consumption** (indicator_code=1, use_of_energy_balance_code=2): PASS, 10 records, metadata: 5 filters
  - Metadata filters: `year`, `energy_commodities`, `energy_sub_commodities`, `end_use_sector`, `end_use_sub_sector`
- **PJ+Supply** (indicator_code=2, use_of_energy_balance_code=1): PASS, 10 records, metadata: 3 filters
  - Metadata filters: `year`, `energy_commodities`, `end_use_sector`

| Parameter | In Swagger | KToE+Supply | KToE+Consumption | PJ+Supply |
|-----------|------------|------|------|------|
| `end_use_sector_code` | Yes | FILTERS(0) | OK(10) | FILTERS(0) |
| `end_use_sub_sector_code` | Yes | FILTERS(0) | OK(10) | FILTERS(0) |
| `energy_commodities_code` | Yes | OK(10) | OK(10) | OK(10) |
| `energy_sub_commodities_code` | Yes | FILTERS(0) | OK(10) | FILTERS(0) |
| `indicator_code` | Yes | (baseline) | (baseline) | (baseline) |
| `page` | Yes | OK(10) | OK(10) | OK(10) |
| `use_of_energy_balance_code` | Yes | (baseline) | (baseline) | (baseline) |
| `year` | Yes | OKM(10) | OKM(10) | OKM(10) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **KToE+Supply**: Swagger-only (not in metadata): `end_use_sector_code`, `end_use_sub_sector_code`, `energy_commodities_code`, `energy_sub_commodities_code`
- **KToE+Supply**: Metadata-only (not in swagger): `end_use_sector`, `energy_commodities`
- **KToE+Consumption**: Swagger-only (not in metadata): `end_use_sector_code`, `end_use_sub_sector_code`, `energy_commodities_code`, `energy_sub_commodities_code`
- **KToE+Consumption**: Metadata-only (not in swagger): `end_use_sector`, `end_use_sub_sector`, `energy_commodities`, `energy_sub_commodities`
- **PJ+Supply**: Swagger-only (not in metadata): `end_use_sector_code`, `end_use_sub_sector_code`, `energy_commodities_code`, `energy_sub_commodities_code`
- **PJ+Supply**: Metadata-only (not in swagger): `end_use_sector`, `energy_commodities`

**Hierarchy-dependent params** (behave differently across variants):
- `end_use_sector_code`: KToE+Supply: filters(0) [NOT in meta] | KToE+Consumption: OK(10) [NOT in meta] | PJ+Supply: filters(0) [NOT in meta]
- `end_use_sub_sector_code`: KToE+Supply: filters(0) [NOT in meta] | KToE+Consumption: OK(10) [NOT in meta] | PJ+Supply: filters(0) [NOT in meta]
- `energy_sub_commodities_code`: KToE+Supply: filters(0) [NOT in meta] | KToE+Consumption: OK(10) [NOT in meta] | PJ+Supply: filters(0) [NOT in meta]

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

String enum 'Energy Balance ( in KToE )' -> status=200, records=10 | Integer '1' -> status=200, records=10 | BOTH formats accepted

---

## HCES

- **Endpoint:** `/api/hces/getHcesRecords`
- **Swagger:** `swagger_user_hces.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (13 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `indicator_code` | Yes | string | Yes |  | in baseline |
| `year` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sub_indicator_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `state_code` |  | string | Yes | Yes | filtered: 10 -> 8 |
| `sector_code` |  | string | Yes |  |  |
| `imputation_type_code` |  | string | Yes |  |  |
| `mpce_fractile_classes_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `item_category_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `cereal_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `employment_of_households_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `social_group_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `page` |  | string | Yes |  |  |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (3 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **MPCE** (indicator_code=Average monthly per capita consumption expenditure (MPCE)): PASS, 10 records, metadata: FAILED
- **MPCE Fractile** (indicator_code=Average monthly per capita consumption expenditure (MPCE) Over 12 Fractile Classes): PASS, 10 records, metadata: FAILED
- **Quantity** (indicator_code=Average Per Capita Monthly Quantity Consumption ): PASS, 10 records, metadata: FAILED

| Parameter | In Swagger | MPCE | MPCE Fractile | Quantity |
|-----------|------------|------|------|------|
| `cereal_code` | Yes | FILTERS(0) | FILTERS(0) | OK(10) |
| `employment_of_households_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `imputation_type_code` | Yes | OK(10) | OK(10) | OK(10) |
| `indicator_code` | Yes | (baseline) | (baseline) | (baseline) |
| `item_category_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `mpce_fractile_classes_code` | Yes | FILTERS(0) | OK(10) | FILTERS(0) |
| `page` | Yes | OK(10) | OK(10) | OK(10) |
| `sector_code` | Yes | OK(10) | OK(10) | OK(10) |
| `social_group_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `state_code` | Yes | FILTERS(8) | OK(10) | OK(10) |
| `sub_indicator_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `year` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**


**Hierarchy-dependent params** (behave differently across variants):
- `cereal_code`: MPCE: filters(0) [NOT in meta] | MPCE Fractile: filters(0) [NOT in meta] | Quantity: OK(10) [NOT in meta]
- `mpce_fractile_classes_code`: MPCE: filters(0) [NOT in meta] | MPCE Fractile: OK(10) [NOT in meta] | Quantity: filters(0) [NOT in meta]
- `state_code`: MPCE: filters(8) [NOT in meta] | MPCE Fractile: OK(10) [NOT in meta] | Quantity: OK(10) [NOT in meta]

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

String enum 'Average monthly per capita consumption expenditure (MPCE)' -> status=200, records=10 | Integer '1' -> status=200, records=10 | BOTH formats accepted

---

## NSS78

- **Endpoint:** `/api/nss-78/getNss78Records`
- **Swagger:** `swagger_user_nss78.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (11 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `Indicator` | Yes | string | Yes |  | in baseline |
| `State_code` |  | string | Yes |  |  |
| `Sector_code` |  | string | Yes |  |  |
| `Gender_code` |  | string | Yes |  |  |
| `AgeGroup_code` |  | string | Yes |  |  |
| `InternetAccess_code` |  | string | Yes |  |  |
| `Household_LeavingReason_code` |  | string | Yes |  |  |
| `Subindicator_code` |  | string | Yes |  |  |
| `Households_code` |  | string | No |  |  |
| `SourceOfFinance_code` |  | string | Yes |  |  |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (3 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **Mobile Phone** (Indicator=Usage of Mobile Phone, indicator_code=2): PASS, 10 records, metadata: 3 filters
  - Metadata filters: `sub_indicator`, `state`, `sector`
- **Mass Media** (Indicator=Access to Mass Media and Broadband, indicator_code=3): PASS, 10 records, metadata: 3 filters
  - Metadata filters: `sub_indicator`, `state`, `sector`
- **Migration** (Indicator=Main Reason for Leaving Last Usaul Place of Residence, indicator_code=12): PASS, 10 records, metadata: 4 filters
  - Metadata filters: `state`, `sector`, `gender`, `reason_leaving_household`

| Parameter | In Swagger | Mobile Phone | Mass Media | Migration |
|-----------|------------|------|------|------|
| `AgeGroup_code` | Yes | OK(10) | OK(10) | OK(10) |
| `Gender_code` | Yes | FAIL | FAIL | OK(10) |
| `Household_LeavingReason_code` | Yes | OK(10) | OK(10) | OK(10) |
| `Households_code` | Yes | FAIL | FAIL | FAIL |
| `Indicator` | Yes | (baseline) | (baseline) | (baseline) |
| `InternetAccess_code` | Yes | OK(10) | OK(10) | OK(10) |
| `Sector_code` | Yes | OK(10) | OK(10) | OK(10) |
| `SourceOfFinance_code` | Yes | OK(10) | OK(10) | OK(10) |
| `State_code` | Yes | FILTERS(6) | OK(10) | OK(10) |
| `Subindicator_code` | Yes | OK(10) | OK(10) | OK(10) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **Mobile Phone**: Swagger-only (not in metadata): `AgeGroup_code`, `Gender_code`, `Household_LeavingReason_code`, `Households_code`, `InternetAccess_code`, `Sector_code`, `SourceOfFinance_code`, `State_code`, `Subindicator_code`
- **Mobile Phone**: Metadata-only (not in swagger): `sector`, `state`, `sub_indicator`
- **Mass Media**: Swagger-only (not in metadata): `AgeGroup_code`, `Gender_code`, `Household_LeavingReason_code`, `Households_code`, `InternetAccess_code`, `Sector_code`, `SourceOfFinance_code`, `State_code`, `Subindicator_code`
- **Mass Media**: Metadata-only (not in swagger): `sector`, `state`, `sub_indicator`
- **Migration**: Swagger-only (not in metadata): `AgeGroup_code`, `Gender_code`, `Household_LeavingReason_code`, `Households_code`, `InternetAccess_code`, `Sector_code`, `SourceOfFinance_code`, `State_code`, `Subindicator_code`
- **Migration**: Metadata-only (not in swagger): `gender`, `reason_leaving_household`, `sector`, `state`

**Hierarchy-dependent params** (behave differently across variants):
- `Gender_code`: Mobile Phone: FAIL [NOT in meta] | Mass Media: FAIL [NOT in meta] | Migration: OK(10) [NOT in meta]
- `State_code`: Mobile Phone: filters(6) [NOT in meta] | Mass Media: OK(10) [NOT in meta] | Migration: OK(10) [NOT in meta]

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `page` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Case Sensitivity

| Original | Alternative | Original Works | Alt Works | Case Sensitive |
|----------|-------------|----------------|-----------|----------------|
| `Indicator` | `indicator` | True | True | False |
| `State_code` | `state_code` | True | True | False |
| `Sector_code` | `sector_code` | True | True | False |
| `Gender_code` | `gender_code` | True | True | False |
| `AgeGroup_code` | `agegroup_code` | True | True | False |
| `InternetAccess_code` | `internetaccess_code` | True | True | False |
| `Household_LeavingReason_code` | `household_leavingreason_code` | True | True | False |
| `Subindicator_code` | `subindicator_code` | True | True | False |
| `Households_code` | `households_code` | False | False | True |
| `SourceOfFinance_code` | `sourceoffinance_code` | True | True | False |

### Indicator Format

String enum 'Usage of Mobile Phone' -> status=200, records=10 | Integer '1' -> status=500, records=0 | Integer rejected: {'success': False, 'error': 'Database error'}

---

## NFHS

- **Endpoint:** `/api/nfhs/getNfhsRecords`
- **Swagger:** `swagger_user_nfhs.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (7 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `indicator_code` | Yes | integer | Yes |  | in baseline |
| `sub_indicator_code` |  | string | Yes |  |  |
| `state_code` |  | integer | Yes |  |  |
| `survey_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `limit` |  | integer | Yes | Yes | filtered: 10 -> 20 |
| `page` |  | integer | Yes |  |  |
| `format` |  | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (3 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **Indicator 1** (indicator_code=1): PASS, 10 records, metadata: 4 filters
  - Metadata filters: `state`, `sub_indicator`, `sector`, `survey`
- **Indicator 2** (indicator_code=2): PASS, 10 records, metadata: 4 filters
  - Metadata filters: `state`, `sub_indicator`, `sector`, `survey`
- **Indicator 5** (indicator_code=5): PASS, 10 records, metadata: 4 filters
  - Metadata filters: `state`, `sub_indicator`, `sector`, `survey`

| Parameter | In Swagger | Indicator 1 | Indicator 2 | Indicator 5 |
|-----------|------------|------|------|------|
| `indicator_code` | Yes | (baseline) | (baseline) | (baseline) |
| `limit` | Yes | FILTERS(20) | FILTERS(20) | FILTERS(20) |
| `page` | Yes | OK(10) | OK(10) | OK(10) |
| `state_code` | Yes | OK(10) | OK(10) | OK(10) |
| `sub_indicator_code` | Yes | OK(10) | FILTERS(0) | FILTERS(0) |
| `survey_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **Indicator 1**: Swagger-only (not in metadata): `state_code`, `sub_indicator_code`, `survey_code`
- **Indicator 1**: Metadata-only (not in swagger): `sector`, `state`, `sub_indicator`, `survey`
- **Indicator 2**: Swagger-only (not in metadata): `state_code`, `sub_indicator_code`, `survey_code`
- **Indicator 2**: Metadata-only (not in swagger): `sector`, `state`, `sub_indicator`, `survey`
- **Indicator 5**: Swagger-only (not in metadata): `state_code`, `sub_indicator_code`, `survey_code`
- **Indicator 5**: Metadata-only (not in swagger): `sector`, `state`, `sub_indicator`, `survey`

**Hierarchy-dependent params** (behave differently across variants):
- `sub_indicator_code`: Indicator 1: OK(10) [NOT in meta] | Indicator 2: filters(0) [NOT in meta] | Indicator 5: filters(0) [NOT in meta]

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `Format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

Integer indicator only (string 'test_string_name' -> 500: internal server error)

---

## ASUSE

- **Endpoint:** `/api/asuse/getAsuseRecords`
- **Swagger:** `swagger_user_asuse.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (32 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `indicator_code` | Yes | integer | Yes |  | in baseline |
| `year` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `state_ut_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `sub_indicator_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `activity_category_code` |  | integer | Yes |  |  |
| `sector_code` |  | integer | Yes |  |  |
| `gender_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `ownership_type_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `establishment_type_code` |  | integer | Yes |  |  |
| `general_education_level_code` |  | integer | Yes |  |  |
| `social_group_of_owner_major_partner_code` |  | integer | Yes |  |  |
| `broad_activity_category_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `other_economic_activitycount_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `account_holder_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `location_of_establishments_code` |  | integer | Yes |  |  |
| `nature_of_operation_code` |  | integer | Yes |  |  |
| `no_of_months_operated_code` |  | integer | Yes |  |  |
| `no_of_working_hours_code` |  | integer | Yes |  |  |
| `audit_status_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `npi_status_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `acts_agency_of_registration_code` |  | integer | Yes |  |  |
| `services_contract_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `nature_of_employment_code` |  | integer | Yes |  |  |
| `type_of_worker_code` |  | integer | Yes |  |  |
| `hired_worker_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `fixed_assets_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `usage_of_internet_code` |  | integer | Yes |  |  |
| `worker_characteristics_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `worker_number_code` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `frequency_code` |  | integer | Yes |  |  |
| `page` |  | integer | Yes |  |  |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (2 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **Indicator 1** (indicator_code=1): PASS, 10 records, metadata: 4 filters
  - Metadata filters: `year`, `sector`, `activity`, `establishment_type`
- **Indicator 2** (indicator_code=2): PASS, 10 records, metadata: 5 filters
  - Metadata filters: `year`, `state`, `sector`, `establishment_type`, `broad_activity_category`

| Parameter | In Swagger | Indicator 1 | Indicator 2 |
|-----------|------------|------|------|
| `account_holder_code` | Yes | FILTERS(0) | FILTERS(0) |
| `activity_category_code` | Yes | OK(10) | FILTERS(0) |
| `acts_agency_of_registration_code` | Yes | OK(10) | OK(10) |
| `audit_status_code` | Yes | FILTERS(0) | FILTERS(0) |
| `broad_activity_category_code` | Yes | FILTERS(0) | OK(10) |
| `establishment_type_code` | Yes | OK(10) | OK(10) |
| `fixed_assets_code` | Yes | FILTERS(0) | FILTERS(0) |
| `frequency_code` | Yes | OK(10) | OK(10) |
| `gender_code` | Yes | FILTERS(0) | FILTERS(0) |
| `general_education_level_code` | Yes | OK(10) | OK(10) |
| `hired_worker_code` | Yes | FILTERS(0) | FILTERS(0) |
| `indicator_code` | Yes | (baseline) | (baseline) |
| `location_of_establishments_code` | Yes | OK(10) | OK(10) |
| `nature_of_employment_code` | Yes | OK(10) | OK(10) |
| `nature_of_operation_code` | Yes | OK(10) | OK(10) |
| `no_of_months_operated_code` | Yes | OK(10) | OK(10) |
| `no_of_working_hours_code` | Yes | OK(10) | OK(10) |
| `npi_status_code` | Yes | FILTERS(0) | FILTERS(0) |
| `other_economic_activitycount_code` | Yes | FILTERS(0) | FILTERS(0) |
| `ownership_type_code` | Yes | FILTERS(0) | FILTERS(0) |
| `page` | Yes | OK(10) | OK(10) |
| `sector_code` | Yes | OK(10) | OK(10) |
| `services_contract_code` | Yes | FILTERS(0) | FILTERS(0) |
| `social_group_of_owner_major_partner_code` | Yes | OK(10) | OK(10) |
| `state_ut_code` | Yes | FILTERS(0) | OK(10) |
| `sub_indicator_code` | Yes | FILTERS(0) | FILTERS(0) |
| `type_of_worker_code` | Yes | OK(10) | OK(10) |
| `usage_of_internet_code` | Yes | OK(10) | OK(10) |
| `worker_characteristics_code` | Yes | FILTERS(0) | FILTERS(0) |
| `worker_number_code` | Yes | FILTERS(0) | FILTERS(0) |
| `year` | Yes | OKM(10) | OKM(10) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **Indicator 1**: Swagger-only (not in metadata): `account_holder_code`, `activity_category_code`, `acts_agency_of_registration_code`, `audit_status_code`, `broad_activity_category_code`, `establishment_type_code`, `fixed_assets_code`, `frequency_code`, `gender_code`, `general_education_level_code`, `hired_worker_code`, `location_of_establishments_code`, `nature_of_employment_code`, `nature_of_operation_code`, `no_of_months_operated_code`, `no_of_working_hours_code`, `npi_status_code`, `other_economic_activitycount_code`, `ownership_type_code`, `sector_code`, `services_contract_code`, `social_group_of_owner_major_partner_code`, `state_ut_code`, `sub_indicator_code`, `type_of_worker_code`, `usage_of_internet_code`, `worker_characteristics_code`, `worker_number_code`
- **Indicator 1**: Metadata-only (not in swagger): `activity`, `establishment_type`, `sector`
- **Indicator 2**: Swagger-only (not in metadata): `account_holder_code`, `activity_category_code`, `acts_agency_of_registration_code`, `audit_status_code`, `broad_activity_category_code`, `establishment_type_code`, `fixed_assets_code`, `frequency_code`, `gender_code`, `general_education_level_code`, `hired_worker_code`, `location_of_establishments_code`, `nature_of_employment_code`, `nature_of_operation_code`, `no_of_months_operated_code`, `no_of_working_hours_code`, `npi_status_code`, `other_economic_activitycount_code`, `ownership_type_code`, `sector_code`, `services_contract_code`, `social_group_of_owner_major_partner_code`, `state_ut_code`, `sub_indicator_code`, `type_of_worker_code`, `usage_of_internet_code`, `worker_characteristics_code`, `worker_number_code`
- **Indicator 2**: Metadata-only (not in swagger): `broad_activity_category`, `establishment_type`, `sector`, `state`

**Hierarchy-dependent params** (behave differently across variants):
- `activity_category_code`: Indicator 1: OK(10) [NOT in meta] | Indicator 2: filters(0) [NOT in meta]
- `broad_activity_category_code`: Indicator 1: filters(0) [NOT in meta] | Indicator 2: OK(10) [NOT in meta]
- `state_ut_code`: Indicator 1: filters(0) [NOT in meta] | Indicator 2: OK(10) [NOT in meta]

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

Integer indicator only (string 'test_string_name' -> 500: {'error': 'Please check the input parameters passed'})

---

## TUS

- **Endpoint:** `/api/tus/getTusRecords`
- **Swagger:** `swagger_user_tus.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (22 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `indicator_code` | Yes | string | Yes |  | in baseline |
| `year` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sub_indicator_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `state_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sector_code` |  | string | Yes |  |  |
| `gender_code` |  | string | Yes |  |  |
| `day_of_week_code` |  | string | Yes |  |  |
| `household_member_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `age_group_code` |  | string | Yes |  |  |
| `icatus_activity_code` |  | string | Yes |  |  |
| `activity_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `usual_principal_activity_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `broad_principal_activity_status_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `place_of_activity_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sna_activity_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `marital_status_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `quintile_class_of_umpce_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `level_of_education_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `employment_status_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `social_group_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `page` |  | string | Yes |  |  |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (2 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **Activity %** (indicator_code=Percentage of persons in different activity in a day as major activity (age 6 years and above)): PASS, 10 records, metadata: FAILED
- **Activity mins** (indicator_code=Minutes spent in different activity in a day as major activity (age 6 years and above)): FAIL (0), 0 records, metadata: FAILED

| Parameter | In Swagger | Activity % | Activity mins |
|-----------|------------|------|------|
| `activity_code` | Yes | FILTERS(0) | N/A |
| `age_group_code` | Yes | OK(10) | N/A |
| `broad_principal_activity_status_code` | Yes | FILTERS(0) | N/A |
| `day_of_week_code` | Yes | OK(10) | N/A |
| `employment_status_code` | Yes | FILTERS(0) | N/A |
| `gender_code` | Yes | OK(10) | N/A |
| `household_member_code` | Yes | FILTERS(0) | N/A |
| `icatus_activity_code` | Yes | OK(10) | N/A |
| `indicator_code` | Yes | (baseline) | N/A |
| `level_of_education_code` | Yes | FILTERS(0) | N/A |
| `marital_status_code` | Yes | FILTERS(0) | N/A |
| `page` | Yes | OK(10) | N/A |
| `place_of_activity_code` | Yes | FILTERS(0) | N/A |
| `quintile_class_of_umpce_code` | Yes | FILTERS(0) | N/A |
| `sector_code` | Yes | OK(10) | N/A |
| `sna_activity_code` | Yes | FILTERS(0) | N/A |
| `social_group_code` | Yes | FILTERS(0) | N/A |
| `state_code` | Yes | FILTERS(0) | N/A |
| `sub_indicator_code` | Yes | FILTERS(0) | N/A |
| `usual_principal_activity_code` | Yes | FILTERS(0) | N/A |
| `year` | Yes | FILTERS(0) | N/A |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**


### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

String enum 'Percentage of persons in different activity in a day as major activity (age 6 years and above)' -> status=200, records=10 | Integer '1' -> status=0, records=0 | Integer rejected: Request timed out

---

## GENDER

- **Endpoint:** `/api/gender/getGenderRecords`
- **Swagger:** `swagger_user_gender.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (31 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `indicator_code` | Yes | string | Yes |  | in baseline |
| `year` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `quarter_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sub_indicator_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `state_ut_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sector_code` |  | string | Yes |  |  |
| `gender_code` |  | string | Yes |  |  |
| `age_group_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `birth_order_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `education_level_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `survey_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `family_planning_method_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `ayush_category_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `discipline_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `nco_division_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `employment_category_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `industry_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `bank_group_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `activity_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `broad_activity_category_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `type_of_establishment_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `deposit_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `scheme_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `lok_sabha_election_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `police_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `court_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `service_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `crime_head_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `category_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `page` |  | string | Yes |  |  |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (3 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **Population** (indicator_code=Trend in Population): PASS, 10 records, metadata: FAILED
- **Sex Ratio** (indicator_code=Sex Ratio): PASS, 10 records, metadata: FAILED
- **LFPR** (indicator_code=Labour Force Participation Rate (LFPR) (in percent) in usual status (ps+ss)): PASS, 10 records, metadata: FAILED

| Parameter | In Swagger | Population | Sex Ratio | LFPR |
|-----------|------------|------|------|------|
| `activity_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `age_group_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `ayush_category_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `bank_group_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `birth_order_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `broad_activity_category_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `category_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `court_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `crime_head_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `deposit_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `discipline_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `education_level_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `employment_category_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `family_planning_method_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `gender_code` | Yes | OK(10) | FILTERS(0) | OK(10) |
| `indicator_code` | Yes | (baseline) | (baseline) | (baseline) |
| `industry_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `lok_sabha_election_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `nco_division_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `page` | Yes | OK(10) | OK(10) | OK(10) |
| `police_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `quarter_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `scheme_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `sector_code` | Yes | OK(10) | FILTERS(0) | OK(10) |
| `service_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `state_ut_code` | Yes | FILTERS(0) | FILTERS(7) | FILTERS(0) |
| `sub_indicator_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `survey_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `type_of_establishment_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `year` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**


**Hierarchy-dependent params** (behave differently across variants):
- `gender_code`: Population: OK(10) [NOT in meta] | Sex Ratio: filters(0) [NOT in meta] | LFPR: OK(10) [NOT in meta]
- `sector_code`: Population: OK(10) [NOT in meta] | Sex Ratio: filters(0) [NOT in meta] | LFPR: OK(10) [NOT in meta]
- `state_ut_code`: Population: filters(0) [NOT in meta] | Sex Ratio: filters(7) [NOT in meta] | LFPR: filters(0) [NOT in meta]

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

String enum 'Trend in Population' -> status=200, records=10 | Integer '1' -> status=200, records=10 | BOTH formats accepted

---

## RBI

- **Endpoint:** `/api/rbi/getRbiRecords`
- **Swagger:** `swagger_user_rbi.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (5 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `sub_indicator_code` | Yes | integer | Yes |  | in baseline |
| `year` |  | integer | Yes | Yes | filtered: 10 -> 0 |
| `limit` |  | integer | Yes | Yes | filtered: 10 -> 20 |
| `page` |  | integer | Yes |  |  |
| `format` |  | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (2 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **SubInd 1** (sub_indicator_code=1): PASS, 10 records, metadata: 0 filters
- **SubInd 5** (sub_indicator_code=5): PASS, 10 records, metadata: 0 filters

| Parameter | In Swagger | SubInd 1 | SubInd 5 |
|-----------|------------|------|------|
| `limit` | Yes | FILTERS(20) | FILTERS(20) |
| `page` | Yes | OK(10) | OK(10) |
| `sub_indicator_code` | Yes | (baseline) | (baseline) |
| `year` | Yes | FILTERS(0) | FILTERS(0) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **SubInd 1**: Swagger-only (not in metadata): `year`
- **SubInd 5**: Swagger-only (not in metadata): `year`

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `Format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

Integer indicator only (string 'test_string_name' -> 400: sub_indicator_code is required)

---

## ENVSTATS

- **Endpoint:** `/api/env/getEnvStatsRecords`
- **Swagger:** `swagger_user_envstats.yaml`
- **Baseline:** PASS (status=200, records=120)

### Swagger Parameters (13 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `indicator_code` | Yes | integer | Yes |  | in baseline |
| `year` |  | string | Yes | Yes | filtered: 120 -> 0 |
| `month_code` |  | integer | Yes | Yes | filtered: 120 -> 0 |
| `quarter_code` |  | integer | Yes | Yes | filtered: 120 -> 24 |
| `state_code` |  | integer | Yes | Yes | filtered: 120 -> 0 |
| `region_code` |  | integer | Yes | Yes | filtered: 120 -> 0 |
| `sector_code` |  | integer | Yes | Yes | filtered: 120 -> 0 |
| `sub_indicator_code` |  | integer | Yes | Yes | filtered: 120 -> 0 |
| `livestock_marine_products_code` |  | integer | Yes | Yes | filtered: 120 -> 0 |
| `wetland_type_area_code` |  | integer | Yes | Yes | filtered: 120 -> 0 |
| `limit` |  | integer | Yes | Yes | filtered: 120 -> 20 |
| `page` |  | integer | Yes |  |  |
| `format` |  | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (3 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **Indicator 1** (indicator_code=1): PASS, 120 records, metadata: 2 filters
  - Metadata filters: `year`, `period`
- **Indicator 5** (indicator_code=5): PASS, 222 records, metadata: 2 filters
  - Metadata filters: `state`, `sub_indicator`
- **Indicator 10** (indicator_code=10): PASS, 703 records, metadata: 4 filters
  - Metadata filters: `year`, `state`, `sub_indicator`, `land_degradation`

| Parameter | In Swagger | Indicator 1 | Indicator 5 | Indicator 10 |
|-----------|------------|------|------|------|
| `indicator_code` | Yes | (baseline) | (baseline) | (baseline) |
| `limit` | Yes | FILTERS(20) | FILTERS(20) | FILTERS(20) |
| `livestock_marine_products_code` | Yes | FAIL | FILTERS(0) | FILTERS(0) |
| `month_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `page` | Yes | OK(120) | OK(222) | OK(703) |
| `quarter_code` | Yes | FILTERS(24) | FILTERS(0) | FILTERS(0) |
| `region_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `sector_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `state_code` | Yes | FILTERS(0) | FILTERS(6) | FILTERS(19) |
| `sub_indicator_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `wetland_type_area_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `year` | Yes | FILTERSM(5) | FILTERS(0) | FILTERSM(333) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **Indicator 1**: Swagger-only (not in metadata): `livestock_marine_products_code`, `month_code`, `quarter_code`, `region_code`, `sector_code`, `state_code`, `sub_indicator_code`, `wetland_type_area_code`
- **Indicator 1**: Metadata-only (not in swagger): `period`
- **Indicator 5**: Swagger-only (not in metadata): `livestock_marine_products_code`, `month_code`, `quarter_code`, `region_code`, `sector_code`, `state_code`, `sub_indicator_code`, `wetland_type_area_code`, `year`
- **Indicator 5**: Metadata-only (not in swagger): `state`, `sub_indicator`
- **Indicator 10**: Swagger-only (not in metadata): `livestock_marine_products_code`, `month_code`, `quarter_code`, `region_code`, `sector_code`, `state_code`, `sub_indicator_code`, `wetland_type_area_code`
- **Indicator 10**: Metadata-only (not in swagger): `land_degradation`, `state`, `sub_indicator`

**Hierarchy-dependent params** (behave differently across variants):
- `livestock_marine_products_code`: Indicator 1: FAIL [NOT in meta] | Indicator 5: filters(0) [NOT in meta] | Indicator 10: filters(0) [NOT in meta]
- `page`: Indicator 1: OK(120) [NOT in meta] | Indicator 5: OK(222) [NOT in meta] | Indicator 10: OK(703) [NOT in meta]
- `quarter_code`: Indicator 1: filters(24) [NOT in meta] | Indicator 5: filters(0) [NOT in meta] | Indicator 10: filters(0) [NOT in meta]
- `state_code`: Indicator 1: filters(0) [NOT in meta] | Indicator 5: filters(6) [NOT in meta] | Indicator 10: filters(19) [NOT in meta]
- `year`: Indicator 1: filters(5) [in meta] | Indicator 5: filters(0) [NOT in meta] | Indicator 10: filters(333) [in meta]

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `Format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

Integer indicator only (string 'test_string_name' -> 400: {'error': 'indicator_code is required (integer)'})

---

## AISHE

- **Endpoint:** `/api/aishe/getAisheRecords`
- **Swagger:** `swagger_user_aishe.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (4 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `indicator_code` | Yes | integer | Yes |  | in baseline |
| `limit` |  | integer | Yes | Yes | filtered: 10 -> 20 |
| `page` |  | integer | Yes |  |  |
| `format` |  | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (2 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **Indicator 1** (indicator_code=1): PASS, 10 records, metadata: 2 filters
  - Metadata filters: `year`, `state`
- **Indicator 3** (indicator_code=3): PASS, 10 records, metadata: 4 filters
  - Metadata filters: `year`, `state`, `education_level`, `gender`

| Parameter | In Swagger | Indicator 1 | Indicator 3 |
|-----------|------------|------|------|
| `indicator_code` | Yes | (baseline) | (baseline) |
| `limit` | Yes | FILTERS(20) | FILTERS(20) |
| `page` | Yes | OK(10) | OK(10) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**

- **Indicator 1**: Metadata-only (not in swagger): `state`, `year`
- **Indicator 3**: Metadata-only (not in swagger): `education_level`, `gender`, `state`, `year`

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `Format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

Integer indicator only (string 'test_string_name' -> 400: indicator_code is required and must be an integer)

---

## CPIALRL

- **Endpoint:** `/api/cpialrl/getCpialrlRecords`
- **Swagger:** `swagger_user_cpialrl.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (8 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `indicator_code` | Yes | string | Yes |  | in baseline |
| `base_year_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `year` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `month_code` |  | string | Yes |  |  |
| `state_code` |  | string | Yes |  |  |
| `groups_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `page` |  | string | Yes |  |  |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (2 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **General Index** (indicator_code=General Index): PASS, 10 records, metadata: FAILED
- **Group Index** (indicator_code=Group Index): PASS, 10 records, metadata: FAILED

| Parameter | In Swagger | General Index | Group Index |
|-----------|------------|------|------|
| `base_year_code` | Yes | FILTERS(0) | FILTERS(0) |
| `groups_code` | Yes | FILTERS(0) | OK(10) |
| `indicator_code` | Yes | (baseline) | (baseline) |
| `month_code` | Yes | OK(10) | OK(10) |
| `page` | Yes | OK(10) | OK(10) |
| `state_code` | Yes | OK(10) | OK(10) |
| `year` | Yes | FILTERS(0) | FILTERS(0) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**


**Hierarchy-dependent params** (behave differently across variants):
- `groups_code`: General Index: filters(0) [NOT in meta] | Group Index: OK(10) [NOT in meta]

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

String enum 'General Index' -> status=200, records=10 | Integer '1' -> status=200, records=10 | BOTH formats accepted

---

## NSS77

- **Endpoint:** `/api/nss-77/getNss77Records`
- **Swagger:** `swagger_user_nss77.yaml`
- **Baseline:** PASS (status=200, records=10)

### Swagger Parameters (54 total)

| Parameter | Required | Type | Accepted | Filters | Notes |
|-----------|----------|------|----------|---------|-------|
| `indicator_code` | Yes | string | Yes |  | in baseline |
| `state_code` |  | string | Yes |  |  |
| `gender_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `visit_code` |  | string | Yes |  |  |
| `land_possessed_hosehold_code` |  | string | Yes |  |  |
| `agricultural_household_code` |  | string | Yes |  |  |
| `caste_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `household_employment_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `household_employment_sub_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `major_disposal_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `agency_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `experienced_crop_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `crop_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sub_experienced_crop_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `operational_holding_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `season_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sub_satisfactory_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `satisfactory_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sub_major_procurement_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `major_procurement_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `resource_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sub_resource_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `agency_procurement_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `seed_procurements_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sub_seed_procurements_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `expenditure_recipt_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `business_type_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `productive_assets_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `expenses_recipt_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `crop_production_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `farming_animals_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `expenses_imputed_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `receipts_type_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `loan_outstanding_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `ownership_holding_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `ownership_holding_area_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `terms_lease_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `livestock_owned_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `stock_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `possession_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `possession_holding_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `harvested_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sub_harvested_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `crop_agency_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `crop_satisfaction_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `crop_procurement_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `crop_insurance_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `crop_experienced_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `quality_seeds_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `insurance_awareness_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `crop_loss_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `msp_awareness_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `sub_indicator_code` |  | string | Yes | Yes | filtered: 10 -> 0 |
| `Format` | Yes | string | Yes |  | in baseline |

### Hierarchy + Metadata Tests (3 variants)

For each variant (indicator + required-param combo), the script calls the 
metadata API to discover which filters are actually available, then tests 
each filter using real values from the metadata response.

**Variant details:**

- **Land Size** (indicator_code=Estimated No. of Hhs for Each Size Class (ha.) of Land Possessed): PASS, 10 records, metadata: FAILED
- **Social Groups** (indicator_code=Estimated No. of Hhs for Different Social Groups): PASS, 10 records, metadata: FAILED
- **Avg Income** (indicator_code=Avg. Monthly Income (in Rs.) Per Agricultural Hh (only the Paid Out Expenditure)): PASS, 10 records, metadata: FAILED

| Parameter | In Swagger | Land Size | Social Groups | Avg Income |
|-----------|------------|------|------|------|
| `agency_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `agency_procurement_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `agricultural_household_code` | Yes | OK(10) | OK(10) | FILTERS(0) |
| `business_type_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `caste_code` | Yes | FILTERS(0) | OK(10) | OK(10) |
| `crop_agency_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `crop_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `crop_experienced_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `crop_insurance_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `crop_loss_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `crop_procurement_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `crop_production_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `crop_satisfaction_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `expenditure_recipt_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `expenses_imputed_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `expenses_recipt_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `experienced_crop_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `farming_animals_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `gender_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `harvested_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `household_employment_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `household_employment_sub_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `indicator_code` | Yes | (baseline) | (baseline) | (baseline) |
| `insurance_awareness_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `land_possessed_hosehold_code` | Yes | OK(10) | FILTERS(0) | OK(10) |
| `livestock_owned_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `loan_outstanding_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `major_disposal_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `major_procurement_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `msp_awareness_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `operational_holding_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `ownership_holding_area_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `ownership_holding_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `possession_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `possession_holding_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `productive_assets_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `quality_seeds_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `receipts_type_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `resource_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `satisfactory_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `season_code` | Yes | FILTERS(0) | FILTERS(0) | OK(10) |
| `seed_procurements_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `state_code` | Yes | OK(10) | OK(10) | OK(10) |
| `stock_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `sub_experienced_crop_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `sub_harvested_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `sub_indicator_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `sub_major_procurement_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `sub_resource_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `sub_satisfactory_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `sub_seed_procurements_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `terms_lease_code` | Yes | FILTERS(0) | FILTERS(0) | FILTERS(0) |
| `visit_code` | Yes | OK(10) | OK(10) | FILTERS(0) |

*M = param was in metadata response for this variant*

**Swagger vs Metadata comparison:**


**Hierarchy-dependent params** (behave differently across variants):
- `agricultural_household_code`: Land Size: OK(10) [NOT in meta] | Social Groups: OK(10) [NOT in meta] | Avg Income: filters(0) [NOT in meta]
- `caste_code`: Land Size: filters(0) [NOT in meta] | Social Groups: OK(10) [NOT in meta] | Avg Income: OK(10) [NOT in meta]
- `land_possessed_hosehold_code`: Land Size: OK(10) [NOT in meta] | Social Groups: filters(0) [NOT in meta] | Avg Income: OK(10) [NOT in meta]
- `season_code`: Land Size: filters(0) [NOT in meta] | Social Groups: filters(0) [NOT in meta] | Avg Income: OK(10) [NOT in meta]
- `visit_code`: Land Size: OK(10) [NOT in meta] | Social Groups: OK(10) [NOT in meta] | Avg Income: filters(0) [NOT in meta]

### Undocumented Parameters

| Parameter | Accepted | Filters | Status | Notes |
|-----------|----------|---------|--------|-------|
| `limit` | Yes |  | 200 | UNDOCUMENTED |
| `page` | Yes |  | 200 | UNDOCUMENTED |
| `format` | Yes |  | 200 | UNDOCUMENTED |

### Indicator Format

String enum 'Estimated No. of Hhs for Each Size Class (ha.) of Land Possessed' -> status=200, records=10 | Integer '1' -> status=200, records=0

---

*Report generated by `test_swagger.py`*