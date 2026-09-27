# AI Database Query Agent

An AI-powered, database-agnostic agent that allows users to interact with databases using natural language.

Instead of writing SQL queries manually, users can ask questions such as:

> "Show me the students with the highest CGPA."

The agent understands the database schema, detects ambiguity, asks clarification questions when necessary, generates the appropriate database query, executes it through the corresponding database adapter, and displays the results.

> **Status:** 🚧 Active Development

---

## Overview

The goal of this project is to build a reusable AI layer that can interact with different types of databases without tightly coupling the agent to a specific database technology.

The current implementation focuses on **PostgreSQL**, with an adapter-based architecture designed to support additional databases such as MySQL, SQLite, and MongoDB in the future.

### Current Flow

```text
User
 │
 │ Natural-language question
 ▼
┌─────────────────────────┐
│   Clarification Engine  │
└────────────┬────────────┘
             │
       Is the question
          ambiguous?
        /            \
      Yes             No
       │               │
       ▼               │
 Ask clarification     │
       │               │
       ▼               │
 User's answer         │
       │               │
       └───────┬───────┘
               ▼
       ┌───────────────┐
       │ SQL Generator │
       └───────┬───────┘
               │
               ▼
       ┌──────────────────┐
       │ SQL / Query      │
       │ Validation Layer │
       └────────┬─────────┘
                │
                ▼
       ┌──────────────────┐
       │ Database Adapter │
       └────────┬─────────┘
                │
                ▼
           PostgreSQL
                │
                ▼
             Results
```

---

## Key Features

### Natural Language Queries

Users can interact with the database using natural language instead of writing SQL manually.

Example:

```text
Ask your question: Get all students with CGPA above 8
```

The agent can generate:

```sql
SELECT *
FROM student
WHERE cgpa > 8;
```

---

### Database Schema Awareness

The agent retrieves the schema from the connected database and provides the relevant database context to the LLM.

For example:

```text
Database: text2sql
Database Type: PostgreSQL

Table: student

Columns:
- id: INTEGER
- name: VARCHAR(50)
- email: VARCHAR(50)
- address: VARCHAR(100)
- cgpa: NUMERIC(5,2)
```

This allows the LLM to generate queries using the actual tables and columns available in the database.

---

### Clarification Engine

Natural-language questions can be ambiguous.

For example:

```text
User: Get the best student
```

The agent should not blindly assume that "best" means the highest CGPA.

Instead, the clarification engine can ask:

```text
Agent: What should "best" mean? Should I use the highest CGPA?
```

The user's answer becomes part of the temporary conversation context.

---

### Temporary Conversation Context

Conversation context is maintained while the main conversation is running.

For example:

```text
User: Get the best student.

Agent: What do you mean by "best"?

User: The student with the highest CGPA.
```

The SQL generator can use the complete context to understand the user's final intent.

The context is temporary and is not persisted after the conversation ends.

---

### Adapter-Based Database Architecture

The AI layer is separated from the database implementation through a common adapter interface.

```text
                 AI Agent
                    │
             DatabaseAdapter
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   PostgreSQL     MySQL      MongoDB
    Adapter       Adapter     Adapter
```

This makes it possible to add support for additional databases without changing the core AI logic.

---

## Architecture

The project currently follows this structure:

```text
text2sql/
│
├── ai/
│   ├── __init__.py
│   ├── gemini.py
│   ├── clarification.py
│   ├── sql_generator.py
│   └── conversationContext.py
│
├── database/
│   ├── __init__.py
│   ├── base.py
│   ├── models.py
│   │
│   └── adapters/
│       ├── __init__.py
│       └── postgres.py
│
├── main.py
├── .env
├── requirements.txt
└── README.md
```

### AI Layer

#### `gemini.py`

Responsible for initializing the Gemini client.

```text
gemini.py
    │
    └── Gemini API Client
             │
       ┌─────┴─────┐
       ▼           ▼
Clarification   SQL Generator
Engine
```

The Gemini client is created in one place and reused by the AI components.

#### `clarification.py`

Responsible for determining whether the user's request is ambiguous and generating clarification questions when required.

#### `sql_generator.py`

Responsible for converting the resolved user intent and database context into a database query.

#### `conversationContext.py`

Maintains temporary conversation history while the application is running.

---

### Database Layer

#### `base.py`

