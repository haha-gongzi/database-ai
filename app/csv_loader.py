import pandas as pd
from app.db import Database
from app.schema_manager import SchemaManager


class CSVLoader:
    def __init__(self, db: Database, schema_manager: SchemaManager):
        self.db = db
        self.schema_manager = schema_manager

    def load_csv(self, file_path: str, table_name: str):
        df = pd.read_csv(file_path)

        # Standardize Column Names
        df.columns = [
            self.schema_manager.normalize_column_name(col)
            for col in df.columns
        ]

        # infer schema
        csv_schema = self.schema_manager.infer_schema_from_dataframe(df)

        existing_tables = self.schema_manager.list_tables()

        if table_name in existing_tables:
            db_schema = self.schema_manager.get_table_schema(table_name)

            if self.schema_manager.is_compatible(csv_schema, db_schema):
                self.insert_rows(table_name, df)
                return f"Data appended to existing table '{table_name}'"
            else:
                new_table = table_name + "_new"
                self.schema_manager.create_table(new_table, csv_schema)
                self.insert_rows(new_table, df)
                return f"Schema mismatch. Created new table '{new_table}'"

        # table does not exist → create
        self.schema_manager.create_table(table_name, csv_schema)
        self.insert_rows(table_name, df)

        return f"Table '{table_name}' created and data inserted"

    def insert_rows(self, table_name: str, df: pd.DataFrame):
        columns = list(df.columns)
        placeholders = ", ".join(["?"] * len(columns))
        columns_sql = ", ".join(columns)

        insert_sql = f"""
        INSERT INTO {table_name} ({columns_sql})
        VALUES ({placeholders});
        """

        rows = [tuple(row) for row in df.itertuples(index=False, name=None)]

        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.executemany(insert_sql, rows)
            conn.commit()