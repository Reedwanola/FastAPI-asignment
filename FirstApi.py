from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from uuid import UUID, uuid4
from typing import List
from fastapi import Request
import time

# Defining the user model
class User(BaseModel):
    id: UUID | None = None  # id is optional on input
    first_name: str
    last_name: str
    age: int
    email: str
    height: float

# In-memory user storage
users: List[User] = []

# FastAPI app initialization
app = FastAPI()
origins = ["http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware for logging requests
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Completed {request.method} {request.url} in {process_time:.2f} seconds")
    return response

# Endpoint to create a user
@app.post("/users/", status_code=201, response_model=User)
async def create_user(user: User):
    # Generate a new UUID for the user
    new_user = User(id=uuid4(), **user.model_dump())  # Use `dict()` for Pydantic v1.x
    users.append(new_user)
    logger.info(f"User created: {new_user}")
    return new_user  # Return the newly created user with an ID

# Endpoint to read all users
@app.get("/users/", response_model=List[User])
async def read_users():
    logger.info("Users retrieved")
    return users