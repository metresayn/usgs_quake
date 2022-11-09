from pydantic import BaseModel
from typing import Optional


class PropertyModel(BaseModel):
    mag: Optional[int]
    place: Optional[str]
    time: int
    updated: int
    detail: str


class GeometryModel(BaseModel):
    type: str
    coordinates: list


class FeatureModel(BaseModel):
    id: str
    property: Optional[PropertyModel]
    geometry: GeometryModel
    type: str = "Feature"


class MetadataModel(BaseModel):
    generated: int
    status: int
    count: int


class EarthquakeModel(BaseModel):
    type: str
    metadata: MetadataModel
    features: list[FeatureModel]
