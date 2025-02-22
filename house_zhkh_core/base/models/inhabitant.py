from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models.flat import Flat

class Inhabitant(models.Model):
    
    """
    Represents a resident of an apartment.

    Attributes:
        flat (Flat): The apartment where the inhabitant resides.
        full_name (str): The full name of the inhabitant.
        age (int): The age of the inhabitant.
    """

    flat = models.ForeignKey (
        Flat, on_delete=models.CASCADE, related_name='inhabitants'
    )
    full_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()

    def __str__ (
        self,
    ) -> str:
        
        """
        Returns a string representation of the Inhabitant instance.

        Returns:
            str: A formatted string displaying the inhabitant's name and apartment.
        """
        
        return f'{self.full_name} (Flat {self.flat.flat_number})'
