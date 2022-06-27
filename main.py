#python
from typing import Optional
from enum import Enum

#pydantic
from pydantic import BaseModel
from pydantic import Field

#FAstAPI
from fastapi import Path, Query, Body, FastAPI

app = FastAPI()

#Models

class HairColor(Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    BLACK = "black"
    BROWN = "brown"
    WHITE = "white"
    OTHER = "other"
class Location(BaseModel):
    city: str = Field(
    ...,
    min_length = 0
  );
    state: str = Field(...)
    country: Optional[str] = Field(default = None);
class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=30
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=30
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
        )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "age": 25,
                "hair_color": "brown",
                "is_married": True
            }
        }


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
    #location: Location = Body(...)
):
    #result = person.dict()
    #result.update(location.dict())
    #return result
    return person