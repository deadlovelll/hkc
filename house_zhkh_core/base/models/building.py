from django.db import models
from django.utils.translation import gettext_lazy as _

class Building(models.Model):
    
    """
    Represents a building with a specific address.

    Attributes:
        address (str): The address of the building, stored as a character field (max length: 200).
    """

    address = models.CharField(max_length=200)

    def __str__ (
        self,
    ) -> str:
        
        """
        Returns a string representation of the Building instance.

        Returns:
            str: The address of the building.
        """
        
        return self.address
