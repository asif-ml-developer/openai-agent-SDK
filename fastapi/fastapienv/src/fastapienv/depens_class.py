from typing import Annotated, Any

from fastapi import Depends, FastAPI

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(CommonQueryParams)]):
# async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]): # this will also work
# async def read_items(commons: Annotated[Any, Depends(CommonQueryParams)]): # this will also work
# async def read_items(commons: Annotated[CommonQueryParams, Depends()]): # this will also work
    # return commons  # returns {"q": q, "skip": skip, "limit": limit}
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    # below is used slice ie for example if their are 100 items capacity and skip is 5 then it start from skiping 5 items and adding more 5 items in limit will complete the total capacity of 100
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response