from pydantic import BaseModel, validator
from domain.kind.kind_schema import Kind
from domain.company.company_schema import Company
from datetime import date

class Finance(BaseModel):
    company: Company
    f_date: date
    sales: int
    gm: int
    ni: int
    asset: int
    ca: int
    cl: int
    issued_shares: int
    bps: int
    eps: int
    
    class Config:
        from_attributes = True

class FinanceCreate(BaseModel):
    f_date: date
    sales: int
    gm: int
    ni: int
    asset: int
    ca: int
    cl: int
    issued_shares: int
    bps: int
    eps: int
    