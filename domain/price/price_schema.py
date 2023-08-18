from pydantic import BaseModel, validator
from domain.company.company_schema import Company
from datetime import date
class Price(BaseModel):
    company: Company
    p_date: date
    price: int
    
    class Config:
        from_attributes = True

class PriceCreate(BaseModel):
    p_date: date
    price: int
