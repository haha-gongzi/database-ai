from app.db import Database
from app.schema_manager import SchemaManager
from app.query_service import QueryService


def test_query_service_valid_select(tmp_path):
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

    db.execute(
        "INSERT INTO users (name, age) VALUES (?, ?);",
        ("Alice", 20)
    )

    service = QueryService(db, schema_manager)

    result = service.execute_query("SELECT name FROM users;")

    assert result["status"] == "success"
    assert result["data"] == [("Alice",)]


def test_query_service_reject_delete(tmp_path):
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

    service = QueryService(db, schema_manager)

    result = service.execute_query("DELETE FROM users;")

    assert result["status"] == "error"
    assert "Only SELECT" in result["message"]