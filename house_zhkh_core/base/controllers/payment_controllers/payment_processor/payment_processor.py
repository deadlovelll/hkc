from datetime import datetime

from base.models.models import Flat, Payment
from base.controllers.payment_controllers.payment_calculator.payment_calculator import PaymentCalculator

class PaymentProcessor:
    
    """
    Processes payment calculations for all apartments.
    """

    def __init__ (
        self, 
        water_rate: float, 
        common_area_rate: float,
    ) -> None:
        
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
        Iterates through all apartments, calculates fees using PaymentCalculator,
        and creates Payment records.

        Args:
            month_date (datetime): The current month as a datetime object.
            prev_month_date (datetime): The previous month as a datetime object.

        Returns:
            list: A list of created Payment objects.
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