from fastapi import FastAPI, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from png2ttf import PNGtoSVG, FontCreator, MakeTTF
from make_sample_img import make_example_from_ttf
from typing import List
import argparse
from pydantic import BaseModel
import json
from database import UserRequest, Database, Settings

class PathModel(BaseModel):
    id : str
    image : List[str]


parser = argparse.ArgumentParser()
parser.add_argument('--back_url', help=" : backend url")
parser.add_argument('--port', help=" : Set ttf port", default=8100 )

args = parser.parse_args()
backend_url = args.back_url

port = args.port

app = FastAPI()
settings = Settings()
requests_database = Database(UserRequest)



@app.get("/{id}", response_model=UserRequest)
async def get_request(id: str) -> UserRequest:
    user_request = await requests_database.get(id)

    if not user_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user_request info with ID dose not exist."
        )
    
    return user_request


@app.get("/", response_model=List[UserRequest])
async def get_all_requests() -> List[UserRequest]:
    user_requests = await requests_database.get_all()

    return user_requests

@app.delete("/{id}")
async def delete_request(id: str) -> dict:
    user_request = await requests_database.delete(id)
    
    if not user_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user_requst with ID dose not exist."
        )
    
    return {"message": "Request info deleted successfully."}



@app.on_event("startup")
async def init_db():
    await settings.initialize_db()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=int(port), reload=True)
