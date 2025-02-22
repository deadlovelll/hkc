import uvicorn

from app.app import create_app
from config.config import Config

app = create_app()

if __name__ == '__main__':
    uvicorn.run (
        app, 
        host=Config.HOST, 
        port=Config.PORT
    )