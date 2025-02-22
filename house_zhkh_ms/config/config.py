import os

class Config:
    
    """
    Configuration class for setting up API settings from environment variables.

    This class defines the configuration settings used by the application, including the host,
    port, API title, description, and version. If environment variables are not set, default
    values are provided.

    Attributes:
        HOST (str): The host address for the API server. Defaults to "127.0.0.1".
        PORT (int): The port number for the API server. Defaults to 8140.
        TITLE (str): The title of the API. Defaults to "House API".
        DESCRIPTION (str): A short description of the API. Defaults to "API for managing houses".
        VERSION (str): The version of the API. Defaults to "1.0.0".
    """
    
    HOST: str = os.getenv('FASTAPI_HOST', '127.0.0.1')
    PORT: int = int(os.getenv('FASTAPI_PORT', 8140))
    TITLE: str = os.getenv('TITLE', 'House API')
    DESCRIPTION: str = os.getenv('DESCRIPTION', 'API for managing houses')
    VERSION: str = os.getenv('VERSION', '1.0.0')