from pydantic import computed_field
from typing import Annotated
from fastapi import Query
from fastapi.responses import JSONResponse
from fastapi import FastAPI,Path,HTTPException    
import json
from pydantic import BaseModel,Field
from typing import Optional,Annotated

app=FastAPI()

class Customer(BaseModel):
    customer_id: Annotated[str,Field(...,description='Id of the customer',examples=['CUST001'])]
    name: Annotated[str,Field(...,description='Name of the customer',examples=['Aarav Sharma'])]
    email: Annotated[str,Field(...,description='Email of the customer',examples=['[EMAIL_ADDRESS]'])]
    age: Annotated[int,Field(...,description='Age of the customer',examples=[28])]
    city: Annotated[str,Field(...,description='City of the customer',examples=['Bengaluru'])]
    country: Annotated[str,Field(...,description='Country of the customer',examples=['India'])]
    signup_date: str
    total_orders: int
    total_spent: float
    last_order_date: str
    preferred_category: str

    @computed_field
    @property
    def VIP_customer(self) -> str:
        return 'Yes' if self.total_orders >10 and self.total_spent >50000 else 'No'

    @computed_field
    @property
    def cost_per_order(self) -> float:
        return self.total_spent / self.total_orders

class CustomerUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None)]
    email: Annotated[Optional[str], Field(None)]
    age: Annotated[Optional[int], Field(None)]
    city: Annotated[Optional[str], Field(None)]
    country: Annotated[Optional[str], Field(None)]
    signup_date: Annotated[Optional[str], Field(None)]
    total_orders: Annotated[Optional[int], Field(None)]
    total_spent: Annotated[Optional[float], Field(None)]
    last_order_date: Annotated[Optional[str], Field(None)]
    preferred_category: Annotated[Optional[str], Field(None)]


def load_data():
    with open('customers.json','r') as f:
        data= json.load(f)
    
    return data

def save_data(data):
    with open('customers.json','w') as f:
        json.dump(data,f)

@app.get("/hi")
def hi():
    return {'message':'hello Kiddo!'}

@app.get("/view")
def view():
    data=load_data()

    return data

@app.get("/customer/{customer_id}")
def view_customer(customer_id :str =Path(...,description='Id of the customer',example='CUST001')):
    data=load_data()
    
    if customer_id in data:
        return data[customer_id]
    return {'error':'customer not    found'}

@app.get("/sort")
def sort_customers(sort_by:str =Query(...,description='sorting  based on age, total_orders'),order:str =Query('asc',description='sort in asc or desc')):

    valid_fields=['total_orders','age']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid case from{valid_fields}')

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f'Invalid case , select between asc and desc')
    
    data=load_data()

    order=True if order=='desc' else False

    sorted_data=sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=order)

    return sorted_data

@app.post("/create")
def create_customer(customer:Customer):

    data=load_data()

    if customer.customer_id in data:
        raise HTTPException(status_code=400,detail='customer already exist')
    
    data[customer.customer_id]=customer.model_dump(exclude=['customer_id'])

    save_data(data)

    return JSONResponse(status_code=201, content={'message':'customer created successfully'})


@app.put("/edit/{customer_id}")
def update_customer(customer_id:str,customer_update:CustomerUpdate):
    data=load_data()

    if customer_id not in data:
        return HTTPException(status_code=404,detail='customer not found')

    existing_customer_info=data[customer_id]

    updated_customer_data=customer_update.model_dump(exclude_unset=True)

    for key,value in updated_customer_data.items():
        existing_customer_info[key]=value
        
    existing_customer_info['customer_id']=customer_id

    # Pass it through the main Customer model to re-compute VIP and cost_per_order
    updated_customer = Customer(**existing_customer_info)
    data[customer_id] = updated_customer.model_dump()

    save_data(data)

    return JSONResponse(status_code=201,content={'message':'cusomter updated successfully'})


@app.delete('/delete/{customer_id}')
def delete_customer(customer_id:str):

    data=load_data()

    if customer_id not in data:
        raise HTTPException(status_code=404,detail='customer not found')

    del data[customer_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'customer deleted successfully'})