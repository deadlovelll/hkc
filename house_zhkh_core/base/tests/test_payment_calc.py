from django.test import TestCase
from unittest.mock import patch, MagicMock
from base.controllers.payment_controllers.payment_calculator.payment_calculator import PaymentCalculator
from datetime import datetime

class PaymentCalculatorTest(TestCase):
    """
    Test suite for the PaymentCalculator class.
    """

    def setUp (
        self,
    ) -> None:
        
        """
        Set up common test data for PaymentCalculator tests.
        """
        
        self.water_rate = 10.0
        self.common_area_rate = 5.0
        self.calculator = PaymentCalculator(self.water_rate, self.common_area_rate)
        self.apartment = MagicMock(square=50)
        self.current_month = datetime(2024, 2, 1)
        self.previous_month = datetime(2024, 1, 1)

    def test_calculate_fees_success (
        self,
    ) -> None:
        
        """
        Test fee calculation when water meter readings are available.
        """
        
        current_reading = MagicMock(reading=200)
        previous_reading = MagicMock(reading=150)
        
        with patch('myapp.calculations.WaterMeter.objects.filter') as mock_filter:
            mock_filter.side_effect = [[current_reading], [previous_reading]]
            result = self.calculator.calculate_fees (
                self.apartment, 
                self.current_month, 
                self.previous_month,
            )
        
        expected_result = {
            'water_fee': 500.0,
            'common_area_fee': 250.0,
            'total_fee': 750.0,
        }
        self.assertEqual (
            result, 
            expected_result,
        )

    def test_calculate_fees_missing_readings (
        self,
    ) -> None:
        
        """
        Test that the method returns None if water meter readings are missing.
        """
        
        with patch('base.models.water_meter.WaterMeter.objects.filter') as mock_filter:
            mock_filter.side_effect = [[], []]
            result = self.calculator.calculate_fees (
                self.apartment, 
                self.current_month, 
                self.previous_month,
            )
        
        self.assertIsNone(result)

    def test_calculate_fees_no_water_consumption (
        self,
    ) -> None:
        
        """
        Test that water fee is zero if no water was consumed.
        """
        
        current_reading = MagicMock(reading=150)
        previous_reading = MagicMock(reading=150)
        
        with patch('base.models.water_meter.WaterMeter.objects.filter') as mock_filter:
            mock_filter.side_effect = [[current_reading], [previous_reading]]
            result = self.calculator.calculate_fees (
                self.apartment, 
                self.current_month, 
                self.previous_month,
            )
        
        expected_result = {
            'water_fee': 0.0,
            'common_area_fee': 250.0,
            'total_fee': 250.0,
        }
        self.assertEqual (
            result, 
            expected_result,
        )
