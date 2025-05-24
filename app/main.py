import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.apis.amazon_api import router as amazon_router
from app.apis.flipkart_api import router as flipkart_router
from app.apis.sapna_api import router as sapna_router

app = FastAPI(
    title="Multi-Store Management System",
    description="API for managing Amazon, Flipkart, and Sapna products",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(amazon_router, prefix="/api/amazon", tags=["Amazon"])
app.include_router(flipkart_router, prefix="/api/flipkart", tags=["Flipkart"])
app.include_router(sapna_router, prefix="/api/sapna", tags=["Sapna"])

@app.get("/")
async def root():
    return {
        "message": "Multi-Store Management System API",
        "available_stores": ["Amazon", "Flipkart", "Sapna"],
        "endpoints": {
            "amazon": "/api/amazon/",
            "flipkart": "/api/flipkart/",
            "sapna": "/api/sapna/"
        }
    }

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )

