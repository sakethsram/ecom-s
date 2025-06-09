from fastapi import FastAPI
from app.apis.sapna_api import router
import uvicorn

app = FastAPI()
app.include_router(router, prefix="/sapna")

if __name__ == "__main__":
    uvicorn.run("app.sapna_main:app", host="0.0.0.0",port=8002,reload=True,log_level="debug")
