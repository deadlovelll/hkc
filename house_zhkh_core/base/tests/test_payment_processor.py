from datetime import datetime  
from unittest.mock import MagicMock, patch  

from django.test import TestCase  

from base.controllers.payment_controllers.payment_calculator.payment_calculator import (
    PaymentCalculator,
)
from base.controllers.payment_controllers.payment_processor.payment_processor import (
    PaymentProcessor,
)

class PaymentProcessorTest(TestCase):
    
    """
    Test suite for the PaymentProcessor class.
    """

    def test_process_payments (
        self,
    ) -> None:
        
        """
        Test that payments are processed and created correctly.
        """
        
        processor = PaymentProcessor(10.0, 5.0)
        with patch (
            'base.models.flat.Flat.objects.all', 
            return_value=[MagicMock(), MagicMock()]
        ), \
            patch.object (
                PaymentCalculator, 
                'calculate_fees', 
                return_value = {
                    'water_fee': 100, 
                    'common_area_fee': 50, 
                    'total_fee': 150,
                }
            ), \
            patch('base.models.payment.Payment.objects.create') as mock_create:
            
            result = processor.process_payments (
                datetime(2024, 2, 1), 
                datetime(2024, 1, 1),
            )
        
        self.assertEqual (
            len(result), 
            2,
        )
        self.assertEqual (
            mock_create.call_count, 
            2,
        )