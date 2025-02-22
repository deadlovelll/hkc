from unittest.mock import MagicMock, patch  

from django.test import TestCase  
from django.utils import timezone  

from base.tasks import CalculatePaymentsTask  

class CalculatePaymentsTaskTest(TestCase):
    
    """
    Test suite for the CalculatePaymentsTask Celery task.
    """
    
    def test_calculate_payments_success (
        self,
    ) -> None:
        
        """
        Test that the task successfully calculates payments for all flats and updates the Payment model.
        """
        
        month = '2024-02-01'
        
        flats = [MagicMock(id=1), MagicMock(id=2)]
        calculator_mock = MagicMock()
        calculator_mock.calculate_for_flat.side_effect = [
            {'amount': 1000}, 
            {'amount': 1200},
        ]
        
        with patch('base.models.flat.Flat.objects.all', return_value=flats), \
            patch (
                'base.models.payment.Payment.objects.update_or_create',
            ) as mock_update_or_create, \
            patch (
                'base.controller.payment_calculator.payment_calculator.PaymentCalculator', 
                return_value=calculator_mock,
            ):
            
            task = CalculatePaymentsTask()
            result = task.run(month)
        
        self.assertEqual (
            result, 
            {'status': 'completed', 'month': month},
        )
        self.assertEqual (
            mock_update_or_create.call_count, 
            2,
        )
        
        mock_update_or_create.assert_any_call (
            flat=flats[0], 
            month=timezone.datetime(2024, 2, 1).date(), 
            defaults={'amount': 1000},
        )
        mock_update_or_create.assert_any_call (
            flat=flats[1], 
            month=timezone.datetime(2024, 2, 1).date(), 
            defaults={'amount': 1200},
        )

    def test_calculate_payments_invalid_month (
        self,
    ) -> None:
        
        """
        Test that the task raises a ValueError when given an invalid month format.
        """
        
        task = CalculatePaymentsTask()
        with self.assertRaises (
            ValueError, 
            msg="Invalid month format. Expected 'YYYY-MM-01'.",
        ):
            task.run('invalid-date')

    def test_calculate_payments_no_flats (
        self,
    ) -> None:
        
        """
        Test that the task completes successfully when there are no flats to process.
        """
        
        month = '2024-02-01'
        
        with patch('base.models.flat.Flat.objects.all', return_value=[]), \
             patch('base.models.payment.Payment.objects.update_or_create') as mock_update_or_create:
            
            task = CalculatePaymentsTask()
            result = task.run(month)
        
        self.assertEqual (
            result, 
            {'status': 'completed', 'month': month},
        )
        mock_update_or_create.assert_not_called()

    def test_calculate_payments_task_progress (
        self,
    ) -> None:
        
        """
        Test that the task updates its state correctly as it processes flats.
        """
        
        month = '2024-02-01'
        
        flats = [MagicMock(id=1), MagicMock(id=2)]
        calculator_mock = MagicMock()
        calculator_mock.calculate_for_flat.return_value = {'amount': 1000}
        
        with patch('base.models.flat.Flat.objects.all', return_value=flats), \
             patch('base.models.payment.Payment.objects.update_or_create'), \
             patch('base.tasks.CalculatePaymentsTask', return_value=calculator_mock), \
             patch.object(CalculatePaymentsTask, 'update_state') as mock_update_state:
            
            task = CalculatePaymentsTask()
            result = task.run(month)
        
        self.assertEqual (
            result, 
            {'status': 'completed', 'month': month},
        )
        self.assertEqual (
            mock_update_state.call_count, 
            2,
        )
        
        mock_update_state.assert_any_call (
            state='PROGRESS', 
            meta={'current': 1, 'total': 2},
        )
        mock_update_state.assert_any_call (
            state='PROGRESS', 
            meta={'current': 2, 'total': 2},
        )

