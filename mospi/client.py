"""
MoSPI API Client
Handles all API calls to the MoSPI data portal
"""

import requests
from typing import Optional, Dict, Any


class MoSPI:
    """
    A unified class to interact with various MoSPI APIs.
    """

    def __init__(self, base_url: str = "https://api.mospi.gov.in"):
        self.base_url = base_url
        self.api_endpoints = {
            "PLFS": "/api/plfs/getData",
            "CPI_Group": "/api/cpi/getCPIIndex",
            "CPI_Item": "/api/cpi/getItemIndex",
            "IIP_Annual": "/api/iip/getIIPAnnual",
            "IIP_Monthly": "/api/iip/getIIPMonthly",
            "ASI": "/api/asi/getASIData",
            "NAS": "/api/nas/getNASData",
            "WPI": "/api/wpi/getWpiRecords",
            "Energy": "/api/energy/getEnergyRecords",
            "AISHE": "/api/aishe/getAisheRecords",
            "ASUSE": "/api/asuse/getAsuseRecords",
            "GENDER": "/api/gender/getGenderRecords",
            "NFHS": "/api/nfhs/getNfhsRecords",
            "ENVSTATS": "/api/env/getEnvStatsRecords",
            "RBI": "/api/rbi/getRbiRecords",
            "NSS77": "/api/nss-77/getNss77Records",
            "NSS78": "/api/nss-78/getNss78Records",
            "CPIALRL": "/api/cpialrl/getCpialrlRecords",
            "HCES": "/api/hces/getHcesRecords",
            "TUS": "/api/tus/getTusRecords",
        }

    def get_data(self, dataset_name: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Fetches data from a specified MoSPI dataset.
        """
        # Clean up params - remove None values
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        # Special handling for CPI with base_year 2024 (unified endpoint)
        if dataset_name in ["CPI_Group", "CPI_Item"] and params and params.get("base_year") == "2024":
            full_url = f"{self.base_url}/api/cpi/getCPIData"
        else:
            endpoint_path = self.api_endpoints.get(dataset_name)
            if not endpoint_path:
                return {"error": f"Dataset '{dataset_name}' not found."}
            full_url = f"{self.base_url}{endpoint_path}"

        try:
            response = requests.get(full_url, params=params, timeout=30)
            response.raise_for_status()

            # Check if CSV format was requested
            format_param = params.get("Format", "JSON") if params else "JSON"
            if format_param == "CSV":
                return {"data": response.text, "format": "CSV"}
            else:
                return response.json()
        except Exception as e:
            return {"error": f"An error occurred: {e}"}

    # =========================================================================
    # PLFS Metadata Methods
    # =========================================================================

    def get_plfs_indicators(self) -> Dict[str, Any]:
        """Fetch PLFS indicators grouped by frequency_code."""
        url = f"{self.base_url}/api/plfs/getIndicatorListByFrequency"
        result = {}
        try:
            for fc, label in [(1, "Annual"), (2, "Quarterly"), (3, "Monthly")]:
                response = requests.get(url, params={"frequency_code": fc}, timeout=30)
                response.raise_for_status()
                data = response.json()
                result[f"frequency_code_{fc}_{label}"] = data.get("data", [])
            return {
                "indicators_by_frequency": result,
                "_note": "frequency_code=1 (Annual) has 8 indicators including all wages. "
                         "It already contains quarterly breakdowns — use quarter_code to filter. "
                         "frequency_code=2 (Quarterly) has 4 indicators for quarterly bulletin tables. "
                         "frequency_code=3 (Monthly) has 3 indicators (2025+ data only). "
                         "Pick the frequency_code whose indicator set matches the query.",
                "statusCode": True,
            }
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_plfs_filters(
        self,
        indicator_code: int,
        frequency_code: int = 1,
        year: Optional[str] = None,
        month_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch available PLFS filters for given indicator/frequency/year/month."""
        params = {
            "indicator_code": indicator_code,
            "frequency_code": frequency_code,
        }
        if year:
            params["year"] = year
        if month_code:
            params["month_code"] = month_code

        try:
            response = requests.get(
                f"{self.base_url}/api/plfs/getFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # CPI Metadata Methods
    # =========================================================================

    def get_cpi_filters(
        self,
        base_year: str = "2024",
        level: str = "Group",
        series_code: str = "Current"
    ) -> Dict[str, Any]:
        """Fetch available CPI filters for given base year and level.

        Args:
            base_year: "2012", "2010", or "2024"
            level: "Group" or "Item" (can be "null" for base_year 2024)
            series_code: "Current" or "Back" (for base_year 2024)
        """
        params = {
            "base_year": base_year,
            "level": level if level else "null",
            "series_code": series_code,
        }

        try:
            response = requests.get(
                f"{self.base_url}/api/cpi/getCpiFilterByLevelAndBaseYear",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_cpi_base_years(self) -> Dict[str, Any]:
        """Fetch available CPI base years and levels.

        Returns:
            Dictionary with available base_year and level options
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/cpi/getCpiBaseYear",
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            # Add guidance about base years
            result["_note"] = (
                "CPI has multiple base years with different data coverage. "
                "DEFAULT to latest base_year (2024) for recent data unless user specifies otherwise. "
                "base_year='2024': Latest data (2026+), new hierarchical structure (division/class/sub_class). "
                "base_year='2012': Data up to 2025. base_year='2010': Historical data. "
                "If data not found in default base year, try others before concluding unavailable."
            )
            return result
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # IIP Metadata Methods
    # =========================================================================

    def get_iip_filters(
        self,
        base_year: str = "2011-12",
        frequency: str = "Annually"
    ) -> Dict[str, Any]:
        """Fetch available IIP filters for given base year and frequency.

        Args:
            base_year: "2011-12", "2004-05", or "1993-94"
            frequency: "Annually" or "Monthly"
        """
        params = {
            "base_year": base_year,
            "frequency": frequency,
        }

        try:
            response = requests.get(
                f"{self.base_url}/api/iip/getIipFilter",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # ASI Metadata Methods
    # =========================================================================

    def get_asi_classification_years(self) -> Dict[str, Any]:
        """Fetch list of available NIC classification years from MoSPI API."""
        try:
            response = requests.get(
                f"{self.base_url}/api/asi/getNicClassificationYear",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_asi_filters(
        self,
        classification_year: str = "2008"
    ) -> Dict[str, Any]:
        """Fetch available ASI filters for given classification year.

        Args:
            classification_year: "2008", "2004", "1998", or "1987"
        """
        params = {
            "classification_year": classification_year,
        }

        try:
            response = requests.get(
                f"{self.base_url}/api/asi/getAsiFilter",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_asi_indicators(self) -> Dict[str, Any]:
        """Fetch ASI indicator list from the filter endpoint (using classification_year=2008).

        Returns indicators plus classification year info so the LLM knows
        it must pass classification_year in get_metadata/get_data.
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/asi/getAsiFilter",
                params={"classification_year": "2008"},
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            filter_data = data.get("data", data)
            # Extract indicator list if present
            indicators = None
            if isinstance(filter_data, dict):
                indicators = filter_data.get("indicator", filter_data.get("indicators", None))
            result = {
                "dataset": "ASI",
                "classification_years": ["2008", "2004", "1998", "1987"],
                "_note": "classification_year is REQUIRED for ASI. It is the NIC classification version, NOT the data year. "
                         "Pick based on which data year you need: "
                         "'1987' → 1992-93 to 1997-98 | "
                         "'1998' → 1998-99 to 2003-04 | "
                         "'2004' → 2004-05 to 2007-08 | "
                         "'2008' → 2008-09 to 2023-24. "
                         "Pass classification_year in 3_get_metadata() and 4_get_data().",
                "statusCode": True,
            }
            if indicators:
                result["indicators"] = indicators
            else:
                result["filters"] = filter_data
            return result
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # NAS Metadata Methods
    # =========================================================================

    def get_nas_indicators(self) -> Dict[str, Any]:
        """Fetch list of all NAS indicators from MoSPI API."""
        try:
            response = requests.get(
                f"{self.base_url}/api/nas/getNasIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            # Add base_year info for consistency with CPI workflow
            if "data" in result and isinstance(result["data"], dict):
                result["data"]["base_year"] = [
                    {"base_year": "2022-23"},
                    {"base_year": "2011-12"},
                ]
            result["_note"] = (
                "NAS requires base_year in 3_get_metadata and 4_get_data. "
                "Available base years: '2022-23' (latest) and '2011-12'. "
                "DEFAULT to '2022-23' for recent data unless user specifies otherwise. "
                "Pass base_year along with series, frequency_code, and indicator_code."
            )
            return result
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_nas_filters(
        self,
        series: str = "Current",
        frequency_code: int = 1,
        indicator_code: int = 1,
        base_year: str = "2022-23"
    ) -> Dict[str, Any]:
        """Fetch available NAS filters for given series/frequency/indicator.

        Args:
            series: "Current" or "Back"
            frequency_code: 1 (Annually) or 2 (Quarterly, Current series only)
            indicator_code: Indicator code (1-22 for Annual, 1-11 for Quarterly)
            base_year: Base year - "2022-23" (latest) or "2011-12"
        """
        params = {
            "base_year": base_year,
            "series": series,
            "frequency_code": frequency_code,
            "indicator_code": indicator_code,
        }

        try:
            response = requests.get(
                f"{self.base_url}/api/nas/getNasFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # WPI Metadata Methods
    # =========================================================================

    def get_wpi_filters(self) -> Dict[str, Any]:
        """Fetch available WPI filters from MoSPI API.

        Returns:
            Available filters: year, month, major_group, group, sub_group, sub_sub_group, item
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/wpi/getWpiData",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # Energy Metadata Methods
    # =========================================================================

    def get_energy_indicators(self) -> Dict[str, Any]:
        """Fetch list of Energy indicators from MoSPI API."""
        try:
            response = requests.get(
                f"{self.base_url}/api/energy/getEnergyIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_energy_filters(
        self,
        indicator_code: int = 1,
        use_of_energy_balance_code: int = 1
    ) -> Dict[str, Any]:
        """Fetch available Energy filters for given indicator and balance type.

        Args:
            indicator_code: 1 (KToE) or 2 (PetaJoules)
            use_of_energy_balance_code: 1 (Supply) or 2 (Consumption)
        """
        params = {
            "indicator_code": indicator_code,
            "use_of_energy_balance_code": use_of_energy_balance_code,
        }

        try:
            response = requests.get(
                f"{self.base_url}/api/energy/getEnergyFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # AISHE (All India Survey on Higher Education) Methods
    # =========================================================================

    def get_aishe_indicators(self) -> Dict[str, Any]:
        """Fetch list of AISHE indicators from MoSPI API.

        Returns 9 indicators covering:
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
        try:
            response = requests.get(
                f"{self.base_url}/api/aishe/getAisheIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_aishe_filters(self, indicator_code: int) -> Dict[str, Any]:
        """Fetch available AISHE filters for given indicator.

        Args:
            indicator_code: Indicator code (1-9)
        """
        params = {"indicator_code": indicator_code}

        try:
            response = requests.get(
                f"{self.base_url}/api/aishe/getAisheFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # ASUSE (Annual Survey of Unincorporated Sector Enterprises) Methods
    # =========================================================================

    def get_asuse_frequencies(self) -> Dict[str, Any]:
        """Fetch list of ASUSE frequencies from MoSPI API."""
        try:
            response = requests.get(
                f"{self.base_url}/api/asuse/getAsuseFrequencyList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_asuse_indicators(self, frequency_code: int = 1) -> Dict[str, Any]:
        """Fetch list of ASUSE indicators grouped by frequency_code.

        Args:
            frequency_code: 1=Annually, 2=Quarterly (ignored - fetches both)
        """
        url = f"{self.base_url}/api/asuse/getAsuseIndicatorListByFrequency"
        result = {}
        try:
            for fc, label in [(1, "Annual"), (2, "Quarterly")]:
                response = requests.get(url, params={"frequency_code": fc}, timeout=30)
                response.raise_for_status()
                data = response.json()
                result[f"frequency_code_{fc}_{label}"] = data.get("data", [])
            return {
                "indicators_by_frequency": result,
                "_note": "frequency_code=1 (Annual) has 35 indicators on establishment details, ownership, workers, GVA. "
                         "frequency_code=2 (Quarterly) has 15 indicators including market establishments, worker counts. "
                         "For RECENT data or quarterly breakdowns (Jan-Mar, Apr-Jun, etc.), use frequency_code=2. "
                         "Pass the correct frequency_code in 3_get_metadata() and 4_get_data().",
                "statusCode": True,
            }
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_asuse_filters(self, indicator_code: int, frequency_code: int = 1) -> Dict[str, Any]:
        """Fetch available ASUSE filters for given indicator.

        Args:
            indicator_code: Indicator code
            frequency_code: 1=Annually, 2=Quarterly
        """
        params = {
            "indicator_code": indicator_code,
            "frequency_code": frequency_code
        }

        try:
            response = requests.get(
                f"{self.base_url}/api/asuse/getAsuseFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # Gender Statistics Methods
    # =========================================================================

    def get_gender_indicators(self) -> Dict[str, Any]:
        """Fetch list of Gender indicators from MoSPI API.

        Returns 157 indicators covering demographics, health, education,
        labour, time use, financial inclusion, political participation,
        crimes against women, and more.
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/gender/getGenderIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_gender_filters(self, indicator_code: int) -> Dict[str, Any]:
        """Fetch available Gender filters for given indicator.

        Args:
            indicator_code: Indicator code (1-157)
        """
        params = {"indicator_code": indicator_code}

        try:
            response = requests.get(
                f"{self.base_url}/api/gender/getGenderFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # NFHS (National Family Health Survey) Metadata Methods
    # =========================================================================

    def get_nfhs_indicators(self) -> Dict[str, Any]:
        """Fetch list of NFHS indicators from MoSPI API."""
        try:
            response = requests.get(
                f"{self.base_url}/api/nfhs/getNfhsIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_nfhs_filters(self, indicator_code: int) -> Dict[str, Any]:
        """Fetch available NFHS filters for given indicator.

        Args:
            indicator_code: Indicator code
        """
        params = {"indicator_code": indicator_code}

        try:
            response = requests.get(
                f"{self.base_url}/api/nfhs/getNfhsFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # Environment Statistics Methods
    # =========================================================================

    def get_envstats_indicators(self) -> Dict[str, Any]:
        """Fetch list of Environment Statistics indicators from MoSPI API.

        Returns 124 indicators covering climate, biodiversity, pollution,
        resources, disasters, health, and environmental expenditure.
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/env/getEnvStatsIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_envstats_filters(self, indicator_code: int) -> Dict[str, Any]:
        """Fetch available Environment Statistics filters for given indicator.

        Args:
            indicator_code: Indicator code (1-130)
        """
        params = {"indicator_code": indicator_code}

        try:
            response = requests.get(
                f"{self.base_url}/api/env/getEnvStatsFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # RBI (Reserve Bank of India) Statistics Methods
    # =========================================================================

    def get_rbi_indicators(self) -> Dict[str, Any]:
        """Fetch list of RBI indicators from MoSPI API.

        Returns 39 indicators covering foreign trade, balance of payments,
        forex rates, external debt, and NRI deposits.
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/rbi/getRbiIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_rbi_filters(self, sub_indicator_code: int) -> Dict[str, Any]:
        """Fetch available RBI filters for given indicator.

        Args:
            sub_indicator_code: Indicator code (1-48)
        """
        params = {"sub_indicator_code": sub_indicator_code}

        try:
            response = requests.get(
                f"{self.base_url}/api/rbi/getRbiMetaData",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_nss77_indicators(self) -> Dict[str, Any]:
        """Fetch list of NSS77 indicators from MoSPI API.

        Returns indicators from NSS 77th Round (Situation Assessment Survey of Agricultural Households).
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/nss-77/getIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_nss77_filters(self, indicator_code: int) -> Dict[str, Any]:
        """Fetch available NSS77 filters for given indicator.

        Args:
            indicator_code: Indicator code (16-51)
        """
        params = {"indicator_code": indicator_code}

        try:
            response = requests.get(
                f"{self.base_url}/api/nss-77/getFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_nss78_indicators(self) -> Dict[str, Any]:
        """Fetch list of NSS78 indicators from MoSPI API.

        Returns indicators from NSS 78th Round (All India Survey on Domestic Tourists).
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/nss-78/getIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_nss78_filters(self, indicator_code: int) -> Dict[str, Any]:
        """Fetch available NSS78 filters for given indicator.

        Args:
            indicator_code: Indicator code (2-15)
        """
        params = {"indicator_code": indicator_code}

        try:
            response = requests.get(
                f"{self.base_url}/api/nss-78/getFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # CPIALRL (CPI for Agricultural Labourers and Rural Labourers) Methods
    # =========================================================================

    def get_cpialrl_indicators(self) -> Dict[str, Any]:
        """Fetch list of CPIALRL indicators from MoSPI API.

        Returns 2 indicators: General Index and Group Index.
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/cpialrl/getCpialrlIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_cpialrl_filters(self, indicator_code: int) -> Dict[str, Any]:
        """Fetch available CPIALRL filters for given indicator.

        Args:
            indicator_code: Indicator code (1-2)
        """
        params = {"indicator_code": indicator_code}

        try:
            response = requests.get(
                f"{self.base_url}/api/cpialrl/getCpialrlFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # HCES (Household Consumption Expenditure Survey) Methods
    # =========================================================================

    def get_hces_indicators(self) -> Dict[str, Any]:
        """Fetch list of HCES indicators from MoSPI API.

        Returns 9 indicators covering MPCE, consumption patterns,
        Gini coefficient, and expenditure by household type/social group.
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/hces/getHcesIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_hces_filters(self, indicator_code: int) -> Dict[str, Any]:
        """Fetch available HCES filters for given indicator.

        Args:
            indicator_code: Indicator code (1-9)
        """
        params = {"indicator_code": indicator_code}

        try:
            response = requests.get(
                f"{self.base_url}/api/hces/getHcesFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    # =========================================================================
    # TUS (Time Use Survey) Methods
    # =========================================================================

    def get_tus_indicators(self) -> Dict[str, Any]:
        """Fetch list of TUS indicators from MoSPI API.

        Returns 41 indicators covering time spent on paid/unpaid activities,
        SNA/non-SNA activities, by gender, age, education, marital status, etc.
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tus/getTusIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_tus_filters(self, indicator_code: int) -> Dict[str, Any]:
        """Fetch available TUS filters for given indicator.

        Args:
            indicator_code: Indicator code (4-44)
        """
        params = {"indicator_code": indicator_code}

        try:
            response = requests.get(
                f"{self.base_url}/api/tus/getTusFilterByIndicatorId",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}


# Global instance
mospi = MoSPI()
