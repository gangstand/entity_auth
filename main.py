from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from entity_auth import EntityAuth

app = FastAPI()


class User(BaseModel):
    username: str
    password: str


class UtilsEntityAuth(EntityAuth):
    secret_key = "secret"


instance_auth = UtilsEntityAuth


@app.post('/login')
def login(data: User, authorize: instance_auth = Depends()):
    if data.username != "test" or data.password != "test":
        raise HTTPException(status_code=401, detail="Bad username or password")
    access_token = authorize.create_access_token(subject=data.username)
    return {"access_token": access_token}


@app.get('/user')
def user(authorize: instance_auth = Depends()):
    authorize.jwt_required()
    current_user = authorize.get_jwt_subject()
    return {"user": current_user}
