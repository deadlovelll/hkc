from django.utils import timezone
from celery import Task, shared_task
from house_zhkh.base.models.models import Flat, Payment

class PaymentCalculator:
    
    """
    Responsible for calculating payment amounts for a given flat.
    """
    
    def __init__ (
        self
    ) -> None:
        
        self.water_rate = 10  
        self.maintenance_rate = 5

    def calculate_for_flat (
        self, 
        flat
    ) -> dict:
        
        """
        Calculates water fee, common area fee, and total fee for a given flat.

        Args:
            flat (Flat): The flat for which to calculate the payment.

        Returns:
            dict: A dictionary with the calculated fees.
        """
        
        water_usage = 0.0
        # Assuming that the related name for counters in Flat is `counters`
        for counter in flat.counters.all():
            if counter.last_reading is not None and counter.current_reading is not None:
                monthly_usage = counter.current_reading - counter.last_reading
                water_usage += monthly_usage

        water_fee = water_usage * self.WATER_RATE
        common_area_fee = flat.square * self.MAINTENANCE_RATE
        total_fee = water_fee + common_area_fee

        return {
            'water_fee': water_fee,
            'common_area_fee': common_area_fee,
            'total_fee': total_fee,
        }


@shared_task(bind=True, name="calculate_payments", base=Task)
class CalculatePaymentsTask(Task):
    
    """
    Celery task to calculate and update payments for all flats for a given month.
    """

    def run (
        self, 
        month
    ) -> dict:
        
        """
        Executes the payment calculation for the provided month.

        Args:
            month (str): A string in the format 'YYYY-MM-01' representing the start of the month.

        Returns:
            dict: A result dictionary containing the task status and the processed month.
        """
        
        try:
            month_start = timezone.datetime.strptime(month, '%Y-%m-01')
        except ValueError as exc:
            raise ValueError("Invalid month format. Expected 'YYYY-MM-01'.") from exc

        # Calculate the end of the month by adding 31 days then rolling back to the last day.
        month_end = month_start + timezone.timedelta(days=31)
        month_end = month_end.replace(day=1) - timezone.timedelta(days=1)

        flats = Flat.objects.all()
        total_flats = flats.count()
        calculator = PaymentCalculator()

        for i, flat in enumerate(flats, start=1):
            payment_data = calculator.calculate_for_flat(flat)

            Payment.objects.update_or_create (
                flat=flat,
                month=month_start.date(),  # Payment.month is a DateField
                defaults=payment_data
            )

            # Update task state to report progress.
            self.update_state (
                state='PROGRESS',
                meta={'current': i, 'total': total_flats}
            )

        return {
            'status': 'completed', 
            'month': month
        }
