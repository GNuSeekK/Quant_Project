from pydantic import BaseModel, validator
from domain.kind.kind_schema import Kind

class Company(BaseModel):
    c_code: str
    c_name: str
    kind: Kind
    
    class Config:
        from_attributes = True

class CompanyCreate(BaseModel):
    c_code: str
    c_name: str
    
    @validator('c_code', 'c_name')
    def not_empty(cls, v):
        if not v:
            raise ValueError('Must not be empty')
        return v