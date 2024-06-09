from fastapi import FastAPI
from api import donation_api

app = FastAPI()
app.include_router(donation_api.router)