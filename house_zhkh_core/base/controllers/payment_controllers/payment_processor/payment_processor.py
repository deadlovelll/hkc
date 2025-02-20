from datetime import datetime

from base.models.flat import Flat
from base.models.payment import Payment
from base.controllers.payment_controllers.payment_calculator.payment_calculator import PaymentCalculator

class PaymentProcessor:
    
    """
    Processes payment calculations for all apartments.

    This class retrieves all apartments from the database, calculates their respective 
    fees using `PaymentCalculator`, and creates `Payment` records for the given month.
    """

    def __init__ (
        self, 
        water_rate: float, 
        common_area_rate: float,
    ) -> None:
        
        """
        Initializes the payment processor with specified rates.

        Args:
            water_rate (float): The cost per unit of water consumption.
            common_area_rate (float): The cost per unit area for common area maintenance.
        """
        
        self.calculator = PaymentCalculator (
            water_rate, 
            common_area_rate,
        )

    def process_payments (
        self, 
        month_date: datetime, 
        prev_month_date: datetime,
    ) -> list:
        
        """
        Iterates through all apartments, calculates fees using `PaymentCalculator`,
        and creates `Payment` records in the database.

        For each apartment, this method:
        1. Retrieves water meter readings for the current and previous months.
        2. Calculates water and common area fees.
        3. Creates a `Payment` record in the database.
        4. Collects and returns a list of created `Payment` objects.

        Args:
            month_date (datetime): The current month as a datetime object.
            prev_month_date (datetime): The previous month as a datetime object.

        Returns:
            list: A list of created `Payment` objects.
                  If no payments are created due to missing data, an empty list is returned.
        """
        
        flats = Flat.objects.all()
        created_payments = []
        
        for apartment in flats:
            fees = self.calculator.calculate_fees (
                apartment, 
                month_date, 
                prev_month_date,
            )
            if fees is None:
                continue

            payment = Payment.objects.create (
                apartment=apartment,
                month=month_date,
                water_fee=fees['water_fee'],
                common_area_fee=fees['common_area_fee'],
                total_fee=fees['total_fee'],
            )
            created_payments.append(payment)
        return created_payments