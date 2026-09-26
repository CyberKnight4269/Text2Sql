from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ColumnInfo:
    name: str
    data_type: str
    nullable: bool = True
    primary_key: bool = False
    default: Optional[str] = None


@dataclass
class ForeignKeyInfo:
    column: str
    referenced_table: str
    referenced_column: str


@dataclass
class TableInfo:
    name: str
    columns: list[ColumnInfo] = field(default_factory=list)
    primary_keys: list[str] = field(default_factory=list)
    foreign_keys: list[ForeignKeyInfo] = field(default_factory=list)


@dataclass
class DatabaseSchema:
    database_type: str
    database_name: str
    tables: list[TableInfo] = field(default_factory=list)