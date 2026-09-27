import os
from dotenv import load_dotenv

from database.adapters.postgres import PostgreSQLAdapter
from ai.sql_generator import SQLGenerator
from ai.clarification import ClarificationEngine
from ai.conversationContext import ConversationContext

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL is not set")

adapter = PostgreSQLAdapter(database_url)

adapter.connect()

if not adapter.test_connection():
    print("Database connection failed!")

else:
    choice = input('"/start"-> Start the conversation\n"/q"-> Exit\n')
    if choice != '/q':
        conversationContext = ConversationContext()
        clarification_engine = ClarificationEngine()
        sqlGenerator = SQLGenerator()
        schema = adapter.get_schema()
        while True:
            question = input("\nAsk your question : ")
            if question == '/q':
                break
            while True:
                result = clarification_engine.check(question,schema,conversationContext.get_messages())
                if result["needs_clarification"]:
                    conversationContext.add_user_message(question)
                    conversationContext.add_assistant_message(result["question"])
                    print(f"Agent: {result["question"]}")
                    question=input()
                else:
                    sql=sqlGenerator.generate(question,schema,conversationContext.get_messages())
                    conversationContext.add_user_message(question)
                    result = adapter.execute(sql)
                    conversationContext.add_assistant_message(result)
                    if result:
                        for row in result:
                            print(row)
                    else:
                        print("No results.")
                    break
        conversationContext.clear()
adapter.disconnect()