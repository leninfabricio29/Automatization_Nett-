"""
MongoDB configuration and connection setup.
Uses PyMongo driver.
Compatible MongoDB Compass.
"""

from pymongo import MongoClient
from pymongo.database import Database

from typing import Generator

from config.settings import get_settings


class DatabaseConfig:
    """MongoDB configuration and connection manager."""

    _client: MongoClient = None
    _database: Database = None

    @classmethod
    def initialize(cls) -> MongoClient:
        """
        Initialize MongoDB client and database.

        Returns:
            MongoClient: MongoDB client instance
        """
        if cls._client is None:
            settings = get_settings()

            cls._client = MongoClient(
                settings.mongodb_uri,          # misma URI que se usa en Compass
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                maxPoolSize=settings.db_pool_size,
                retryWrites=True
            )

            cls._database = cls._client[settings.mongodb_database]

        return cls._client

    @classmethod
    def get_client(cls) -> MongoClient:
        """Get MongoDB client."""
        if cls._client is None:
            cls.initialize()
        return cls._client

    @classmethod
    def get_database(cls) -> Database:
        """Get MongoDB database."""
        if cls._database is None:
            cls.initialize()
        return cls._database

    @classmethod
    
    def get_db(cls) -> Generator[Database, None, None]:
        """
        Context manager for MongoDB access.

        Usage:
            with DatabaseConfig.get_db() as db:
                collection = db["users"]
                collection.insert_one({...})
        """
        db = cls.get_database()
        try:
            yield db
        except Exception:
            raise

    @classmethod
    def health_check(cls) -> bool:
        """
        Test MongoDB connection.

        Returns:
            bool: True if connection is successful
        """
        try:
            client = cls.get_client()
            client.admin.command("ping")
            return True
        except Exception as e:
            print(f"MongoDB health check failed: {e}")
            return False

    @classmethod
    def dispose(cls) -> None:
        """Close MongoDB connection."""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._database = None
