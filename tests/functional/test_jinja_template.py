from utils.template import read_ddl_db, read_ddl_dml_table


def test_ddl_command():
    actual = read_ddl_db("utils/templates/ddl_db.sql")
    expected = "CREATE DATABASE usgs;"
    assert actual == expected
