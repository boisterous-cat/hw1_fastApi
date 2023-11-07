from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, date, time
from operator import attrgetter
from fastapi.encoders import jsonable_encoder

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root()->Timestamp:
    max_id = max(post_db, key=attrgetter('id')).id
    return post_db[max_id]

@app.get("/dog")
def dogByType(dogType:DogType)->list:
    #list(dogs_db.keys())[list(dogs_db.values()).index(dogType)]
    result=[]
    for key,value in dogs_db.items():
        curDog = value
        curType = curDog.kind
        if (curType.__contains__(dogType)):
            result.append(curDog)
    return result

@app.get("/dog/{pk}")
def dogByPk(pk:int)->Dog:
    result:Dog
    for key,value in dogs_db.items():
        curDog = value
        curPk = curDog.pk
        if (curPk==pk):
            result = curDog
    return result

@app.post("/post")
def createTimestamp():
    max_id = max(post_db, key=attrgetter('id')).id
    new_id = max_id+1
    new_timestamp = Timestamp(id=new_id, timestamp=round(datetime.now().timestamp()))
    post_db.append((new_timestamp))
    return new_timestamp

@app.post("/dog", response_model=Dog, summary='Create Dog')
def createDog(dog:Dog)->Dog:
    dogId=0
    for key, value in dogs_db.items():
        if (value.pk == dog.pk):
            raise HTTPException(status_code=409,detail='The specified PK already exists.')
    if (dog.pk in dogs_db):
        raise HTTPException(status_code=409,detail='The specified PK already exists.')
    else:
        dogs_db[dog.pk]=dog
    return dog

@app.patch("/dog/{pk}", response_model=Dog, summary='Update Dog')
def updateDog(pk:int, dog:Dog)->Dog:

    if (pk not in dogs_db):
        raise HTTPException(status_code=409,detail='Dog not found')
    else:
        dogs_db.update({pk:dog})
    return dogs_db[pk]