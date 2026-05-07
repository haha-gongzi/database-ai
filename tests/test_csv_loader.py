import pandas as pd
from app.db import Database
from app.schema_manager import SchemaManager
from app.csv_loader import CSVLoader


def test_csv_loader_creates_table_and_inserts_data(tmp_path):
    csv_path = tmp_path / "users.csv"
    db_path = tmp_path / "test.db"

    df = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Age": [20, 25]
    })

    df.to_csv(csv_path, index=False)

    db = Database(str(db_path))
    schema_manager = SchemaManager(db)
    loader = CSVLoader(db, schema_manager)

    message = loader.load_csv(str(csv_path), "users")

    rows = db.fetch_all("SELECT name, age FROM users;")

    assert "created" in message.lower()
    assert rows == [("Alice", 20), ("Bob", 25)]