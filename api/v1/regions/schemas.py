from pydantic import BaseModel


# Public partner-related models:
class RegionsRussiaSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
