from django.test import TestCase
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient
from django.urls import reverse

class PaymentCalculationViewTest(TestCase):
    
    """
    Test suite for the PaymentCalculationView API.
    """

    def setUp (
        self,
    ) -> None:
        
        self.client = APIClient()
        self.url = reverse('calculate-payments')
    
    @patch('base.views.views.PaymentCalculationView.post', return_value=[MagicMock(), MagicMock()])
    def test_payment_calculation_success (
        self, 
        mock_process_payments,
    ) -> None:
        
        response = self.client.post(self.url, {'month': '2024-02'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['CREATED_PAYMENTS'], 2)
    
    def test_missing_month_field (
        self,
    ) -> None:
        
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn('ERROR', response.data)

class CalculatePaymentsViewTest(TestCase):
    
    """
    Test suite for the CalculatePaymentsView API.
    """
    
    def setUp (
        self,
    ) -> None:
        
        self.client = APIClient()
        self.url = reverse('trigger-payment-task')
    
    @patch('base.views.views.CalculatePaymentsView.post', return_value=MagicMock(id='task_123'))
    def test_task_triggered_successfully (
        self, 
        mock_task
    ) -> None:
        
        response = self.client.post(self.url, {'month': '2024-02'})
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data['TASK_ID'], 'task_123')

class TaskStatusViewTest(TestCase):
    
    """
    Test suite for the TaskStatusView API.
    """

    def setUp (
        self,
    ) -> None:
        
        self.client = APIClient()
        self.url = reverse('task-status', kwargs={'task_id': 'task_123'})
    
    @patch('base.views.views.TaskStatusView.get')
    def test_task_status_retrieval (
        self, 
        mock_async_result,
    ) -> None:
        
        mock_async_result.return_value.state = 'SUCCESS'
        mock_async_result.return_value.info = {'current': 1, 'total': 2}
        mock_async_result.return_value.result = 'Completed'
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['STATE'], 'SUCCESS')
        self.assertEqual(response.data['RESULT'], 'Completed')
