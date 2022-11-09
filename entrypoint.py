from postgresql.connection import create_connection, close_connection
from loguru import logger
from postgresql.load_data_to_db import execute_query
from config import settings
from utils.template import read_ddl_db, read_ddl_dml_table

## Run exactly once to setup database
def create_database(conn):
    # create database in postgres
    execute_query(conn, query_path="utils/templates/ddl_db.sql", query=read_ddl_db)


## Run exactly once to setup table
def create_table(conn):
    # create table in postgres
    execute_query(
        conn, query_path="utils/templates/ddl_table.sql", query=read_ddl_dml_table
    )
    logger.info("Tables successfully created")


conn = create_connection(
    settings.database.database_name,
    settings.database.username,
    settings.database.password,
    settings.database.host,
    settings.database.port,
)
create_database(conn)
create_table(conn)
close_connection(conn)
