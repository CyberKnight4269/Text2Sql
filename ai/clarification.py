import json
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.getcwd())

from google import genai
from ai.gemini import client
from database.models import DatabaseSchema

load_dotenv()

class ClarificationEngine:

    def check(self,question: str,schema_context: str, conversation_context):
        system_prompt = """
            You are a database query clarification engine.

            Your job is to determine whether a user's database question
            contains ambiguity that could cause an incorrect query.

            You have access to the database schema.

            Ask for clarification when:
            - The user uses an undefined or subjective term.
            - The requested information cannot be determined from the schema.
            - Multiple interpretations could produce substantially different queries.
            - The user refers to something unclear.
            - A required condition is missing.

            Do NOT ask for clarification when the question is sufficiently
            clear to generate a reasonable database query.

            Return ONLY valid JSON in this format:
            {
                "needs_clarification": True,
                "reason": "short explanation",
                "question": "clarification question"
            }
            or:
            {
                "needs_clarification": False,
                "reason": null,
                "question": null
            }
        """

        input_context = f"""
            Database schema:
            {schema_context}

            Conversation Context:
            {conversation_context}

            User question:
            {question}
        """

        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            system_instruction=system_prompt,
            input=input_context,
            response_format={
                "type": "text",
                "mime_type": "application/json"
            }
        )

        text_response = interaction.output_text.strip()

        return json.loads(text_response)