from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import userauth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(userauth.router)


@app.get("/health")
async def root():
    return {"message": "OK, API is up and running"}
