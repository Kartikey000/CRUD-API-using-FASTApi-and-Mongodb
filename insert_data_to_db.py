import json
import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

db = client['empdb']
collection = db['empdata']

with open('employeedb.json', 'r') as f:
    file_data = json.load(f)

collection.insert_many(file_data)

client.close()
