from pydantic import BaseModel, validator


class Kind(BaseModel):
    kind: int
    k_name: str
    
    class Config:
        from_attributes = True

class KindCreate(BaseModel):
    kind: int
    k_name: str
    
    @validator('kind', 'k_name')
    def not_empty(cls, v):
        if not v:
            raise ValueError('Must not be empty')
        return v