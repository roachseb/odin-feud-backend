from pandas import DataFrame
from pytrends.request import TrendReq
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"This": "Update"}

@app.get("/regions/{_region}")
async def get_trend_by_region(region: int):
    df:DataFrame= TrendReq.interest_by_region(resolution="Python")
    return df.to_json()