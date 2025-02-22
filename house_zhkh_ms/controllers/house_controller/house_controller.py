from fastapi.responses import JSONResponse

from psycopg2 import (
    DatabaseError, 
    OperationalError, 
    IntegrityError, 
    InterfaceError, 
    ProgrammingError, 
    DataError,
)

from controllers.base_controller.base_controller import BaseController  
from house_zhkh_ms.house_factory.house_factory import HouseFactory  
from modules.database.database_pool_controllers import DatabasePoolControllers  
from modules.logger.logger import LoggerInitializer  

class HouseController(BaseController):
    
    def __init__ (
        self,
    ) -> None:
        
        super().__init__()
        
        self.db = DatabasePoolControllers()
        self.house_factory = HouseFactory()
        
        self.logger = LoggerInitializer.init_logger()

    async def get (
        self, 
        house_street: str,
    ) -> JSONResponse:
        
        """
        Fetches house information based on the street name.

        Args:
            house_street (str): The street name to query.

        Returns:
            JSONResponse: API response containing house data or an error message.
        """

        query = """
            SELECT 
                bb.id AS house_id, 
                bf.id AS flat_id, bf.flat_number, bf.flat_floor, bf.square,
                bc.id AS counter_id, bc.counter_type, bc.count,
                bch.id AS counter_history_id, bch.date, bch.count AS counter_history_count,
                bi.id AS inhabitant_id, bi.full_name, bi.age,
                bfb.balance
            FROM base_building AS bb
            LEFT JOIN base_flat bf ON bf.building_id = bb.id
            LEFT JOIN base_counter bc ON bc.corresponding_flat_id = bf.id
            LEFT JOIN base_counterhistory bch ON bch.corresponding_counter_id = bc.id
            LEFT JOIN base_inhabitant bi ON bi.living_at_flat_id = bf.id
            LEFT JOIN base_flathcsbalance bfb ON bfb.flat_id = bf.id
            WHERE bb.address = %s
            GROUP BY 
                bb.id, bf.id, bf.flat_number, bf.flat_floor, bf.square,
                bc.id, bc.counter_type, bc.count,
                bch.id, bch.date, bch.count,
                bi.id, bi.full_name, bi.age,
                bfb.balance;
        """

        try:
            with self.db.get_connection() as connection:
                cursor = connection.cursor()
                self.logger.info(f'Fetching house info for: {house_street}')

                cursor.execute (
                    query, 
                    (house_street,),
                )
                rows = cursor.fetchall()

                if not rows:
                    self.logger.warning(f'No house found for address: {house_street}')
                    
                    return JSONResponse (
                        {
                            'STATUS': 'FAILED', 
                            'MESSAGE': 'House not found',
                        }
                    )

                response_data = self.house_factory.create_house(rows)
                connection.commit()

                return JSONResponse (
                    {
                        'STATUS': 'SUCCESS', 
                        'HOUSE INFO': response_data,
                    }
                )

        except (
            DatabaseError, 
            OperationalError, 
            IntegrityError, 
            InterfaceError, 
            ProgrammingError, 
            DataError, 
            Exception,
        ) as e:
            
            self.logger.error(f"Database error for '{house_street}': {e}", exc_info=True)
            
            return JSONResponse (
                {
                    'STATUS': 'FAILED', 
                    'MESSAGE': 'Internal Server Error',
                }
            )
            
    async def create (
        self, 
        house_street: str,
    ) -> JSONResponse:
        
        """
        Fetches house information based on the street name.

        Args:
            house_street (str): The street name to query.

        Returns:
            JSONResponse: API response containing house data or an error message.
        """
        
        query = """
            INSERT INTO base_building (address) 
            VALUES (%s) 
            RETURNING id
        """

        try:
            with self.db.get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute (
                    query, 
                    (house_street,),
                )
                house_id = cursor.fetchone()[0]  
                connection.commit()
            
            return JSONResponse (
                {
                    'STATUS': 'SUCCESS', 
                    'HOUSE_ID': house_id,
                }
            )

        except (
            DatabaseError, 
            OperationalError, 
            IntegrityError, 
            InterfaceError, 
            ProgrammingError, 
            DataError, 
            Exception,
        ) as e:
            
            self.logger.error(f'Database error occurred: {e}', exc_info=True)
            
            return JSONResponse (
                {
                    'STATUS': 'FAILED', 
                    'MESSAGE': 'Internal Server Error',
                }
            )