#python
from typing import Optional

#pydantic
from pydantic import BaseModel

#FAstAPI
from fastapi import Query, Body, FastAPI

app = FastAPI()

#Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def Home():
    return {"message": "Hello World"}

    #request and response Body

@app.post("/person/new")
def createPerson(person: Person = Body(...)):
    return person

#validations Query Params

@app.get("/person/details")
def showPerson(
    name: Optional[str] = Query(None, min_length=3, max_length=10),
    age: str = Query(...),
):
    return {"name": name, "age": age}
    