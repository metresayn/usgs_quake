from api import (
    fetch_and_transform_earthquake_detail,
    fetch_and_transform_earthquake_property,
)
from postgresql.connection import create_connection, close_connection
from postgresql.load_data_to_db import (
    execute_query,
    execute_query_for_getting_event_ids,
)
from postgresql.load_data_to_db import store_dataframe_to_table
from config import settings
import requests
from utils.template import read_ddl_db, read_ddl_dml_table
from loguru import logger
import psycopg2


def read_table_count(connection: psycopg2.extensions.connection) -> int:
    """
    Reads the table count for events table
    Input:
        connection: postgres.connection
    """
    return execute_query(
        connection, query_path="utils/templates/dml_count.sql", query=read_ddl_dml_table
    )


def check_count_of_api_query() -> bool:
    """
    Reads the count of data for an api call
    """
    api_url_template = settings.api.count_query
    api_url = api_url_template.format(settings.api.start_date, settings.api.end_date)
    response = requests.get(api_url)
    logger.info("count api call successful")
    return int(response.text)


def incrementally_load_earthquake_feature_data_given_dates(
    connection: psycopg2.extensions.connection, start_date: str, end_date: str
) -> None:
    """
    Incrementally loads data into db
    Input:
        connection: postgres connection object
        start_date: start_date for api call
        end_date: end_date for api call
    """
    counter = 0
    api_count = check_count_of_api_query()
    batch_counter = 0
    while counter != api_count:
        logger.info(f"Batch Counter -> {batch_counter}")
        earthquake_data = fetch_and_transform_earthquake_property.EarthquakeJson(
            api_url=settings["api"].get("events_query"),
            retrieval_start_time=start_date,
            retrieval_end_time=end_date,
            api_limit=settings["api"].get("limit"),
            data_format=settings["api"].get("dataformat"),
            offset=counter + 1,
        )
        data = earthquake_data.parse_data()
        result = earthquake_data.create_dataframe_from_list()

        logger.info(f"dataframe consists of {len(result)} records")

        # store data to in postgres table
        store_dataframe_to_table(
            result, table_name=settings.database.table_name, connection=connection
        )

        # commit count of data to counter var
        counter += len(data)
        batch_counter += 1
        logger.info(
            f"Successfully inserted records for batch number {batch_counter}, table count is currently {read_table_count(conn)} "
        )
    return


def read_unique_events(connection: psycopg2.extensions.connection):
    """
    Get the unique event_ids from events table
    Input:
        connection: postgres connection object
    """
    return execute_query_for_getting_event_ids(
        connection,
        query_path="utils/templates/dml_unique_event_ids.sql",
        query=read_ddl_dml_table,
    )


def incrementally_load_earthquake_from_events(array_of_event_ids: list):
    """
    Using event_ids, load content data (data about nearby cities of earthquake) into db
    Input:
        array_of_event_ids: list of unique event_ids
    """
    for event_id in array_of_event_ids:
        earthquake_detailed_data = (
            fetch_and_transform_earthquake_detail.EarthquakeDetailJson(
                api_url=settings.api.detail_query,
                data_format=settings["api"].get("dataformat"),
                event_id=str(event_id),
            )
        )
        data = earthquake_detailed_data.parse_data()

        if len(data) > 0:
            res = earthquake_detailed_data.create_dataframe_from_list()
            store_dataframe_to_table(res, table_name="nearby_cities", connection=conn)
            logger.info(
                f"Loaded in data in nearby_cities table for event_id -> {event_id}"
            )
    return


# #create connection to postgres
conn = create_connection(
    settings.database.database_name,
    settings.database.username,
    settings.database.password,
    settings.database.host,
    settings.database.port,
)


incrementally_load_earthquake_feature_data_given_dates(
    conn, settings.api.start_date, settings.api.end_date
)
list_of_event_ids = read_unique_events(conn)
incrementally_load_earthquake_from_events(list_of_event_ids)
close_connection(conn)
