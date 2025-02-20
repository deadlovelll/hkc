from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models.flat import Flat

class Payment(models.Model):
    
    """
    Represents a utility payment for an apartment.

    Attributes:
        flat (Flat): The apartment for which the payment is made.
        month (date): The billing month of the payment.
        water_fee (float): The fee for water consumption.
        common_area_fee (float): The fee for common area maintenance.
        total_fee (float): The total amount due, including all fees.
    """

    flat = models.ForeignKey(Flat, on_delete=models.CASCADE)
    month = models.DateField()
    water_fee = models.FloatField()
    common_area_fee = models.FloatField()
    total_fee = models.FloatField()

    def __str__ (
        self,
    ) -> str:
        
        """
        Returns a string representation of the Payment instance.

        Returns:
            str: A formatted string displaying the apartment, month, and total fee.
        """
        
        return f"Payment for {self.flat} ({self.month}): {self.total_fee}"
