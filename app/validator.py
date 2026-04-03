import re
from app.schema_manager import SchemaManager


class SQLValidator:
    def __init__(self, schema_manager: SchemaManager):
        self.schema_manager = schema_manager

    def validate(self, sql: str) -> tuple[bool, str]:
        sql_clean = sql.strip()

        if not sql_clean:
            return False, "Empty query."

        # only one statement is allowed
        if sql_clean.count(";") > 1:
            return False, "Multiple statements are not allowed."

        sql_no_semicolon = sql_clean.rstrip(";").strip()

        # only SELECT is allowed
        if not sql_no_semicolon.lower().startswith("select"):
            return False, "Only SELECT queries are allowed."

        # prohibited dangerous keywords
        forbidden_keywords = [
            "insert", "update", "delete", "drop",
            "alter", "create", "attach", "detach", "pragma"
        ]

        lowered = sql_no_semicolon.lower()
        for keyword in forbidden_keywords:
            if re.search(rf"\b{keyword}\b", lowered):
                return False, f"Forbidden keyword detected: {keyword}"

        # check if the table exists
        tables = self._extract_tables(sql_no_semicolon)
        known_tables = self.schema_manager.list_tables()

        for table in tables:
            if table not in known_tables:
                return False, f"Unknown table: {table}"

        return True, "Query is valid."

    def _extract_tables(self, sql: str) -> list:
        pattern = r"\bfrom\s+([a-zA-Z_][a-zA-Z0-9_]*)|\bjoin\s+([a-zA-Z_][a-zA-Z0-9_]*)"
        matches = re.findall(pattern, sql, flags=re.IGNORECASE)

        tables = []
        for match in matches:
            for group in match:
                if group:
                    tables.append(group)
        return tables