"""
Database configuration and connection setup.
Uses SQLAlchemy with PostgreSQL driver (psycopg).
"""

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from typing import Generator

from config.settings import get_settings


class DatabaseConfig:
    """Database configuration and connection manager."""
    
    _engine: Engine = None
    _session_factory: sessionmaker = None
    
    @classmethod
    def initialize(cls) -> Engine:
        """
        Initialize database engine and session factory.
        
        Returns:
            Engine: SQLAlchemy engine instance
        """
        if cls._engine is None:
            settings = get_settings()
            
            cls._engine = create_engine(
                settings.database_url,
                poolclass=QueuePool,
                pool_size=settings.db_pool_size,
                max_overflow=settings.db_max_overflow,
                echo=settings.is_debug,  # Log SQL queries in debug mode
                connect_args={
                    "connect_timeout": 10,
                    "options": "-c statement_timeout=30000"
                }
            )
            
            cls._session_factory = sessionmaker(
                bind=cls._engine,
                expire_on_commit=False,
                autoflush=False
            )
        
        return cls._engine
    
    @classmethod
    def get_engine(cls) -> Engine:
        """Get the database engine instance."""
        if cls._engine is None:
            cls.initialize()
        return cls._engine
    
    @classmethod
    def get_session_factory(cls) -> sessionmaker:
        """Get the session factory."""
        if cls._session_factory is None:
            cls.initialize()
        return cls._session_factory
    
    @classmethod
    @contextmanager
    def get_session(cls) -> Generator[Session, None, None]:
        """
        Context manager for database sessions.
        
        Usage:
            with DatabaseConfig.get_session() as session:
                # Use session
                pass
        """
        session = cls.get_session_factory()()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    @classmethod
    def health_check(cls) -> bool:
        """
        Test database connection.
        
        Returns:
            bool: True if connection is successful
        """
        try:
            engine = cls.get_engine()
            with engine.connect() as connection:
                connection.execute("SELECT 1")
            return True
        except Exception as e:
            print(f"Database health check failed: {e}")
            return False
    
    @classmethod
    def dispose(cls) -> None:
        """Close all database connections."""
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None
