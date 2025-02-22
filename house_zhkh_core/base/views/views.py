from datetime import datetime, timedelta
from typing import Any, List, Dict

from celery.result import AsyncResult
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from base.tasks import CalculatePaymentsTask
from base.controllers.payment_controllers.payment_processor.payment_processor import PaymentProcessor
from base.models.payment import Payment

class PaymentCalculationView(APIView):
    
    """
    API view to calculate payments for apartments based on water consumption.
    
    This view expects a POST request with a 'month' field in the format 'YYYY-MM'. 
    It calculates the payments for the provided month and returns the number of created payments.
    """
    
    def __init__ (
        self, 
        **kwargs: Any,
    ) -> None:
        
        """
        Initialize the PaymentCalculationView.
        
        Sets default water and common area rates, and creates an instance of PaymentProcessor 
        with those rates.
        
        Args:
            **kwargs: Additional keyword arguments passed to the base APIView.
        """
        
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
        
        """
        Calculate payments for a specified month.
        
        The view expects a JSON payload containing a "month" key with the value formatted as 'YYYY-MM'.
        It parses the month, calculates the previous month's date, and processes payments via the
        PaymentProcessor. The response includes the status, a success message, and the number of payments created.
        
        Args:
            request (Request): The HTTP request object containing the 'month' data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        
        Returns:
            Response: A JSON response with:
                - 'STATUS': A string indicating success.
                - 'MESSAGE': A message indicating successful payment calculation.
                - 'CREATED_PAYMENTS': An integer representing the number of payments created.
                
            If the "month" field is missing, returns a 400 Bad Request.
            If an exception occurs during processing, returns a 500 Internal Server Error with an error message.
        """
        
        month: str = request.data.get("month")
        if not month:
            return Response (
                {
                    'ERROR': 'Month is required'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            month_date = datetime.strptime(month, '%Y-%m')
            prev_month_date = month_date - timedelta(days=month_date.day)

            created_payments: List[Payment] = self.payment_processor.process_payments (
                month_date, 
                prev_month_date,
            )

            return Response (
                {
                    'STATUS': 'success',
                    'MESSAGE': 'Payments calculated successfully.',
                    'CREATED_PAYMENTS': len(created_payments),
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response (
                {
                    'ERROR': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CalculatePaymentsView(APIView):
    
    """
    API view to trigger asynchronous calculation of payments for a given month.

    This view accepts a POST request containing a 'month' parameter in the request body.
    It then enqueues a Celery task to calculate the payments for that month and returns
    the task's unique identifier for tracking purposes.
    """
    
    def post (
        self, 
        request: Request,
    ) -> Response:
        
        """
        Initiate the calculation of payments asynchronously.

        Expects:
            A POST request with a JSON payload containing:
                - "month" (str): The month for which to calculate payments.

        Returns:
            Response: A JSON response with the key 'TASK_ID' containing the ID of the enqueued task,
            and an HTTP 202 Accepted status code.
        """
        
        month: str = request.data.get('month')
        task = CalculatePaymentsTask.delay(month)
        
        return Response (
            {
                'TASK_ID': task.id
            }, 
            status=status.HTTP_202_ACCEPTED
        )


class TaskStatusView(APIView):
    
    """
    API view to check the status of an asynchronous Celery task.

    This view accepts a GET request with a task_id parameter and returns the current state,
    progress, and result of the corresponding Celery task.
    """
    
    def get (
        self, 
        request: Request, 
        task_id: str,
    ) -> Response:
        
        """
        Retrieve the status of an asynchronous task.

        Args:
            request (Request): The incoming HTTP request.
            task_id (str): The unique identifier of the Celery task.

        Returns:
            Response: A JSON response containing:
                - "STATE": The current state of the task.
                - "CURRENT": The current progress count (if available; otherwise 0).
                - "TOTAL": The total expected count (if available; otherwise 1).
                - "RESULT": The task result if available, or None if pending.
        """

        task_result = AsyncResult(task_id)

        response: Dict[str, Any] = {
            'STATE': task_result.state,
            'CURRENT': task_result.info.get('current', 0)
            if task_result.state != 'PENDING'
            else 0,
            'TOTAL': task_result.info.get('total', 1)
            if task_result.state != 'PENDING'
            else 1,
            'RESULT': task_result.result if task_result.state != 'PENDING' else None,
        }

        return Response(response)
