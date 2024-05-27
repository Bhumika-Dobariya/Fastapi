from fastapi import FastAPI,HTTPException,APIRouter,Depends,Header
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.emp_schemas import AllEmployee,emppass,update
from src.models.emp_models import Employee
import uuid
from src.utils.token import get_token,decode_token_user_id,decode_token_uname,decode_token_password,logging_token
from typing import Optional
from logs.log_config import logger


pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

employee = APIRouter()

db = Sessionlocal()



#_______________create_emp_________________________


@employee.post("/create_emp",response_model=AllEmployee)
def create_employee(emp :AllEmployee):
    
    logger.info("employee is creating ")
    
    new_emp = Employee(
    id = str(uuid.uuid4()),
    emp_name  = emp.emp_name,
    email = emp.email,
    phone_no =emp.phone_no,
    position = emp.position,
    u_name = emp.u_name,
    password  = pwd_context.hash(emp.password)
    )
    
    logger.success("employee is created")
    
    logger.info("employee is adding to database...")
    db.add(new_emp)
    logger.info("employee loaded successfuly")
    
    db.commit()
    logger.success("employee has been saved successfully")

    return new_emp


#___________encode_id_________________

@employee.get("/encode_token_id")
def encode_token_id(id:str):
    logger.info(f"access token generateing for id:{id}")
    access_token = get_token(id)
    logger.success(f"access token generated for id:{id}")
    
    logger.success("access token return successfuly")
    return access_token


#__________get by token_______________



@employee.get("/get_info_by_token",response_model=AllEmployee)
def get_id_info_by_token(token:str):
    logger.info("Accessing employee information using token")
    emp_id = decode_token_user_id(token)
    logger.info ("Finding employee information in the database")
    db_emp = db.query(Employee).filter(Employee.id == emp_id,Employee.is_active==True).first()
    
    logger.success("retrived employeed information successfuly")
    
    if db_emp is None:
        logger.error ("employee not found in database")
        raise HTTPException(status_code=404,detail= "employee not found")
    
    logger.info("Returning employee information")
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
        raise HTTPException(status_code=404,detail= "employee not found")
    return db_emp



#___________________get all_____________________

@employee.get("/get_all",response_model=list[AllEmployee])
def get_all_emp():
    logger.info("finding all employee from database")
    db_emp = db.query(Employee).all()
    if db_emp is None:
        logger.error("employee not found in database")
        raise HTTPException(status_code=404,detail = "employee not found")
    logger.info("Returning employee information")
    return db_emp



#______________update emp by token________________


@employee.put("/update_emp_by_token",response_model=AllEmployee)
def update_emp(token:str, emp : AllEmployee):
    logger.info("accessing employee information using token")
    emp_id = decode_token_user_id(token)
    
    logger.info("finding employee id from database")
    db_emp = db.query(Employee).filter(Employee.id == emp_id,Employee.is_active == True).first()
    logger.info("retriving employee information from database")
    
    if db_emp is None:
        logger.error("employee not found in database")
        raise HTTPException(status_code=404,detail="emp not found")
    
    logger.info("starting modification of employee details")
    db_emp.emp_name  = emp.emp_name,
    db_emp.email = emp.email,
    db_emp.phone_no =emp.phone_no,
    db_emp.position = emp.position,
    db_emp.u_name = emp.u_name,
    db_emp.password  = pwd_context.hash(emp.password)
    logger.info("All employee details are modified")
    
    db.commit()
    
    logger.info("Returning updated employee information")

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

#.......


 



#______________delete_by_token___________________________



@employee.delete("/delete_emp_by_token")
def delete_emp(token:str):
    logger.info("accessing employee information using token")
    emp_id = decode_token_user_id(token)
    
    logger.info("finding employee id from database")
    db_emp = db.query(Employee).filter(Employee.id ==emp_id , Employee.is_active ==True).first()
    logger.info("retriving employee information from database")
    
    if db_emp is None:
        logger.error("employee not found in database")
        raise HTTPException(status_code=404,detail="emp not found")
    
    logger.info("deleting employee")
    
    db_emp.is_delete = True
    db_emp.is_active = False
   
    db.commit()
    logger.info("employee deleted successfully")
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
    logger.info("accessing employee information using token")
    emp_id = decode_token_user_id(token)
    
    logger.info("finding employee details from database")
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    logger.info("retriving employee information from database")
    
    if db_emp is None:
        logger.error("employee not found")
        raise HTTPException(status_code=404,detail="emp not found")
    
    logger.info("re-register employee")
    if db_emp.is_delete is True and db_emp.is_active is False:
        if pwd_context.verify(empn.password,db_emp.password):
           
            db_emp.is_delete = False
            db_emp.is_active = True
            
            db.commit()
            logger.info("set is_delete to False and is_active to True")
            logger.info("re-register complated")
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
    logger.warning("Invalid credentials")
    raise HTTPException(status_code=404,detail= "invalid crediantial")



#______________forget password________________________



@employee.put("/forget_Password_by_token")

def forget_password_token(token: str ,user_newpass : str):
    logger.info("accessing employee details from database")
    emp_id = decode_token_user_id(token)
    
    logger.info("finding employee id from database")
    db_emp = db.query(Employee).filter(Employee.id == emp_id ).first()
    logger.info("retriving employee details from database")
    
    if db_emp is  None:
        logger.error("employee not found")
        raise HTTPException(status_code=404,detail="emp not found")
    
    logger.info("verifying password")
    db_emp.password = pwd_context.hash(user_newpass)
    logger.success("password verified successfully ")
    
    db.commit()
    logger.success("Password updated successfully")
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
    
    logger.info("accessing employee details from database")
    emp_id = decode_token_user_id(token)
    logger.info("finding employee information from database")
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    logger.info("retrivinf employee deatails from database")
    
    if db_emp is None:
        logger.error("employee not found")
        raise HTTPException(status_code=404,detail="emp not found")
    
    logger .info("verifying password")
    if pwd_context.verify(oldpass,db_emp.password):
        db_emp.password = pwd_context.hash(newpass)
        logger.success("password verified successfully ")

        db.commit()
        logger.success("password reset successfully")
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
    logger.info("accessing username and password from database")
    access_token = logging_token(uname,password)
    logger.info("token generated successfully")
    return access_token


        
 #_______________logging_________________   
     

@employee.get("/logging_by_token")
def logging(token:str):
    logger.info("accessing token from database")
    uname = decode_token_uname(token)
    password = decode_token_password(token)
    
    logger.info("finding employee name from database")
    db_emp = db.query(Employee).filter(Employee.u_name==uname,Employee.is_active ==True).first()
    logger.info("retriving employee info from database")
    
    if db_emp is None:
        
        logger.error("employee not found")
        raise HTTPException(status_code=404,detail="emp not found")
    
    if not pwd_context.verify(password,db_emp.password):
        
        logger.error("password verification is failed..enter correct password")
        raise HTTPException(status_code=404,detail= "incorrect password")
    
    logger.info("logging successfully")
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