# Adding a New Dataset to MoSPI MCP Server

This guide explains how to add a new dataset to the MoSPI MCP server.

## Architecture Overview

```
mospi_server.py          # 4 generic tools + mappings
    ↓
mospi/client.py          # API methods for each dataset
    ↓
MoSPI API                # https://api.mospi.gov.in
```

## Step 1: Discover the API Endpoints

First, find the API endpoints for your new dataset. MoSPI typically provides:

| Endpoint Type | URL Pattern | Purpose |
|---------------|-------------|---------|
| Indicator List | `/api/{dataset}/get{Dataset}IndicatorList` | List all indicators |
| Filter List | `/api/{dataset}/get{Dataset}FilterByIndicatorId?indicator_code=X` | Get filters for indicator |
| Data | `/api/{dataset}/get{Dataset}Records?...` | Fetch actual data |

**Test the endpoints manually first:**
```bash
# List indicators
curl "https://api.mospi.gov.in/api/newdata/getNewdataIndicatorList"

# Get filters for indicator 1
curl "https://api.mospi.gov.in/api/newdata/getNewdataFilterByIndicatorId?indicator_code=1"

# Fetch data
curl "https://api.mospi.gov.in/api/newdata/getNewdataRecords?indicator_code=1"
```

## Step 2: Add to client.py

### 2.1 Add the data endpoint

In `mospi/client.py`, add your dataset to the `api_endpoints` dict:

```python
self.api_endpoints = {
    # ... existing datasets ...
    "NEWDATA": "/api/newdata/getNewdataRecords",
}
```

### 2.2 Add indicator list method

```python
# =========================================================================
# NEWDATA Methods
# =========================================================================

def get_newdata_indicators(self) -> Dict[str, Any]:
    """Fetch list of NEWDATA indicators from MoSPI API."""
    try:
        response = requests.get(
            f"{self.base_url}/api/newdata/getNewdataIndicatorList",
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "statusCode": False}
```

### 2.3 Add filter/metadata method

```python
def get_newdata_filters(self, indicator_code: int) -> Dict[str, Any]:
    """Fetch available NEWDATA filters for given indicator.

    Args:
        indicator_code: Indicator code from get_newdata_indicators()
    """
    params = {"indicator_code": indicator_code}

    try:
        response = requests.get(
            f"{self.base_url}/api/newdata/getNewdataFilterByIndicatorId",
            params=params,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "statusCode": False}
```

**Note:** Some datasets require additional parameters for filters (see Special Cases below).

## Step 3: Add to mospi_server.py

### 3.1 Add to VALID_DATASETS

```python
VALID_DATASETS = [
    "PLFS", "CPI", "IIP", "ASI", "NAS", "WPI", "ENERGY", "HCES",
    "NSS78", "NSS77", "TUS", "NFHS", "ASUSE", "GENDER", "RBI",
    "ENVSTATS", "AISHE", "CPIALRL", "NEWDATA"  # <-- Add here
]
```

### 3.2 Add to get_indicators()

In the `indicator_methods` dict:

```python
indicator_methods = {
    # ... existing datasets ...
    "NEWDATA": mospi.get_newdata_indicators,
}
```

### 3.3 Add to get_metadata()

Add an `elif` block for your dataset:

```python
elif dataset == "NEWDATA":
    if indicator_code is None:
        return {"error": "indicator_code is required for NEWDATA"}
    return mospi.get_newdata_filters(indicator_code=indicator_code)
```

### 3.4 Add to get_data() dataset_map

```python
dataset_map = {
    # ... existing datasets ...
    "NEWDATA": "NEWDATA",
}
```

### 3.5 Add to know_about_mospi_api()

Add dataset description:

```python
"datasets": {
    # ... existing datasets ...
    "NEWDATA": {
        "name": "Full Name of New Dataset",
        "description": "What this dataset contains, how many indicators, key features",
        "use_for": "What queries this dataset answers"
    }
}
```

Update the `total_datasets` count.

## Step 4: Test

### 4.1 Quick test

