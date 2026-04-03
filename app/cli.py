from app.db import Database
from app.schema_manager import SchemaManager
from app.csv_loader import CSVLoader
from app.query_service import QueryService


def main():
    db = Database("app_data.db")
    schema_manager = SchemaManager(db)
    loader = CSVLoader(db, schema_manager)
    query_service = QueryService(db, schema_manager)

    print("Welcome to DatabaseAI CLI")
    print("Commands:")
    print("  load <csv_path> <table_name>")
    print("  tables")
    print("  schema <table_name>")
    print("  query <SQL>")
    print("  exit")

    while True:
        user_input = input("\n> ").strip()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Goodbye.")
            break

        parts = user_input.split(maxsplit=2)
        command = parts[0].lower()

        try:
            if command == "load":
                if len(parts) < 3:
                    print("Usage: load <csv_path> <table_name>")
                    continue
                csv_path = parts[1]
                table_name = parts[2]
                result = loader.load_csv(csv_path, table_name)
                print(result)

            elif command == "tables":
                print(schema_manager.list_tables())

            elif command == "schema":
                if len(parts) < 2:
                    print("Usage: schema <table_name>")
                    continue
                print(schema_manager.get_table_schema(parts[1]))

            elif command == "query":
                if len(parts) < 2:
                    print("Usage: query <SQL>")
                    continue
                sql = user_input[len("query "):]
                result = query_service.execute_query(sql)
                print(result)

            else:
                print("Unknown command.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()