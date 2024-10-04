from pydantic import BaseModel, ConfigDict

class KittenBase(BaseModel):
    color: str
    age: int
    description: str
    breed: str

    class Config(ConfigDict):
        orm_mode = True

class KittenCreate(KittenBase):
    pass

class KittenRead(KittenCreate):
    id: int

    class Config:
        orm_mode = True

