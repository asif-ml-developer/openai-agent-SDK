from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"salam": "Dunya"}
    # return"Hello World"


@app.get("/item")
def read_item():
    return"Item"

@app.get("/item/{item_id}")
def read_item(item_id: int): # here if we will not put type int then it will take string as input however if place int then it will take int and create error on given string input
    return item_id

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# =========================================================================================================
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}
# if above fixed path is called in below app.get("/users/{user_id}") then it will return {"user_id": "the current user"}
# because of order it place befor app.get("/users/{user_id}")

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# @app.get("/users/me")
# async def read_user_me():
#     return {"user_id": "the current user"}
# Otherwise, the path for /users/{user_id} would match also for /users/me, "thinking" that it's receiving a parameter user_id with a value of "me".

# =========================================================================================================
@app.get("/userss")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/userss")
async def read_users2():
    return ["Bean", "Elfo"]
# The first one will always be used since the path matches first.

# =========================================================================================================

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
# =========================================================================================================

@app.get("/{product}/inventory/{item}")
async def read_item(item: int, product: str):
    return {"item": item, "product_name": product}

# =========================================================================================================

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return file_path

