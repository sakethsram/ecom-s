from fastapi import FastAPI
from app.apis.flipkart_api import router
import uvicorn

app = FastAPI()
app.include_router(router, prefix="/flipkart")

if __name__ == "__main__":
    uvicorn.run("app.flipkart_main:app", host="0.0.0.0",port=8001,reload=True,log_level="debug")
