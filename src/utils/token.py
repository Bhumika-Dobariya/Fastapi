from datetime import datetime,timedelta
from fastapi import HTTPException,status,Security
from dotenv import load_dotenv
import os
from jose import JWTError,jwt

load_dotenv()

SECRET_KEY = str(os.environ.get("SECRET_KEY"))
ALGORITHM = str(os.environ.get("ALGORITHM"))

def get_token(id):
    payload = {
        "emp_id" : id,
        "exp" : datetime.utcnow() +timedelta(minutes=30)
    }
    
    access_token = jwt.encode(payload,SECRET_KEY,ALGORITHM)
    print(type(access_token))
    return access_token


def logging_token(uname,password):
    payload = {
        "emp_uname" :uname,
        "emp_password" : password ,
        "exp" : datetime.utcnow() + timedelta(minutes=35)
    }
    access_token  = jwt.encode(payload,SECRET_KEY,ALGORITHM)
    print(type(access_token))
    return access_token



def decode_token_user_id(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("emp_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
        )
        
def decode_token_uname(token):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        emp_uname = payload.get("emp_uname")
        if not emp_uname:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail="uname not exists in payload")
        return emp_uname
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= "invalid token")
    
    
   
def decode_token_password(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        emp_password = payload.get("emp_password")
        if not emp_password:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= "password not exists in payload")
        return emp_password
    except JWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "invalid token")
        


