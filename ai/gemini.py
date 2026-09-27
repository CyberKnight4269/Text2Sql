import os
import sys
from dotenv import load_dotenv

sys.path.append(os.getcwd())

from database.adapters.postgres import PostgreSQLAdapter
from google import genai

load_dotenv()

def main():

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL is not set")

    adapter = PostgreSQLAdapter(database_url)
    adapter.connect()

    if not adapter.test_connection():
        print("Database connection failed.")
        return

    print("PostgreSQL connected.")

    schema = adapter.get_schema()

    client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

    system_prompt = """
        You are a Text-to-SQL agent.

        Your task is to convert the user's natural language question
        into a valid PostgreSQL SQL query.

        Rules:
        1. Generate only the SQL query.
        2. Do not provide explanations.
        3. Do not use markdown code fences.
        4. Use only tables and columns provided in the database schema.
        5. Use valid PostgreSQL syntax.
        6. Do not invent tables or columns.
    """

    question = input("\nAsk your question: ")

    input_context = f"""
        Here is the database schema:
        {schema}
        User's question:
        {question}
    """

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        system_instruction=system_prompt,
        input=input_context
    )

    sql=interaction.output_text

    print("\nGenerated SQL:")
    print(sql)

    result = adapter.execute(sql)

    print("\nResult:")

    if result:
        for row in result:
            print(row)
    else:
        print("No results.")
    adapter.disconnect()


if __name__ == "__main__":
    main()