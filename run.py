import uvicorn
from app_views.main import app

if __name__ == "__main__":
    uvicorn.run("fastapi_code:app", reload = True)