from fastapi import FastAPI
from src.routers.emp_routers import employee 

app = FastAPI(title="EmployeeDetails")
app.include_router(employee)