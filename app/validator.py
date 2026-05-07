import re
from app.schema_manager import SchemaManager


class SQLValidator:
    def __init__(self, schema_manager: SchemaManager):
        self.schema_manager = schema_manager

    def validate(self, sql: str):
        sql = sql.strip()

        if not sql.lower().startswith("select"):
            return False, "Only SELECT queries are allowed."

        tables = self.schema_manager.list_tables()

        table_match = re.search(r'from\s+(\w+)', sql, re.IGNORECASE)

        if not table_match:
            return False, "No table found in query."

        table_name = table_match.group(1)

        if table_name not in tables:
            return False, f"Unknown table: {table_name}"

        # check columns
        schema = self.schema_manager.get_table_schema(table_name)

        select_match = re.search(
            r'select\s+(.*?)\s+from',
            sql,
            re.IGNORECASE
        )

        if select_match:
            columns_part = select_match.group(1)

            if columns_part.strip() != "*":
                columns = [col.strip() for col in columns_part.split(",")]

                for col in columns:
                    if col not in schema:
                        return False, f"Unknown column: {col}"

        return True, "Query is valid."