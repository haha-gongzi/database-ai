class LLMAdapter:
    """
    Mock LLM Adapter.
    This class simulates converting natural language into SQL.
    """

    def generate_sql(self, user_question: str, schema_context: str = "") -> str:
        question = user_question.lower()

        if "all users" in question:
            return "SELECT * FROM users;"

        if "all products" in question:
            return "SELECT * FROM products;"

        if "count" in question:
            return "SELECT COUNT(*) FROM users;"

        return "SELECT name FROM sqlite_master WHERE type='table';"