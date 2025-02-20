from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models.flat import Flat

class Counter(models.Model):
    
    """
    Represents a utility meter for an apartment (gas, electricity, water, or heat).

    Attributes:
        flat (Flat): The apartment to which the meter belongs.
        counter_type (int): The type of meter (Gas, Electricity, Water, or Heat).
        last_reading (float): The previous recorded reading of the meter.
        current_reading (float): The latest recorded reading of the meter.
    """

    class CounterType(models.IntegerChoices):
        
        """
        Enum representing different types of utility meters.

        Values:
            GAS (0): Gas meter.
            ELECTRICITY (1): Electricity meter.
            WATER (2): Water meter.
            HEAT (3): Heat meter.
        """
        
        GAS = 0, _("Gas Counter")
        ELECTRICITY = 1, _("Electricity Counter")
        WATER = 2, _("Water Counter")
        HEAT = 3, _("Heat Counter")

    flat = models.ForeignKey (
        Flat, on_delete=models.CASCADE, related_name="counters"
    )
    counter_type = models.IntegerField(choices=CounterType.choices)
    last_reading = models.FloatField()
    current_reading = models.FloatField()

    def __str__ (
        self,
    ) -> str:
        
        """
        Returns a string representation of the Counter instance.

        Returns:
            str: A formatted string displaying the counter type and associated apartment.
        """
        
        return f"{self.get_counter_type_display()} for {self.flat}"


class CounterHistory(models.Model):
    
    """
    Stores the history of meter readings for different utility counters.

    Attributes:
        counter (Counter): A foreign key reference to the associated Counter instance.
        date (date): The date when the meter reading was recorded (automatically set on creation).
        reading (float): The recorded meter reading value.
    """

    counter = models.ForeignKey (
        Counter, on_delete=models.CASCADE, related_name="history"
    )
    date = models.DateField(auto_now_add=True)
    reading = models.FloatField()

    def __str__ (
        self,
    ) -> str:
        
        """
        Returns a string representation of the CounterHistory instance.

        Returns:
            str: A formatted string indicating the counter and the recorded date.
        """
        
        return f"History for {self.counter} on {self.date}"
