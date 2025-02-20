from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models.building import Building

class Flat(models.Model):
    
    """
    Represents an apartment within a building.

    Attributes:
        building (Building): The building to which the apartment belongs.
        flat_number (int): The apartment number.
        flat_floor (int): The floor on which the apartment is located.
        square (int): The total area of the apartment in square meters.
    """

    building = models.ForeignKey (
        Building, on_delete=models.CASCADE, related_name="flats"
    )
    flat_number = models.PositiveIntegerField()
    flat_floor = models.PositiveIntegerField()
    square = models.PositiveIntegerField()

    def __str__ (
        self,
    ) -> str:
        
        """
        Returns a string representation of the Flat instance.

        Returns:
            str: A formatted string displaying the flat number and building address.
        """
        
        return f"Flat {self.flat_number}, {self.building.address}"


class FlatHcsBalance(models.Model):
    
    """
    Represents the housing and communal services (HCS) balance for an apartment.

    Attributes:
        flat (Flat): The apartment to which this balance belongs.
        balance (int): The current balance amount (e.g., debt or credit).
    """

    flat = models.ForeignKey (
        Flat, on_delete=models.CASCADE, related_name="balances"
    )
    balance = models.IntegerField(default=0)

    def __str__ (
        self,
    ) -> str:
        
        """
        Returns a string representation of the FlatHcsBalance instance.

        Returns:
            str: A formatted string displaying the balance for the given apartment.
        """
        
        return f"Balance for {self.flat}: {self.balance}"
