# import parent module
import sys

sys.path.append("../usgs_quake")


import requests
from typing import Dict, List, Optional
import pandas as pd
import datetime
from api.earthquake_model import FeatureModel, EarthquakeModel
from helpers import flatten_data
from loguru import logger


class EarthquakeJson:
    def __init__(
        self,
        api_url,
        data_format,
        retrieval_start_time,
        retrieval_end_time,
        api_limit,
        offset,
    ) -> None:
        self.api_url = api_url
        self.data_format = data_format
        self.retrieval_start_time = retrieval_start_time
        self.retrieval_end_time = retrieval_end_time
        self.api_limit = api_limit
        self.offset = offset
        self.data = self.retrieve_data_from_api()

    def retrieve_data_from_api(
        self,
    ) -> Dict:
        self.query_params: Dict = {
            "format": self.data_format,
            "starttime": datetime.datetime.strptime(
                self.retrieval_start_time, "%d-%m-%Y"
            ).date(),
            "endtime": datetime.datetime.strptime(
                self.retrieval_end_time, "%d-%m-%Y"
            ).date(),
            "limit": self.api_limit,
            "offset": self.offset,
        }
        try:
            response = requests.get(self.api_url, params=self.query_params)
        except Exception as err:
            logger.warn(err)
        json_data: requests.Response = response.json()
        logger.info(f"Response successfull with status: {response.status_code}")
        return json_data

    def parse_data(self) -> List:
        self.events_data_list = []
        self.earthquake = EarthquakeModel(
            type=self.data.get("type"),
            metadata=self.data.get("metadata"),
            features=self.data.get("features"),
        )
        # TODO remove looping, currently we normalize the data, not required for answering questions
        for elements in self.data.get("features"):
            self.feature = FeatureModel(
                id=elements["id"],
                type=elements["type"],
                property=elements["properties"],
                geometry=elements["geometry"],
            )
            self.events_data_list.append(self.feature.dict())
            logger.info(f"Parsing successful for event {self.feature.id}")

        return self.events_data_list

    def create_dataframe_from_list(self) -> pd.DataFrame:
        events_df = pd.json_normalize(self.events_data_list, max_level=1)
        # TODO use configuartion for this transformation
        events_df = events_df.rename(
            columns={
                "property.mag": '"property.mag"',
                "property.place": '"property.place"',
                "property.detail": '"property.detail"',
                "geometry.type": '"geometry.type"',
                "geometry.coordinates": '"geometry.coordinates"',
            }
        )
        events_df["generated_at"] = self.earthquake.metadata.generated

        # if you encounter a "year is out of range" error the timestamp
        # may be in milliseconds, try `ts /= 1000` in that case
        events_df["created_at"] = datetime.datetime.utcfromtimestamp(
            self.feature.property.time / 1000
        ).strftime("%Y-%m-%d %H:%M:%S")
        events_df["updated_at"] = datetime.datetime.utcfromtimestamp(
            self.feature.property.updated / 1000
        ).strftime("%Y-%m-%d %H:%M:%S")

        # remove columns not required anymore
        events_df.drop(["property.time", "property.updated"], axis=1, inplace=True)
        # flattened_events_df = flatten_data.flatten_nested_json_df(events_df)
        logger.info(f"dataframe generated for api call")
        return events_df
