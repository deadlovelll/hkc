from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseController(ABC):
    
    """
    Abstract base class for controllers, defining a standard CRUD interface.
    """

    @abstractmethod
    async def get (
        self, 
        identifier: Any,
    ) -> Any:
        
        """
        Retrieve a resource based on an identifier.
        """
        
        pass

    @abstractmethod
    async def create (
        self, 
        data: Dict,
    ) -> Any:
        
        """
        Create a new resource using the provided data.
        """
        
        pass

    async def update (
        self, 
        identifier: Any, 
        data: Dict,
    ) -> Any:
        
        """
        Update an existing resource. Override if update functionality is needed.
        """
        
        raise NotImplementedError('Update operation is not implemented.')

    async def delete (
        self, 
        identifier: Any,
    ) -> Any:
        
        """
        Delete a resource. Override if delete functionality is needed.
        """
        
        raise NotImplementedError('Delete operation is not implemented.')
