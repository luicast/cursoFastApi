#python
from typing import Optional
from enum import Enum

#pydantic
from pydantic import BaseModel, SecretStr, EmailStr
from pydantic import Field

#FAstAPI
from fastapi import UploadFile, status, HTTPException, FastAPI
from fastapi import Path, Query, Body, Form, Header, Cookie, File

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

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=30,
        example = "John"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=30,
        example = "Doe"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example = 25
        )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
class Person(PersonBase):
    password: str = Field(..., min_length=8)
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "John",
    #             "last_name": "Doe",
    #             "age": 25,
    #             "hair_color": "brown",
    #             "is_married": True
    #         }
    #     }

class Login(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    message: str = Field(default="Login successful")


@app.get(
    path="/", 
    status_code=status.HTTP_200_OK,
    tags=["Home"]
    )
def Home():
    return {"message": "Hello World"}

#request and response Body

@app.post(
    path="/person/new", 
    response_model=Person, 
    response_model_exclude={"password"},
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
    )
def createPerson(person: Person = Body(...)):
    return person

#validations Query Params

@app.get(
    path="/person/details",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
def showPerson(
    name: Optional[str] = Query(
        None,
        min_length=3,
        max_length=50,
        title="Person's name",
        description="The name of the person to show, Its between 3 and 50 characters",
        example="Joy"
    ), 
    age: str = Query(
        ...,
        title="Person's age",
        description = "person's age, Its a number and required",
        example = "25"
    ),
):
    return {"name": name, "age": age}

#validations path Params

persons = [1,2,3,4,5]

@app.get(
    path="/person/details/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
def showPerson(
    person_id: int = Path(
        ...,
        gt=0,
        example=123
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Person not found"
        )
    return {"person_id": person_id}

#validations body Params
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Persons"]
    )
def updatePerson(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person's id",
        description="The id of the person to update, Its a number and required",
        example=123
        ),
    person: Person = Body(...),
    #location: Location = Body(...)
):
    #result = person.dict()
    #result.update(location.dict())
    #return result
    return person

@app.post(
    path="/login",
    response_model=Login,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
def login(username:str = Form(...), password:SecretStr = Form(...)):
    return Login(username=username)

#cookies and headers params

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["contact"]
    )
def contact(
    first_name: str = Form(...,
    max_length=20,
    min_length=3
    ),
    last_name: str = Form(...,
    max_length=20,
    min_length=3
    ),
    email: EmailStr = Form(...),
    message: str = Form(...,
    max_length=200,
    min_length=20,
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)

):
    return user_agent

#files
@app.post(
    path="/post-image",
    status_code=status.HTTP_200_OK,
    tags=["Files"]
    )
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename":image.filename,
        "Format":image.content_type,
        "Size(kb)":round(len(image.file.read())/1024,2)
    }

