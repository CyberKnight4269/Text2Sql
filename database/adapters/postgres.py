from typing import Any

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine

from database.base import DatabaseAdapter
from database.models import (
    ColumnInfo,
    DatabaseSchema,
    ForeignKeyInfo,
    TableInfo,
)


class PostgreSQLAdapter(DatabaseAdapter):

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine: Engine | None = None

    def connect(self) -> None:
        self.engine = create_engine(self.database_url)

    def disconnect(self) -> None:
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None

    def test_connection(self) -> bool:
        if self.engine is None:
            self.connect()

        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception as error:
            print(f"Database connection failed: {error}")
            return False

    def get_schema(self) -> DatabaseSchema:
        if self.engine is None:
            self.connect()
        inspector = inspect(self.engine)
        database_name = self.engine.url.database
        tables = []
        for table_name in inspector.get_table_names():
            columns = []
            for column in inspector.get_columns(table_name):
                primary_key = False
                column_info = ColumnInfo(
                    name=column["name"],
                    data_type=str(column["type"]),
                    nullable=column["nullable"],
                    primary_key=primary_key,
                    default=str(column["default"])
                    if column["default"] is not None
                    else None,
                )
                columns.append(column_info)

            pk_constraint = inspector.get_pk_constraint(table_name)
            primary_keys = pk_constraint.get(
                "constrained_columns",
                []
            )
            for column in columns:
                if column.name in primary_keys:
                    column.primary_key = True

            foreign_keys = []
            for fk in inspector.get_foreign_keys(table_name):
                constrained_columns = fk.get(
                    "constrained_columns",
                    []
                )
                referred_columns = fk.get(
                    "referred_columns",
                    []
                )
                referred_table = fk.get(
                    "referred_table"
                )
                for column, referred_column in zip(
                    constrained_columns,
                    referred_columns
                ):
                    foreign_keys.append(
                        ForeignKeyInfo(
                            column=column,
                            referenced_table=referred_table,
                            referenced_column=referred_column,
                        )
                    )
            table_info = TableInfo(
                name=table_name,
                columns=columns,
                primary_keys=primary_keys,
                foreign_keys=foreign_keys,
            )
            tables.append(table_info)
        return DatabaseSchema(
            database_type="postgresql",
            database_name=database_name or "",
            tables=tables,
        )

    def execute(self, query: str) -> Any:
        if self.engine is None:
            self.connect()
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            if result.returns_rows:
                return result.fetchall()
            return None