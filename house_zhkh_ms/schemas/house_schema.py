from pydantic import BaseModel

class HouseInfo(BaseModel):
    id: int
    street: str

class NewHouseRequest(BaseModel):
    house_street: str