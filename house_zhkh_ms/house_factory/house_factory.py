from typing import Dict, Any, List, Tuple


class HouseFactory:
    
    """
    Factory class for processing raw database rows into structured house data.
    """

    @staticmethod
    def create_house (
        rows: List[Tuple],
    ) -> Dict[str, Any]:
        
        """
        Creates a structured house representation from database query results.

        Args:
            rows (List[Tuple]): The raw data from the database query.

        Returns:
            Dict[str, Any]: A structured representation of house information.
        """

        result = {"house_id": None, "flats": {}}

        for row in rows:
            (
                house_id, flat_id, flat_number, flat_floor, square,
                counter_id, counter_type, count,
                counter_history_id, counter_date, counter_history_count,
                inhabitant_id, full_name, age, balance
            ) = row

            if result["house_id"] is None:
                result["house_id"] = house_id

            if flat_number not in result["flats"]:
                result["flats"][flat_number] = HouseFactory._create_flat (
                    flat_id, 
                    flat_number, 
                    flat_floor, 
                    square, 
                    balance,
                )

            if counter_id:
                result["flats"][flat_number]["counters"].append (
                    HouseFactory._create_counter (
                        counter_id, 
                        counter_type, 
                        count,
                    )
                )

            if counter_history_id:
                result["flats"][flat_number]["counter_history"].append (
                    HouseFactory._create_counter_history (
                        counter_history_id, 
                        counter_date, 
                        counter_history_count,
                    )
                )

            if inhabitant_id:
                HouseFactory._add_inhabitant (
                    result["flats"][flat_number]["inhabitants"], 
                    inhabitant_id, 
                    full_name, 
                    age,
                )

        return result

    @staticmethod
    def _create_flat (
        flat_id: int, 
        flat_number: int, 
        flat_floor: int, 
        square: float, 
        balance: float,
    ) -> Dict[str, Any]:
        
        """
        Creates a flat dictionary.

        Args:
            flat_id (int): Flat ID.
            flat_number (int): Flat number.
            flat_floor (int): Floor number.
            square (float): Flat area.
            balance (float): Balance for the flat.

        Returns:
            Dict[str, Any]: Structured flat information.
        """
        
        return {
            "flat_id": flat_id,
            "flat_number": flat_number,
            "flat_floor": flat_floor,
            "square": square,
            "counters": [],
            "counter_history": [],
            "inhabitants": [],
            "balance": balance,
        }

    @staticmethod
    def _create_counter (
        counter_id: int, 
        counter_type: str, 
        count: float,
    ) -> Dict[str, Any]:
        
        """
        Creates a counter dictionary.

        Args:
            counter_id (int): Counter ID.
            counter_type (str): Type of counter.
            count (float): Counter value.

        Returns:
            Dict[str, Any]: Structured counter information.
        """
        
        return {
            "id": counter_id, 
            "counter_type": counter_type, 
            "count": count
        }

    @staticmethod
    def _create_counter_history (
        counter_history_id: int, 
        date: str, 
        count: float,
    ) -> Dict[str, Any]:
        
        """
        Creates a counter history entry.

        Args:
            counter_history_id (int): Counter history ID.
            date (str): Date of reading.
            count (float): Counter reading.

        Returns:
            Dict[str, Any]: Structured counter history information.
        """
        
        return {
            "id": counter_history_id, 
            "date": date, 
            "count": count
        }

    @staticmethod
    def _add_inhabitant (
        inhabitants: List[Dict[str, Any]], 
        inhabitant_id: int, 
        full_name: str, 
        age: int,
    ) -> None:
        
        """
        Adds an inhabitant to the list if not already present.

        Args:
            inhabitants (List[Dict[str, Any]]): The list of inhabitants.
            inhabitant_id (int): Inhabitant ID.
            full_name (str): Full name of the inhabitant.
            age (int): Age of the inhabitant.
        """
        
        if not any (
            inhabitant["id"] == inhabitant_id for inhabitant in inhabitants
        ):
            inhabitants.append (
                {
                    "id": inhabitant_id,
                    "full_name": full_name or f"Житель {inhabitant_id}",
                    "age": age
                }
            )
