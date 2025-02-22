import os

from typing import Any, Optional

import psycopg2


class Database:
    
    """
    Singleton class responsible for managing a PostgreSQL connection pool.
    
    This class provides methods to connect to the database, retrieve a connection, 
    release a connection back to the pool, and close all connections. 
    It ensures that only one instance of the connection pool is used across the application.

    Attributes:
        instance (Database, optional): The singleton instance of the class.
        pool (psycopg2.pool.SimpleConnectionPool, optional): The connection pool for PostgreSQL connections.
    """

    instance: Optional["Database"] = None
    
    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the Database instance with database connection credentials
        retrieved from environment variables.
        
        Attributes:
            host (str): The host address of the database server.
            db_user (str): The database user.
            password (str): The password for the database user.
            database (str): The name of the database to connect to.
        """
        
        self.host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
    
    def __new__ (
        cls,
    ) -> "Database":
        
        """
        Ensures that only one instance of the Database class is created (Singleton pattern).

        Returns:
            Database: The singleton instance of the Database class.
        """
        
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.pool = None
            
        return cls.instance
    
    def connect (
        self,
    ) -> None:
        
        """
        Establishes a connection pool to the PostgreSQL database if it does not already exist.
        
        Uses `psycopg2`'s `SimpleConnectionPool` to create a pool with a minimum of 1 connection 
        and a maximum of 20 connections.
        """
        
        if self.pool is None:
            self.pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,  # minconn, maxconn
                host=self.host,
                user=self.db_user,
                password=self.password,
                database=self.database,
            )
    
    def get_connection (
        self,
    ) -> Any:
        
        """
        Retrieves a connection from the connection pool.
        
        If the pool is not initialized, it will first establish a connection pool.
        
        Returns:
            Any: A connection object from the PostgreSQL connection pool.
        
        Raises:
            Exception: If the pool is not initialized and cannot be connected to.
        """
        
        if self.pool is None:
            self.connect()
        
        return self.pool.getconn()
    
    def release_connection (
        self, 
        connection
    ) -> None:
        
        """
        Releases a connection back to the connection pool.
        
        Args:
            connection (Any): The connection object to be returned to the pool.
        """
        
        self.pool.putconn(connection)
    
    def close_all (
        self,
    ) -> None:
        
        """
        Closes all connections in the connection pool.
        
        This method should be called when the application is shutting down to ensure
        all database connections are closed properly.
        """
        
        if self.pool:
            self.pool.closeall()
