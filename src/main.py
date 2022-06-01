from pytrends.request import TrendReq
from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Test": "Output"}