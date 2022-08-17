from pydantic import BaseModel, root_validator, validator
from typing import Any, Dict, List, Optional


class BaseData(BaseModel):
    attributes: Any
    id_: str
    type_: str

    class Config:
        fields = {
            "id_": "id",
            "type_": "type",
        }


class Meta(BaseModel):
    count: int


class AnalysisResult(BaseModel):
    category: str
    engine_name: str
    method: str
    result: str


class LastAnalysisResults(BaseModel):
    __root__: Dict[str, AnalysisResult]


class LastAnalysisStats(BaseModel):
    harmless: int
    malicious: int
    suspicious: int
    timeout: int
    undetected: int


class Popularity(BaseModel):
    rank: int
    timestamp: int


class PopularityRanks(BaseModel):
    __root__: Dict[str, Popularity]


class Attributes(BaseModel):
    creation_date: Optional[int]
    jarm: Optional[str]
    last_analysis_results: LastAnalysisResults
    last_analysis_stats: LastAnalysisStats
    last_dns_records_date: Optional[int]
    last_https_certificate_date: Optional[int]
    last_modification_date: Optional[int]
    last_update_date: Optional[int]
    popularity_ranks: PopularityRanks
    registrar: Optional[str]
    reputation: int
    tags: List[str]

class Ip_Attributes(BaseModel):
    as_owner: Optional[str]
    country: Optional[str]
    last_analysis_results: LastAnalysisResults
    last_analysis_stats: LastAnalysisStats
    last_modification_date: Optional[int]
    reputation: int
    whois: Optional[str]


class Ip_Data(BaseData):
    attributes: Ip_Attributes
    id_: str
    type_: str

    class Config:
        fields = {
            "id_": "id",
            "type_": "type",
        }

class Ip(BaseModel):
    data: Ip_Data

class Data(BaseData):
    attributes: Attributes
    id_: str
    type_: str

    class Config:
        fields = {
            "id_": "id",
            "type_": "type",
        }


class Domain(BaseModel):
    data: Data


class ResolutionAttributes(BaseModel):
    date: int
    host_name: str
    resolver: str
    ip_address_last_analysis_stats: LastAnalysisStats
    ip_address: str
    host_name_last_analysis_stats: LastAnalysisStats


class ResolutionData(BaseData):
    attributes: ResolutionAttributes


class Resolutions(BaseModel):
    meta: Meta
    data: List[ResolutionData]


class HistoricalWhoisMap(BaseModel):
    domain: str = ""
    registrar: Optional[str]
    name_servers: List[str] = []
    creation_date: Optional[str]
    expiry_date: Optional[str]
    expiry_date_alt: Optional[str]
    admin_city: Optional[str]
    admin_state: Optional[str]
    admin_country: Optional[str]
    admin_postal_code: Optional[str]
    admin_email: Optional[str]
    last_updated: Optional[str]
    registered_on: Optional[str]
    registrant_name: Optional[str]
    registrant_email: Optional[str]
    updated_date: Optional[str]

    class Config:
        fields = {
            "domain": "Domain Name",
            "registrar": "Registrar",
            "name_servers": "Name Server",
            "creation_date": "Creation Date",
            "expiry_date": "Registry Expiry Date",
            "expiry_date_alt": "Expiry date",
            "admin_city": "Admin City",
            "admin_state": "Admin State/Province",
            "admin_country": "Admin Country",
            "admin_postal_code": "Admin Postal Code",
            "admin_email": "Admin Email",
            "last_updated": "Last updated",
            "registered_on": "Registered on",
            "registrant_name": "Registrant Name",
            "registrant_email": "Registrant Email",
            "updated_date": "Updated Date",
        }

    @validator("name_servers", pre=True)
    def transform_nameservers(cls, v):
        return v.split(" | ")

    @validator("*")
    def dedupe_values(cls, v):
        if "|" in v:
            return v.split(" | ")[0]
        return v


class HistoricalWhoisAttributes(BaseModel):
    first_seen_date: Optional[int]
    whois_map: Optional[HistoricalWhoisMap]
    registrant_country: Optional[str]
    registrar_name: Optional[str]
    last_updated: Optional[int]

    @root_validator(pre=True)
    def remove_empty_whois_map(cls, v):
        if v.get("whois_map") == {}:
            v.pop("whois_map")
        return v


class HistoricalWhoisData(BaseData):
    attributes: HistoricalWhoisAttributes


class HistoricalWhois(BaseModel):
    meta: Meta
    data: List[HistoricalWhoisData]
