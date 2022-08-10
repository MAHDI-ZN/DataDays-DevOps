from fastapi import FastAPI , Path
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    name : str
    lastName : str

DefaultNameSet = {
    1:{
        "name" : "John",
        "lastName" : "Wick"
    },
    2:{
        "name" : "John",
        "lastName" : "Snow"
    },
    3:{
        "name" : "Walter",
        "lastName" : "White"
    }
}

@app.get("/ExtractPerson/{Id}")
def Extract_Full_Name_Via_Id(Id: int = Path(None,description="Enter the Id of person you want his name:",ge=1,le=10)):
    return DefaultNameSet[Id]

@app.post("/CreatePerson/{Id}")
def Create_Person( item: Person,Id: int = Path(None,description="Enter the Id you want to associate with your person:",ge=1,le=10)):
    if id in DefaultNameSet:
        return {"Error" : "Person Id already exists"}
    DefaultNameSet[Id] = item
    return {"Created": item}

@app.put("/UpdatePerson/{Id}")
def Update_Person( item: Person,Id: int = Path(None,description="Enter the Id of the person you want to update:",ge=1,le=10)):
    if Id not in DefaultNameSet:
        return {"Error" : "Person Id doesn't exist"}
    DefaultNameSet[Id] = item
    return {"Update": item}

@app.delete("/DeletePerson/{Id}")
def Delete_Person(Id: int = Path(None,description="Enter the Id of the person you want to delete:",ge=1,le=10)):
    if Id not in DefaultNameSet:
        return {"Error" : "Person Id doesn't exist"}
    DefaultNameSet[Id] = None;
    return {"Deleted": Id}
