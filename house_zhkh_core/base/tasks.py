from django.utils import timezone
from celery import Task, shared_task

from base.models.models import Flat, Payment
from base.controllers.payment_controllers.payment_calculator.payment_calculator import PaymentCalculator

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
