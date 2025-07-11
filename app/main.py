from fastapi import FastAPI

from app.routers import location_retrieval

from app.config import get_settings


settings = get_settings()

app = FastAPI()

app.include_router(location_retrieval.router,prefix="/location-retrieval/v0.4",tags=["Location retrieval"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)