Defines the common interface that every database adapter must implement.

The interface currently includes operations such as:

```python
connect()
disconnect()
test_connection()
get_schema()
execute()
```

#### `models.py`

Contains common database metadata models such as:

* `ColumnInfo`
* `ForeignKeyInfo`
* `TableInfo`
* `DatabaseSchema`

These models provide a database-independent representation of schema information.

#### `postgres.py`

Implements the `DatabaseAdapter` interface for PostgreSQL using SQLAlchemy.

The PostgreSQL adapter currently supports:

* Database connection
* Connection testing
* Schema introspection
* Table metadata retrieval
* Column metadata retrieval
* Primary key detection
* Foreign key detection
* Query execution

---

## Technology Stack

### AI

* Python
* Google Gemini API
* google-genai

### Database

* PostgreSQL
* SQLAlchemy
* Psycopg

### Configuration

* python-dotenv

### Planned

* MySQL
* SQLite
* MongoDB
* Database-independent query planning
* Query validation
* Query correction and retry
* Improved conversational context

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd text2sql
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key

DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/text2sql
```

Do not commit `.env` to GitHub.

Add it to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## PostgreSQL Setup

Create a PostgreSQL database:

```text
text2sql
```

For the current development setup, the database contains a `student` table:

```sql
CREATE TABLE student (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50),
    address VARCHAR(100),
    cgpa NUMERIC(5,2)
);
```

You can populate it with test data:

```sql
INSERT INTO student
(id, name, email, address, cgpa)
VALUES
(1, 'Rahul', 'rahul@example.com', 'Kolkata', 8.7),
(2, 'Aman', 'aman@example.com', 'Delhi', 9.1),
(3, 'Priya', 'priya@example.com', 'Mumbai', 8.3);
```

---

## Running the Project

Start the application with:

```bash
python main.py
```

The application will connect to PostgreSQL and start the conversational interface.

Example:

```text
"/start" -> Start the conversation
"/q" -> Exit

Ask your question: Get students with CGPA above 8
```

The agent may generate:

```sql
SELECT *
FROM student
WHERE cgpa > 8;
```

The query is then passed to the PostgreSQL adapter for execution.

---

## Example: Clarification

### User

```text
Get the best student
```

### Agent

```text
What should "best" mean? Should I use the highest CGPA?
```

### User

```text
Yes, highest CGPA
```

### Generated SQL

```sql
SELECT *
FROM student
ORDER BY cgpa DESC
LIMIT 1;
```

### Result

```text
(2, 'Aman', 'aman@example.com', 'Delhi', Decimal('9.10'))
```

---

## Design Philosophy

The project follows a few important architectural principles.

### Separation of AI and Database Logic

The AI components should not directly know how PostgreSQL works.

Instead:

```text
AI
 │
 ▼
DatabaseAdapter
 │
 ▼
Database
```

This allows the same AI layer to work with different database technologies.

### Common Schema Representation

Database-specific metadata is converted into common models:

```text
PostgreSQL ──┐
MySQL ───────┤
SQLite ──────┼──► DatabaseSchema
MongoDB ─────┘
```

This allows the AI layer to reason about databases without depending on a specific database implementation.

### Conversation State Belongs to the Application

The application owns the temporary conversation context.

```text
Application
    │
    └── ConversationContext
             │
             ├── User messages
             └── Assistant messages
```

The context exists only during the active conversation.

---

## Security Considerations

The current project is intended for development and experimentation.

LLM-generated queries should **not** be blindly executed against production databases.

Before using this system with sensitive or production data, the project should implement:

* Read-only database credentials
* SQL statement validation
* Allowed-operation restrictions
* Query timeouts
* Result-size limits
* Permission boundaries
* Protection against destructive SQL
* Sensitive-data handling

A future version will introduce a dedicated query validation layer between the LLM and the database adapter.

---

## Project Goal

The long-term goal is to build a reusable **AI database agent** capable of interacting with different database technologies through natural language while maintaining a clean separation between:

```text
Conversation
     │
     ▼
Intent Understanding
     │
     ▼
Clarification
     │
     ▼
Database-Independent Query Plan
     │
     ▼
Database-Specific Query Generation
     │
     ▼
Validation
     │
     ▼
Database Adapter
     │
     ▼
Results
```

The current implementation is the foundation for this architecture, starting with PostgreSQL.

---