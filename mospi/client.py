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
            "HCES": "/api/hces/getHcesRecords",
            "NSS78": "/api/nss-78/getNss78Records",
            "NFHS": "/api/nfhs/getNfhsRecords",
            "ASUSE": "/api/asuse/getAsuseRecords",
            "TUS": "/api/tus/getTusRecords",
            "GENDER": "/api/gender/getGenderRecords",
            "RBI": "/api/rbi/getRbiRecords",
            "ENVSTATS": "/api/env/getEnvStatsRecords",
            "AISHE": "/api/aishe/getAisheRecords",
            "CPIALRL": "/api/cpialrl/getCpialrlRecords",
            "NSS77": "/api/nss-77/getNss77Records",
        }

    def get_data(self, dataset_name: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Fetches data from a specified MoSPI dataset.
        """
        endpoint_path = self.api_endpoints.get(dataset_name)
        if not endpoint_path:
            return {"error": f"Dataset '{dataset_name}' not found."}

        full_url = f"{self.base_url}{endpoint_path}"

        # Clean up params - remove None values
        if params:
            params = {k: v for k, v in params.items() if v is not None}

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
        """Fetch list of all PLFS indicators from MoSPI API."""
        try:
            response = requests.get(
                f"{self.base_url}/api/plfs/getIndicatorListByFrequency",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
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
        base_year: str = "2012",
        level: str = "Group"
    ) -> Dict[str, Any]:
        """Fetch available CPI filters for given base year and level.

        Args:
            base_year: "2012" or "2010"
            level: "Group" or "Item"
        """
        params = {
            "base_year": base_year,
            "level": level,
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
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_nas_filters(
        self,
        series: str = "Current",
        frequency_code: int = 1,
        indicator_code: int = 1
    ) -> Dict[str, Any]:
        """Fetch available NAS filters for given series/frequency/indicator.

        Args:
            series: "Current" or "Back"
            frequency_code: 1 (Annually) or 2 (Quarterly, Current series only)
            indicator_code: Indicator code (1-22 for Annual, 1-11 for Quarterly)
        """
        params = {
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
    # NSS78 Metadata Methods
    # =========================================================================

    def get_nss78_indicators(self) -> Dict[str, Any]:
        """Fetch list of NSS78 indicators from MoSPI API."""
        try:
            response = requests.get(
                f"{self.base_url}/api/nss-78/getIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_nss78_filters(
        self,
        indicator_code: int,
        sub_indicator_code: Optional[int] = None
    ) -> Dict[str, Any]:
        """Fetch available NSS78 filters for given indicator.

        Args:
            indicator_code: Indicator code (2-15)
            sub_indicator_code: Sub-indicator code (optional)
        """
        params = {"indicator_code": indicator_code}
        if sub_indicator_code:
            params["sub_indicator_code"] = sub_indicator_code

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
    # HCES Metadata Methods
    # =========================================================================

    def get_hces_indicators(self) -> Dict[str, Any]:
        """Fetch list of HCES indicators from MoSPI API."""
        try:
            response = requests.get(
                f"{self.base_url}/api/hces/getHcesIndicatorList",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e), "statusCode": False}

    def get_hces_filters(self, indicator_code: int = 1) -> Dict[str, Any]:
        """Fetch available HCES filters for given indicator.

        Args:
            indicator_code: Indicator code 1-9
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
    # TUS (Time Use Survey) Metadata Methods
    # =========================================================================

    def get_tus_indicators(self) -> Dict[str, Any]:
        """Fetch list of TUS indicators from MoSPI API."""
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
            indicator_code: Indicator code (1-21)
        """
        params = {"indicator_code": indicator_code}

        try:
            response = requests.get(
                f"{self.base_url}/api/nfhs/getnfhsFilterByIndicatorId",
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
        """Fetch list of ASUSE indicators for given frequency.

        Args:
            frequency_code: 1=Annually, 2=Quarterly
        """
        params = {"frequency_code": frequency_code}

        try:
            response = requests.get(
                f"{self.base_url}/api/asuse/getAsuseIndicatorListByFrequency",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
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
    # CPIALRL (CPI for Agricultural Labourers and Rural Labourers) Methods
    # =========================================================================

    def get_cpialrl_indicators(self) -> Dict[str, Any]:
        """Fetch list of CPIALRL indicators from MoSPI API.

        Returns 2 indicators:
        - General Index (1)
        - Group Index (2)
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
    # NSS77 (Land and Livestock Holdings Survey) Methods
    # =========================================================================

    def get_nss77_indicators(self) -> Dict[str, Any]:
        """Fetch list of NSS77 indicators from MoSPI API.

        Returns 33 indicators covering:
        - Land holdings and possession
        - Agricultural household income
        - Crop production and expenses
        - Livestock ownership
        - Loan and insurance data
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


# Global instance
mospi = MoSPI()
