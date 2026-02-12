from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.db.base_class import Base
from app.db.session import engine
from app.db.session import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Kết nóo các routes
app.include_router(api_router, prefix="/app/v1")

@app.get("/")
def root():
    return {"message": "Welcome to Blog API. Go to /docs for Swagger UI."}