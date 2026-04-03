import pandas as pd
from app.db import Database


class SchemaManager:
    TYPE_MAPPING = {
        "int64": "INTEGER",
        "float64": "REAL",
        "object": "TEXT",
        "bool": "INTEGER"
    }

    def __init__(self, db: Database):
        self.db = db

    def normalize_column_name(self, name: str) -> str:
        return name.strip().lower().replace(" ", "_")

    def infer_schema_from_dataframe(self, df: pd.DataFrame) -> dict:
        schema = {}
        for col in df.columns:
            normalized_col = self.normalize_column_name(col)
            dtype_str = str(df[col].dtype)
            sqlite_type = self.TYPE_MAPPING.get(dtype_str, "TEXT")
            schema[normalized_col] = sqlite_type
        return schema

    def list_tables(self) -> list:
        rows = self.db.fetch_all(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
        )
        return [row[0] for row in rows]

    def get_table_schema(self, table_name: str) -> dict:
        rows = self.db.fetch_all(f"PRAGMA table_info({table_name});")
        schema = {}
        for row in rows:
            col_name = row[1]
            col_type = row[2]
            if col_name != "id":
                schema[col_name] = col_type
        return schema

    def is_compatible(self, csv_schema: dict, db_schema: dict) -> bool:
        return csv_schema == db_schema

    def create_table_sql(self, table_name: str, schema: dict) -> str:
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
        for col_name, col_type in schema.items():
            columns.append(f"{col_name} {col_type}")
        columns_sql = ", ".join(columns)
        return f"CREATE TABLE {table_name} ({columns_sql});"

    def create_table(self, table_name: str, schema: dict):
        sql = self.create_table_sql(table_name, schema)
        self.db.execute(sql)