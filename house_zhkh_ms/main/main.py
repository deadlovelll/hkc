import uvicorn

from house_zhkh_ms.app.app import create_app
from house_zhkh_ms.config.config import Config

app = create_app()

if __name__ == "__main__":
    uvicorn.run (
        app, 
        host=Config.HOST, 
        port=Config.PORT
    )