from pydantic import BaseModel


class AllEmployee(BaseModel):
    emp_name :str
    email : str
    phone_no :str
    position :str
    u_name :str
    password :str
    
    
  
    
class emppass(BaseModel):
    password :str
    
class update(BaseModel):
    phone_no :str
    position :str