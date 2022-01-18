import uvicorn
from app_views.main import app

if __name__ == "__main__":
    uvicorn.run("run:app", reload = True, host = "0.0.0.0", port = 3000)
