from abc import ABC, abstractmethod
from typing import Any

from database.models import DatabaseSchema


class DatabaseAdapter(ABC):

    @abstractmethod
    def connect(self) -> None:
        """
        Establish a connection to the database.
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """
        Close the database connection.
        """
        pass

    @abstractmethod
    def get_schema(self) -> DatabaseSchema:
        """
        Return the database schema in our standardized format.
        """
        pass

    @abstractmethod
    def execute(self, query: str) -> Any:
        """
        Execute a query and return the result.
        """
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """
        Check whether the database connection is working.
        """
        pass