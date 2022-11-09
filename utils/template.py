from jinja2 import Template
from config import settings


def read_ddl_dml_table(filepath):
    with open(filepath) as f:
        sql = f.read()
    return Template(sql).render(table_name=settings.database.table_name)


def read_ddl_db(filepath):
    with open(filepath) as f:
        sql = f.read()
    return Template(sql).render(database_name=settings.database.database_name)
