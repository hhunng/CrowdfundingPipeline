from fastapi import FastAPI
from api import newsfeed_api

app = FastAPI()
app.include_router(newsfeed_api.router)