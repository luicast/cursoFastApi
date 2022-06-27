#python
from typing import Optional

#pydantic
from pydantic import BaseModel

#FAstAPI
from fastapi import Path, Query, Body, FastAPI

app = FastAPI()

#Models
class Location(BaseModel):
    city: str
    state: str
    country: str
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
    name: Optional[str] = Query(
        None,
        min_length=3,
        max_length=50,
        title="Person's name",
        description="The name of the person to show, Its between 3 and 50 characters",
    ), 
    age: str = Query(
        ...,
        title="Person's age",
        description = "person's age, Its a number and required",
    ),
):
    return {"name": name, "age": age}

#validations path Params

@app.get("/person/details/{person_id}")
def showPerson(
    person_id: int = Path(..., gt=0)
):
    return {"person_id": person_id}

#validations body Params
@app.put("/person/{person_id}")
def updatePerson(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person's id",
        description="The id of the person to update, Its a number and required",
        ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    result = person.dict()
    result.update(location.dict())
    return result