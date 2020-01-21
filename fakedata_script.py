from faker import Faker
# import motor.motor_asyncio
import json
from random2 import randint
fake = Faker()

# create connection for the Mongo database
# client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
#
# db = client['employee']
# collection = db['employee_data']


#dictionary for the employee database
finaldata=[]

for i in range(0, 10100):
    employee_data = {}
    employee_data['emp_id'] = randint(1,110000)
    employee_data['name'] = fake.name()
    employee_data['email'] = fake.email()
    employee_data['age'] = randint(18,60)
    employee_data['country'] = fake.country()
    finaldata.append(employee_data)

with open('employeedb.json', 'w') as dbf :
    json.dump(finaldata, dbf)


