from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models.flat import Flat

class WaterMeter(models.Model):
    
    """
    Represents a water meter for a specific apartment.

    Attributes:
        flat (Flat): The apartment to which this water meter belongs.
        reading (float): The recorded water consumption in cubic meters.
        month (date): The month for which the reading is recorded.
    """

    flat = models.ForeignKey (
        Flat, 
        on_delete=models.CASCADE,
    )
    reading = models.FloatField()
    month = models.DateField()

    def __str__ (
        self,
    ) -> str:
        
        """
        Returns a string representation of the WaterMeter instance.

        Returns:
            str: A formatted string with the reading, apartment, and month.
        """
        
        return f'WaterMeter {self.reading} for {self.flat} ({self.month})'
