# import parent module
import sys

sys.path.append("../usgs_quake")


import requests
from typing import Dict, List, Optional
import pandas as pd
from api.earthquake_detail_model import DetailModel
from loguru import logger


class EarthquakeDetailJson:
    def __init__(self, api_url, data_format, event_id) -> None:
        self.api_url = api_url
        self.data_format = data_format
        self.event_id = event_id
        self.data = self.retrieve_data_from_api()

    def retrieve_data_from_api(
        self,
    ) -> Dict:
        """
        method to call api using api parameters defined when creating object,
        method returns json dictionary of data
        {
            "key": "value"
        }
        """
        try:
            response = requests.get(
                self.api_url.format(self.event_id, self.data_format)
            )
        except Exception as err:
            print(err)

        json_data: requests.Response = response.json()
        logger.info(f"Response successfull with status: {response.status_code}")
        return json_data

    def parse_data(self) -> List:
        """
        method to parse incoming data, and only use what is necessary for querying
        """
        self.earthquake_details_list = []
        self.earthquake_details = DetailModel(
            type=self.data.get("type"),
            property=self.data.get("properties"),
            id=self.data.get("id"),
        )
        if self.earthquake_details.property.products.nearby_cities:
            for nearby_city in self.earthquake_details.property.products.nearby_cities:
                self.earthquake_details_list.append(nearby_city.dict())
        else:
            logger.info(f"No data for {self.earthquake_details.id}")

        return self.earthquake_details_list

    def create_dataframe_from_list(self) -> pd.DataFrame:
        detailed_df = pd.json_normalize(self.earthquake_details_list, max_level=3)
        # TODO use configuartion for this transformation
        detailed_df = detailed_df.rename(
            columns={
                "contents.json_object.contentType": '"contents.json_object.contentType"',
                "contents.json_object.lastModified": '"contents.json_object.lastModified"',
                "contents.json_object.url": '"contents.json_object.url"',
            }
        )
        return detailed_df
