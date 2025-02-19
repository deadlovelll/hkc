from datetime import datetime

from base.models.models import Flat, WaterMeter

class PaymentCalculator:
    
    """
    Responsible for calculating fees for a single apartment based on water consumption.
    """

    def __init__ (
        self, 
        water_rate: float, 
        common_area_rate: float,
    ) -> None:
        
        self.water_rate = water_rate
        self.common_area_rate = common_area_rate

    def calculate_fees (
        self, 
        apartment: Flat, 
        month_date: datetime, 
        prev_month_date: datetime,
    ) -> dict:
        
        """
        Calculates water, common area, and total fees for the provided apartment.

        Args:
            apartment (Flat): The apartment for which to calculate fees.
            month_date (datetime): The current month as a datetime object.
            prev_month_date (datetime): The previous month as a datetime object.

        Returns:
            dict: A dictionary containing calculated fees. If readings are missing, returns None.
        """
        
        current_reading = WaterMeter.objects.filter (
            apartment=apartment, month=month_date
        ).first()
        previous_reading = WaterMeter.objects.filter (
            apartment=apartment, month=prev_month_date
        ).first()

        if not current_reading or not previous_reading:
            return None

        water_consumption = current_reading.reading - previous_reading.reading
        water_fee = self.water_rate * water_consumption if water_consumption > 0 else 0
        common_area_fee = self.common_area_rate * apartment.square
        total_fee = water_fee + common_area_fee

        return {
            'water_fee': water_fee,
            'common_area_fee': common_area_fee,
            'total_fee': total_fee,
        }

