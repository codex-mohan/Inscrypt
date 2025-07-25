from fastapi import FastAPI
from app.v1.routes import stenography
from app.logging_config import logger
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Inscrypt API...")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock down in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stenography.router, prefix="/api/v1")


@app.get("/")
def read_root():
    logger.info("Root endpoint was hit")
    return {"message": "Welcome to the Inscrypt API"}
