"""Database access layer for the LuminaText ETL application."""

from __future__ import annotations

from typing import Final, Optional

from pymongo import MongoClient
from pymongo.database import Database

from src.config import DATABASE_NAME, MONGO_URI

_client: Optional[MongoClient] = None
_database: Optional[Database] = None


def get_database() -> Database:
    """Return a shared PyMongo Database instance.

    The module caches the MongoClient and Database objects to avoid creating a
    new connection client on each call. This allows PyMongo to leverage its
    internal connection pool while keeping the access layer simple and
    deterministic.
    """
    global _client, _database

    if _database is None:
        _client = MongoClient(MONGO_URI)
        _database = _client[DATABASE_NAME]

    return _database


if __name__ == "__main__":
    try:
        database = get_database()
        database.client.admin.command("ping")
        print("MongoDB connection successful.")
    except Exception as exc:
        print(f"MongoDB connection failed: {exc}")
