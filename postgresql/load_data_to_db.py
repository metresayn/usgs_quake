import pandas as pd
import psycopg2.extras
from psycopg2 import OperationalError
from typing import Optional
from loguru import logger


def execute_query(connection, query_path, query) -> Optional[int]:
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        query_string = query(query_path)
        cursor.execute(query_string)
    except OperationalError as e:
        print(f"The error '{e}' occurred")

    try:
        (number_of_rows,) = cursor.fetchone()
    except psycopg2.ProgrammingError:
        logger.info("no result set to fetch")
        return
    return number_of_rows


def execute_query_for_getting_event_ids(connection, query_path, query) -> Optional[int]:
    connection.autocommit = True
    cursor = connection.cursor()
    event_ids = []
    try:
        query_string = query(query_path)
        cursor.execute(query_string)
    except OperationalError as e:
        print(f"The error '{e}' occurred")

    try:
        rows = cursor.fetchall()
        for row in rows:
            event_ids.append(row[0])
    except Exception as err:
        logger.warning(err)
        return
    return event_ids


def store_dataframe_to_table(
    events_df: pd.DataFrame, table_name: str, connection
) -> None:
    """
    Store the dataframe into table
    INPUTS:
    ___________________________
        events_df: pd.DataFrame
        table_name: str
    RETURN:
        None
    """
    if len(events_df) > 0:
        df_columns = list(events_df)
        # create (col1,col2,...)
        columns = ",".join(df_columns)

        # create VALUES('%s', '%s",...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))

        # create INSERT INTO table (columns) VALUES('%s',...)
        insert_stmt = "INSERT INTO {} ({}) {}".format(table_name, columns, values)

        cur = connection.cursor()
        psycopg2.extras.execute_batch(cur, insert_stmt, events_df.values)
        connection.commit()
        cur.close()
