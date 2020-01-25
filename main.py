from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
import os
from typing import List
mongoconnection = os.environ.get("MONGO_CONNECTION","127.0.0.1")
#initializing the app
app = FastAPI()

#connection with DataBase
client = motor.motor_asyncio.AsyncIOMotorClient(mongoconnection, 27017)

db = client['empdb']
collection = db['empdata']

#request serializers
class Item(BaseModel):
    emp_id : int
    name : str
    email : str
    age : int
    country : str

#response serializer
class Res(BaseModel):
    name: str
    email: str
    age: int
    country: str

#update serializer
class Updatedata(BaseModel):
    name: str
    email: str
    age: int
    country: str

#Pagination class
class Custom_Pagination:
    default_offset= 0
    default_pagesize= 10

    def __init__(self, page, offset):
        self.page_no = page
        self.offset = offset

    async def count_doc(self):
        return await db.empdata.count_documents({})

    async def next(self):
        doc_count = await self.count_doc()
        if self.offset + self.default_pagesize < doc_count :
            return True
        else:
            return False

    def previous(self):
        if self.offset <= 0 :
            return False
        else:
            return True

    async def pagination_Response(self):
        dict={
            "page_number": self.page_no,
            "total_items": await self.count_doc(),
            "link": {
                "next": await self.next(),
                "previous": self.previous(),
            },
        }
        return dict

@app.post("/create", response_model=List[Res])
async def do_insertt(item:List[Item]):
    update_item_encoded = jsonable_encoder(item)
    print(update_item_encoded)
    result = await db.empdata.insert_many(update_item_encoded)
    return item

@app.get("/retrieve/")
async def do_find(pagenum:int=1,pagesize:int=10):
    page = pagenum
    offset = pagesize*(pagenum-1)
    connect_query = db.empdata.find().skip(offset).limit(pagesize)
    arr=[]
    print(connect_query)
    async for document in connect_query:
        dict={}
        dict["emp_id"] = document["emp_id"]
        dict["name"] = document["name"]
        dict["email"] = document["email"]
        dict["age"] = document["age"]
        dict["country"] = document["country"]
        arr.append(dict)
        print(dict)
    ob = Custom_Pagination(page,offset)
    page_resp = await ob.pagination_Response()
    print (arr)
    respon = {}
    respon["page"] = page_resp
    respon["data"] = arr
    return respon

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


