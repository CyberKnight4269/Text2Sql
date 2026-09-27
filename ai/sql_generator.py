import os
import sys
from dotenv import load_dotenv

sys.path.append(os.getcwd())

from ai.gemini import client
from google import genai

load_dotenv()

class SQLGenerator:

    def generate(self,question: str, schema_context: str, conversation_context) -> str:

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
        input_context = f"""
            Here is the database schema:
            {schema_context}

            Conversation Context:
            {conversation_context}

            User's question:
            {question}
        """

        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            system_instruction=system_prompt,
            input=input_context
        )

        sql=interaction.output_text

        return sql
