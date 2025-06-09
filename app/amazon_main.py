from fastapi import FastAPI
from app.apis.amazon_api import router
import uvicorn

app = FastAPI()
app.include_router(router, prefix="/amazon")

if __name__ == "__main__":
    uvicorn.run("app.amazon_main:app", host="0.0.0.0",port=8000,reload=True,log_level="debug")