```python
# test_newdata.py
from mospi.client import mospi

# Test indicators
print(mospi.get_newdata_indicators())

# Test filters
print(mospi.get_newdata_filters(indicator_code=1))

# Test data
print(mospi.get_data("NEWDATA", {"indicator_code": "1"}))
```

### 4.2 Test via MCP

```bash
python mospi_server.py
# Then test with your MCP client
```

## Special Cases

### Dataset without indicator list (like CPI, IIP, WPI, ASI)

If your dataset doesn't have a traditional indicator list:

**1. Add to special_datasets in get_indicators():**
```python
special_datasets = {
    # ... existing ...
    "NEWDATA": "NEWDATA uses X instead of indicators. Call get_metadata with Y param.",
}
```

**2. Modify get_metadata() to handle different params:**
```python
elif dataset == "NEWDATA":
    return mospi.get_newdata_filters(some_other_param=some_value)
```

### Dataset with extra required parameters

If filters need additional params (like PLFS needs `frequency_code`):

**1. Add optional params to get_metadata() signature if needed**

**2. Handle in the elif block:**
```python
elif dataset == "NEWDATA":
    if indicator_code is None:
        return {"error": "indicator_code is required for NEWDATA"}
    return mospi.get_newdata_filters(
        indicator_code=indicator_code,
        extra_param=extra_param or default_value
    )
```

### Dataset with different response structure

Some datasets return different JSON structures. Document this in:
1. The client.py method docstring
2. The know_about_mospi_api() description

## Checklist

- [ ] Tested API endpoints manually (curl/browser)
- [ ] Added data endpoint to `client.py` → `api_endpoints`
- [ ] Added `get_newdata_indicators()` to `client.py`
- [ ] Added `get_newdata_filters()` to `client.py`
- [ ] Added to `VALID_DATASETS` in `mospi_server.py`
- [ ] Added to `indicator_methods` in `get_indicators()`
- [ ] Added `elif` block in `get_metadata()`
- [ ] Added to `dataset_map` in `get_data()`
- [ ] Added description in `know_about_mospi_api()`
- [ ] Updated `total_datasets` count
- [ ] Tested indicators, metadata, and data fetching
- [ ] Added test file (optional but recommended)

## Example: Adding a Hypothetical "CENSUS" Dataset

```python
# === client.py ===

# In api_endpoints:
"CENSUS": "/api/census/getCensusRecords",

# Methods:
def get_census_indicators(self) -> Dict[str, Any]:
    """Fetch list of CENSUS indicators."""
    try:
        response = requests.get(
            f"{self.base_url}/api/census/getCensusIndicatorList",
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "statusCode": False}

def get_census_filters(self, indicator_code: int) -> Dict[str, Any]:
    """Fetch available CENSUS filters for given indicator."""
    params = {"indicator_code": indicator_code}
    try:
        response = requests.get(
            f"{self.base_url}/api/census/getCensusFilterByIndicatorId",
            params=params,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "statusCode": False}
```

```python
# === mospi_server.py ===

# VALID_DATASETS:
VALID_DATASETS = [..., "CENSUS"]

# get_indicators():
indicator_methods = {
    ...,
    "CENSUS": mospi.get_census_indicators,
}

# get_metadata():
elif dataset == "CENSUS":
    if indicator_code is None:
        return {"error": "indicator_code is required for CENSUS"}
    return mospi.get_census_filters(indicator_code=indicator_code)

# get_data() dataset_map:
dataset_map = {
    ...,
    "CENSUS": "CENSUS",
}

# know_about_mospi_api():
"CENSUS": {
    "name": "Census of India",
    "description": "Population census data - demographics, housing, migration, etc.",
    "use_for": "Population counts, demographic breakdowns, district-level data"
}
```

## Files Reference

| File | What to modify |
|------|----------------|
| `mospi/client.py` | API endpoints + indicator/filter methods |
| `mospi_server.py` | VALID_DATASETS, get_indicators, get_metadata, get_data, know_about_mospi_api |
| `tests/test_newdata.py` | Test file (optional) |
