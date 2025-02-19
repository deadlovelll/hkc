import os

class Config:
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8140))
    TITLE: str = os.getenv("TITLE", "House API")
    DESCRIPTION: str = os.getenv("DESCRIPTION", "API for managing houses")
    VERSION: str = os.getenv("VERSION", "1.0.0")