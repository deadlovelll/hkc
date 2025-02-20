from modules.database.database import Database
from modules.logger.logger import LoggerInitializer

class DatabasePoolControllers:
    
    def __init__ (
        self,
    ) -> None:
        
        self.logger = LoggerInitializer.init_logger()
        self.db = None
    
    def get_db (
        self,
    ) -> Database:
        
        if self.db is None:
            self.db = Database()  # Instantiate Database when needed
        return self.db

    async def startup_event (
        self,
    ) -> None:
        
        self.logger.info('Starting App')
        
        try:
            db = self.get_db()
            db.connect()
            self.logger.info('Database Pool Started Succesfully')
            
        except Exception as e:
            self.logger.fatal(f'Failed to start the database pool: {e}. Application would be stopped. Full traceback below.', exc_info=True)
            raise e
    
    async def shutdown_event (
        self,
    ) -> None:
        
        try:
            if self.db.pool:
                self.logger.info('Shutdown made succesfully')
                self.db.close_all()
            
        except Exception as e:
            self.logger.fatal(f'Failed to close the database pool: {e}. Application would be stopped. Full traceback below.', exc_info=True)
            raise e