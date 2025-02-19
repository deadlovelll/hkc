from datetime import datetime, timedelta
from typing import Any, List, Dict

from celery.result import AsyncResult
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from house_zhkh.base.celery.tasks import calculate_payments
from house_zhkh.base.controllers.payment_controllers.payment_processor.payment_processor import PaymentProcessor
from house_zhkh.base.models.models import Payment

class PaymentCalculationView(APIView):
    
    """
    API view to calculate payments for apartments based on water consumption.
    Expects a POST request with a 'month' field in the format 'YYYY-MM'.
    """
    
    def __init__ (
        self, 
        **kwargs: Any,
    ) -> None:
        
        super().__init__(**kwargs)
        
        self.water_rate: int = 10
        self.common_area_rate: int = 5
        self.payment_processor: PaymentProcessor = PaymentProcessor (
            self.water_rate, 
            self.common_area_rate
        )

    def post (
        self, 
        request: Request, 
        *args: Any, 
        **kwargs: Any,
    ) -> Response:
        
        month: str = request.data.get("month")
        if not month:
            return Response (
                {
                    'error': 'Month is required'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Parse the month string into a datetime object.
            month_date = datetime.strptime(month, '%Y-%m')
            # Calculate the previous month date by subtracting the current day count.
            prev_month_date = month_date - timedelta(days=month_date.day)

            created_payments: List[Payment] = self.payment_processor.process_payments (
                month_date, 
                prev_month_date,
            )

            return Response (
                {
                    'status': 'success',
                    'message': 'Payments calculated successfully.',
                    'created_payments': len(created_payments),
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response (
                {
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CalculatePaymentsView(APIView):
    
    def post (
        self, 
        request: Request,
    ) -> Response:
        
        month: str = request.data.get("month")
        task = calculate_payments.delay(month)
        
        return Response (
            {
                'task_id': task.id
            }, 
            status=status.HTTP_202_ACCEPTED
        )


class TaskStatusView(APIView):
    
    def get (
        self, 
        request: Request, 
        task_id: str,
    ) -> Response:

        task_result = AsyncResult(task_id)

        response: Dict[str, Any] = {
            "state": task_result.state,
            "current": task_result.info.get("current", 0)
            if task_result.state != "PENDING"
            else 0,
            "total": task_result.info.get("total", 1)
            if task_result.state != "PENDING"
            else 1,
            "result": task_result.result if task_result.state != "PENDING" else None,
        }

        return Response(response)
