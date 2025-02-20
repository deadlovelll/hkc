from datetime import datetime

from base.models.flat import Flat
from base.models.water_meter import WaterMeter

class PaymentCalculator:
    
    """
    Responsible for calculating fees for a single apartment based on water consumption.
    
    This class computes water fees, common area fees, and total fees for a given apartment
    by comparing water meter readings from the current and previous month. It uses the provided
    water and common area rates to calculate the fees.
    """

    def __init__ (
        self, 
        water_rate: float, 
        common_area_rate: float,
    ) -> None:
        
        """
        Initialize the PaymentCalculator with specified rates.

        Args:
            water_rate (float): The cost per unit of water consumption.
            common_area_rate (float): The cost per unit area for common areas.
        """
        
        self.water_rate = water_rate
        self.common_area_rate = common_area_rate

    def calculate_fees (
        self, 
        apartment: Flat, 
        month_date: datetime, 
        prev_month_date: datetime,
    ) -> dict:
        
        """
        Calculate water, common area, and total fees for the provided apartment.

        This method retrieves the water meter readings for the current and previous month
        for the given apartment. It computes the water consumption as the difference between
        the current and previous readings. The water fee is calculated by multiplying the 
        consumption by the water rate. The common area fee is calculated by multiplying the 
        apartment's square footage by the common area rate. The total fee is the sum of both.
        If either the current or previous water reading is missing, the method returns None.

        Args:
            apartment (Flat): The apartment for which to calculate fees.
            month_date (datetime): The datetime object representing the current month.
            prev_month_date (datetime): The datetime object representing the previous month.

        Returns:
            dict: A dictionary containing:
                - 'water_fee': Calculated fee for water consumption.
                - 'common_area_fee': Calculated fee for common area usage.
                - 'total_fee': Sum of water and common area fees.
            If either the current or previous water reading is missing, returns None.
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

