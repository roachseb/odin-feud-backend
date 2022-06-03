from pandas import DataFrame, concat
from pytrends.request import TrendReq
from typing import List, Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
pytrends = TrendReq()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://intense-castle-46815.herokuapp.com/"
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_suggestions(word:str) -> List[str]:
    return [ v for dic in pytrends.suggestions(word) for k,v in dic.items() if k == "title"]

@app.get("/")
async def read_root():
    return {"This": "Update"}


@app.get("/regions/{word}")
async def get_trend_by_region(word: str, timeframe:str="today 1-m", suggestion: bool=False):
    if suggestion:
        word = get_suggestions(word)
    pytrends.build_payload(word,timeframe=timeframe)
    res_dict = pytrends.interest_by_region().mean(axis=1).nlargest(6).to_dict()
    return [{"text": k, "money": v/100*50} for k,v in res_dict.items()]


@app.get("/interest/{word}")
async def get_trend(word: str, timeframe:str="today 1-m", suggestion: bool=False):
    if suggestion:
        word = get_suggestions(word)
    pytrends.build_payload(word,timeframe=timeframe)
    res_dict = pytrends.interest_over_time()[pytrends.interest_over_time()['isPartial']==False].drop(["isPartial"],axis=1).mean(axis=0).to_dict()
    return [{"text": k, "money": v/100*50} for k,v in res_dict.items()]
