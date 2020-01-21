from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio

from typing import List

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

db = client['empdb']
collection = db['empdata']

class Item(BaseModel):
    emp_id : int
    name : str
    email : str
    age : int
    country : str

class Res(BaseModel):
    name: str
    email: str
    age: int
    country: str

class Updatedata(BaseModel):
    name: str
    email: str
    age: int
    country: str


@app.post("/create", response_model=List[Res])
async def do_insertt(item:List[Item]):
    update_item_encoded = jsonable_encoder(item)
    print(update_item_encoded)
    result = await db.testdata.insert_many(update_item_encoded)
    return item

@app.get("/retrieve/")
async def do_find(pagenum:int=1,pagesize:int=10):
    arr=[]
    async for document in db.empdata.find().skip(pagesize*(pagenum-1)).limit(pagesize):
        dict={}
        dict["emp_id"] = document["emp_id"]
        dict["name"] = document["name"]
        dict["email"] = document["email"]
        dict["age"] = document["age"]
        dict["country"] = document["country"]
        arr.append(dict)
    if not arr:
        return f"no more data"
    else:
        return {f"page number : {pagenum} {arr}"}


@app.get("/retrieve-one/{n}")
async def do_find(n: int):
    dict={}
    result = await db.empdata.find_one({"emp_id": n})
    dict["emp_id"] = result["emp_id"]
    dict["name"] = result["name"]
    dict["email"] = result["email"]
    dict["age"] = result["age"]
    dict["country"] = result["country"]
    return dict


@app.put("/update/{q}")
async def do_updat(q: int, item: Updatedata):
    update_item_encoded = jsonable_encoder(item)
    print(update_item_encoded)
    cursorr = db.empdata
    result = await cursorr.update_one({"emp_id":q} , {"$set": update_item_encoded})
    print("hello")
    return update_item_encoded

@app.delete("/delete-all")
async def do_delete():
    cursorr=db.empdata
    c= await cursorr.count_documents({})
    print(f"number of documents is {c}")
    res= await db.empdata.delete_many({"emp_id":{'$lte' : 100000}})
    d = await cursorr.count_documents({})
    return (f"{c-d} number of items deleted")

@app.delete("/delete-one/{q}")
async def do_delete(q:int):
    print(q)
    cursorr=db.empdata
    c= await cursorr.count_documents({})
    print(f"number of documents is {c}")
    res= await db.empdata.delete_one({'emp_id':q})
    d = await cursorr.count_documents({})
    return (f"{c-d} number of items deleted")


