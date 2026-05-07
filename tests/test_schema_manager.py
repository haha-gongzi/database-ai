from app.db import Database
from app.schema_manager import SchemaManager


def test_schema_manager_create_and_list_table(tmp_path):
    db_path = tmp_path / "test.db"
    db = Database(str(db_path))
    schema_manager = SchemaManager(db)

    schema_manager.create_table(
        "users",
        {
            "name": "TEXT",
            "age": "INTEGER"
        }
    )

    tables = schema_manager.list_tables()

    assert "users" in tables


def test_schema_manager_get_table_schema(tmp_path):
    db_path = tmp_path / "test.db"
    db = Database(str(db_path))
    schema_manager = SchemaManager(db)

    schema_manager.create_table(
        "users",
        {
            "name": "TEXT",
            "age": "INTEGER"
        }
    )

    schema = schema_manager.get_table_schema("users")

    assert schema == {
        "name": "TEXT",
        "age": "INTEGER"
    }