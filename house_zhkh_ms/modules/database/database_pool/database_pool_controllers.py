from house_zhkh_ms.modules.database.database.database import Database
from modules.logger.logger import LoggerInitializer

class DatabasePoolControllers:
    
    """
    Manages the database connection pool, handling startup and shutdown events.
    Ensures the database pool is initialized and closed properly during application lifecycle events.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the DatabasePoolControllers instance, setting up the logger and database connection.

        Attributes:
            logger (Logger): The logger instance to log events and errors.
            db (Database, optional): The database instance, initially set to None until needed.
        """
        
        self.logger = LoggerInitializer.init_logger()
        self.db = None

    def get_db (
        self,
    ) -> Database:
        
        """
        Retrieves the database connection, initializing it if it does not already exist.

        Returns:
            Database: The database connection instance.

        Notes:
            The method ensures that only one database connection is instantiated during the application's lifecycle.
        """
        
        if self.db is None:
            self.db = Database()  
        return self.db

    async def startup_event (
        self,
    ) -> None:
        
        """
        Handles the startup event for the application, initializing and connecting the database pool.

        Logs the successful initialization of the database pool or logs a fatal error and raises an exception if the connection fails.

        Raises:
            Exception: If the database pool fails to start, the exception is raised and the application stops.
        """
        
        self.logger.info('Starting App')

        try:
            db = self.get_db()
            db.connect()
            self.logger.info('Database Pool Started Successfully')

        except Exception as e:
            self.logger.fatal (
                f'Failed to close the database pool: {e}. 
                Application would be stopped. Full traceback below.', 
                exc_info=True
            )
            raise e

    async def shutdown_event (
        self,
    ) -> None:
        
        """
        Handles the shutdown event for the application, closing the database pool connections.

        Ensures all connections are closed properly before the application shuts down.

        Raises:
            Exception: If the database pool fails to close properly, the exception is raised and the application stops.
        """
        
        try:
            if self.db.pool:
                self.logger.info('Shutdown made successfully')
                self.db.close_all()

        except Exception as e:
            self.logger.fatal (
                f'Failed to close the database pool: {e}. 
                Application would be stopped. Full traceback below.', 
                exc_info=True
            )
            raise e
