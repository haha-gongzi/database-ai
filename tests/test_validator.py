from app.db import Database
from app.schema_manager import SchemaManager
from app.validator import SQLValidator


def setup_validator():
    db = Database("test.db")
    schema_manager = SchemaManager(db)

    # create test table
    db.execute("CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, product TEXT);")

    return SQLValidator(schema_manager)


def test_valid_select():
    validator = setup_validator()
    valid, msg = validator.validate("SELECT * FROM sales;")
    assert valid is True


def test_invalid_delete():
    validator = setup_validator()
    valid, msg = validator.validate("DELETE FROM sales;")
    assert valid is False


def test_unknown_table():
    validator = setup_validator()
    valid, msg = validator.validate("SELECT * FROM fake;")
    assert valid is False

def test_reject_unknown_column(tmp_path):
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

    validator = SQLValidator(schema_manager)

    valid, message = validator.validate(
        "SELECT salary FROM users;"
    )

    assert valid is False
    assert "Unknown column" in message