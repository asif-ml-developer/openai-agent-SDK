# https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/

from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


# async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
#     return {"q": q, "skip": skip, "limit": limit}

async def common_parameters(q: str | None = "RAttan Lal ....", skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons:dict = Depends(common_parameters)):  # without annotated 
    return commons

@app.get("/item/")
async def read_items(commons:dict = Depends(common_parameters)):  # without annotated 
    return commons['q']

@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]): # with Annotated
    return commons