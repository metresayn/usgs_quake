from pydantic import BaseModel, Field
from typing import Optional, List


class ContentModel(BaseModel):
    contentType: str
    lastModified: int
    url: str


class ContentModelJson(BaseModel):
    json_object: ContentModel = Field(alias="nearby-cities.json")


class NearbycityModel(BaseModel):
    code: str
    source: str
    status: str
    contents: ContentModelJson


class ProductModel(BaseModel):
    nearby_cities: Optional[list[NearbycityModel]] = Field(alias="nearby-cities")


class PropertyDetailedModel(BaseModel):
    url: str
    mag: int
    place: str
    products: ProductModel


class DetailModel(BaseModel):
    type: str
    property: PropertyDetailedModel
    id: str
