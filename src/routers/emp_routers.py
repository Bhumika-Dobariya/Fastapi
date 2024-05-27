from fastapi import FastAPI,HTTPException,APIRouter,Depends,Header
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.emp_schemas import AllEmployee,emppass,update
from src.models.emp_models import Employee
import uuid
from src.utilis.token import get_token,decode_token_user_id,decode_token_uname,decode_token_password,logging_token



pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

employee = APIRouter()

db = Sessionlocal()



#_______________create_emp_________________________


@employee.post("/create_emp",response_model=AllEmployee)
def create_employee(emp :AllEmployee):
    new_emp = Employee(
    id = str(uuid.uuid4()),
    emp_name  = emp.emp_name,
    email = emp.email,
    phone_no =emp.phone_no,
    position = emp.position,
    u_name = emp.u_name,
    password  = pwd_context.hash(emp.password)
    )
    db.add(new_emp)
    db.commit()
    return new_emp


#___________encode_id_________________

@employee.get("/encode_token_id")
def encode_token_id(id:str):
    access_token = get_token(id)
    return access_token


#__________get by token_______________

@employee.get("/get_info_by_token",response_model=AllEmployee)
def get_id_info_by_token(token:str):
    emp_id = decode_token_user_id(token)
    db_emp = db.query(Employee).filter(Employee.id == emp_id,Employee.is_active==True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail= "emp not found")
    return db_emp 


#__ depends

@employee.get("/get_info_by_token_depends",response_model=AllEmployee)
def get_id_info_by_token(emp_id = Depends(decode_token_user_id)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id,Employee.is_active==True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail= "emp not found")
    return db_emp 


#__ header

@employee.get("/get_info_by_token_header",response_model=AllEmployee)
def get_id_info_by_token(token=Header(...)):
    emp_id = decode_token_user_id(token)
    db_emp = db.query(Employee).filter(Employee.id == emp_id,Employee.is_active==True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail= "emp not found")
    return db_emp



#___________________get all_____________________

@employee.get("/get_all",response_model=list[AllEmployee])
def get_all_emp():
    db_emp = db.query(Employee).all()
    if db_emp is None:
        raise HTTPException(status_code=404,detail = "emp not found")
    return db_emp



#______________update emp by token________________


