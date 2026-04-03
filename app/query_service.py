from app.db import Database
from app.schema_manager import SchemaManager
from app.validator import SQLValidator


class QueryService:
    def __init__(self, db: Database, schema_manager: SchemaManager):
        self.db = db
        self.schema_manager = schema_manager
        self.validator = SQLValidator(schema_manager)

    def execute_query(self, sql: str):
        # 1. verity SQL
        is_valid, message = self.validator.validate(sql)

        if not is_valid:
            return {
                "status": "error",
                "message": message
            }

        try:
            # 2. implement SQL
            results = self.db.fetch_all(sql)

            return {
                "status": "success",
                "data": results
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }