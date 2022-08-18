import pickle
import redis
from fastapi import FastAPI, Path
from pydantic import BaseModel
redis_client = redis.Redis(host='myred', port=6379, db=0)


app = FastAPI()


class Person(BaseModel):
    name: str
    lastName: str


if redis_client.get('dictionary') is None:
    DefaultNameSet = {
        1: {
            "name": "John",
            "lastName": "Wick"
        },
        2: {
            "name": "John",
            "lastName": "Snow"
        },
        3: {
            "name": "Walter",
            "lastName": "White"
        }
    }
else:
    DefaultNameSet = pickle.loads(redis_client.get('dictionary'))


@app.get("/ExtractPerson/{id}")
def extract_full_name_via_id(
        id: int = Path(None, description="Enter the id of person you want his name:", ge=1, le=10)):
    return DefaultNameSet[id]


@app.post("/CreatePerson/{id}")
def create_person(item: Person,
                  id: int =
                  Path(None, description="Enter the id you want to associate with your person:", ge=1, le=10)):
    if id in DefaultNameSet:
        return {"Error": "Person id already exists"}
    DefaultNameSet[id] = item
    redis_client.set('dictionary', pickle.dumps(DefaultNameSet))
    return {"Created": item}


@app.put("/UpdatePerson/{id}")
def update_person(item: Person,
                  id: int = Path(None, description="Enter the id of the person you want to update:", ge=1, le=10)):
    if id not in DefaultNameSet:
        return {"Error": "Person id doesn't exist"}
    DefaultNameSet[id] = item
    redis_client.set('dictionary', pickle.dumps(DefaultNameSet))
    return {"Update": item}


@app.delete("/DeletePerson/{id}")
def delete_person(id: int = Path(None, description="Enter the id of the person you want to delete:", ge=1, le=10)):
    if id not in DefaultNameSet:
        return {"Error": "Person id doesn't exist"}
    del DefaultNameSet[id]
    redis_client.set('dictionary', pickle.dumps(DefaultNameSet))
    return {"Deleted": id}