@employee.put("/update_emp_by_token",response_model=AllEmployee)
def update_emp(token:str, emp : AllEmployee):
    emp_id = decode_token_user_id(token)
    db_emp = db.query(Employee).filter(Employee.id == emp_id,Employee.is_active == True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    db_emp.emp_name  = emp.emp_name,
    db_emp.email = emp.email,
    db_emp.phone_no =emp.phone_no,
    db_emp.position = emp.position,
    db_emp.u_name = emp.u_name,
    db_emp.password  = pwd_context.hash(emp.password)
    
    db.commit()
    return db_emp


#__depends

@employee.put("/update_through_depends",response_model=update)
def update_emp_patch(emp:update,emp_id = Depends(decode_token_user_id)):
        db_emp = db.query(Employee).filter(Employee.id == emp_id,Employee.is_active == True).first()
        if db_emp is None:
           raise HTTPException(status_code=404,detail="emp not found")
       
        db_emp.phone_no =emp.phone_no,
        db_emp.position = emp.position,
        
        db.commit()
        return db_emp
 
    
#__ header

@employee.put("/update_through_header",response_model=update)
def update_emp_patch(emp:update,token = Header(...)):
        emp_id = decode_token_user_id(token)
        db_emp = db.query(Employee).filter(Employee.id == emp_id,Employee.is_active == True).first()
        if db_emp is None:
           raise HTTPException(status_code=404,detail="emp not found")
       
        db_emp.phone_no =emp.phone_no,
        db_emp.position = emp.position,
        
        db.commit()
        return db_emp 


#patch request

@employee.patch("/update_through_patch",response_model=update)
def update_emp_patch(token:str,emp:update):
        emp_id = decode_token_user_id(token)
        db_emp = db.query(Employee).filter(Employee.id == emp_id,Employee.is_active == True).first()
        if db_emp is None:
           raise HTTPException(status_code=404,detail="emp not found")
       
        if emp.phone_no:
            db_emp.phone_no = emp.phone_no
        if emp.position:
            db_emp.position = emp.position 
            
        db.commit()
        return db_emp
 
 #put
 
@employee.put("/update_through_put",response_model=update)
def update_emp_patch(token:str,emp:update):
        emp_id = decode_token_user_id(token)
        db_emp = db.query(Employee).filter(Employee.id == emp_id,Employee.is_active == True).first()
        if db_emp is None:
           raise HTTPException(status_code=404,detail="emp not found")
       
        db_emp.phone_no =emp.phone_no,
        db_emp.position = emp.position,
        
        db.commit()
        return db_emp          



#______________delete_by_token___________________________



@employee.delete("/delete_emp_by_token")
def delete_emp(token:str):
    emp_id = decode_token_user_id(token)
    db_emp = db.query(Employee).filter(Employee.id ==emp_id , Employee.is_active ==True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    db_emp.is_delete = True
    db_emp.is_active = False
   
    
    db.commit()
    return {"emp delete successfully"}


#__  depends

@employee.delete("/delete_emp_by_depends")
def delete_emp(emp_id = Depends(decode_token_user_id)):
    db_emp = db.query(Employee).filter(Employee.id ==emp_id , Employee.is_active ==True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    db_emp.is_delete = True
    db_emp.is_active = False
   
    
    db.commit()
    return {"emp delete successfully"}


#__  header

@employee.delete("/delete_emp_by_header")
def delete_emp(token = Header(...)):
    emp_id = decode_token_user_id(token)
    db_emp = db.query(Employee).filter(Employee.id ==emp_id , Employee.is_active ==True).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    db_emp.is_delete = True
    db_emp.is_active = False
   
    
    db.commit()
    return {"emp delete successfully"}



#_____________________reregister______________________


@employee.put("/reregister")
def toggel_emp(token:str,empn:emppass):
    emp_id = decode_token_user_id(token)
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    if db_emp.is_delete is True and db_emp.is_active is False:
        if pwd_context.verify(empn.password,db_emp.password):
           
            db_emp.is_delete = False
            db_emp.is_active = True
            
            db.commit()
            return True
    raise HTTPException(status_code=404,detail= "invalid crediantial")


#depends

@employee.put("/reregister_depends")
def toggel_emp(empn:emppass,emp_id=Depends(decode_token_user_id)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    if db_emp.is_delete is True and db_emp.is_active is False:
        if pwd_context.verify(empn.password,db_emp.password):
           
            db_emp.is_delete = False
            db_emp.is_active = True
            
            db.commit()
            return True
    raise HTTPException(status_code=404,detail= "invalid crediantial")


#header

@employee.put("/reregister_header")
def toggel_emp(empn:emppass,token = Header(...)):
    emp_id = decode_token_user_id(token)
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    if db_emp.is_delete is True and db_emp.is_active is False:
        if pwd_context.verify(empn.password,db_emp.password):
           
            db_emp.is_delete = False
            db_emp.is_active = True
            
            db.commit()
            return True
    raise HTTPException(status_code=404,detail= "invalid crediantial")



#______________forget password________________________



@employee.put("/forget_Password_by_token")

def forget_password_token(token: str ,user_newpass : str):
    emp_id = decode_token_user_id(token)
    db_emp = db.query(Employee).filter(Employee.id == emp_id ).first()
    if db_emp is  None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    db_emp.password = pwd_context.hash(user_newpass)
    
    db.commit()
    return "Forget Password successfully"


#depends

@employee.put("/forget_Password_by_depends")

def forget_password_token(user_newpass : str,emp_id = Depends(decode_token_user_id)):
    
    db_emp = db.query(Employee).filter(Employee.id == emp_id ).first()
    if db_emp is  None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    db_emp.password = pwd_context.hash(user_newpass)
    
    db.commit()
    return "Forget Password successfully"



#header

@employee.put("/forget_Password_by_header")

def forget_password_token(user_newpass : str, token =Header(...)):
    emp_id = decode_token_user_id(token)
    db_emp = db.query(Employee).filter(Employee.id == emp_id ).first()
    if db_emp is  None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    db_emp.password = pwd_context.hash(user_newpass)
    
    db.commit()
    return "Forget Password successfully"



#_______________reset password___________________


@employee.put("/reset_password_by_token")
def reset_password_token(token:str,oldpass:str,newpass:str):
    emp_id = decode_token_user_id(token)
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    if pwd_context.verify(oldpass,db_emp.password):
        db_emp.password = pwd_context.hash(newpass)
        db.commit()
        return {"password reset successfully"}
    else:
        return {"password not matched"}
  
#depends

@employee.put("/reset_password_by_token_depends")
def reset_password_token(oldpass:str,newpass:str,emp_id = Depends(decode_token_user_id)):
    
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    if pwd_context.verify(oldpass,db_emp.password):
        db_emp.password = pwd_context.hash(newpass)
        db.commit()
        return {"password reset successfully"}
    else:
        return {"password not matched"}
    
#header
  
@employee.put("/reset_password_by_header")
def reset_password_token(oldpass:str,newpass:str, token = Header(...)):
    
    emp_id = decode_token_user_id(token)
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    
    if pwd_context.verify(oldpass,db_emp.password):
        db_emp.password = pwd_context.hash(newpass)
        db.commit()
        return {"password reset successfully"}
    else:
        return {"password not matched"}  
    
    
    
    
#________________encode logging____________


@employee.get("/encode_logging")
def token_logging(uname:str,password:str):
    access_token = logging_token(uname,password)
    return access_token


        
 #_______________logging_________________   
     

@employee.get("/logging_by_token")
def logging(token:str):
    uname = decode_token_uname(token)
    password = decode_token_password(token)
    db_emp = db.query(Employee).filter(Employee.u_name==uname,Employee.is_active ==True).first()
    
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    if not pwd_context.verify(password,db_emp.password):
        raise HTTPException(status_code=404,detail= "incorrect password")
    
    return "loging successfully"


#__depends

@employee.get("/logging_by_depends")

def logging(uname = Depends(decode_token_uname), password = Depends(decode_token_password)):
  
    db_emp = db.query(Employee).filter(Employee.u_name==uname,Employee.is_active ==True).first()
    
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    if not pwd_context.verify(password,db_emp.password):
        raise HTTPException(status_code=404,detail= "incorrect password")
    
    return "loging successfully"


#___header

@employee.get("/logging_by_header")
def logging(token = Header(...)):
    uname = decode_token_uname(token)
    password = decode_token_password(token)
    db_emp = db.query(Employee).filter(Employee.u_name==uname,Employee.is_active ==True).first()
    
    if db_emp is None:
        raise HTTPException(status_code=404,detail="emp not found")
    if not pwd_context.verify(password,db_emp.password):
        raise HTTPException(status_code=404,detail= "incorrect password")
    
    return "loging successfully"