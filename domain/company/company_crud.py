from domain.company.company_schema import CompanyCreate
from models import *
from sqlalchemy.orm import Session
from datetime import datetime


def create_company(db: Session, company_create: CompanyCreate, kind: Kind):
    db_company = Company(
        c_code=company_create.c_code,
        c_name=company_create.c_name,
        kind = kind
    )
    
    db.add(db_company)
    db.commit()

def get_company_by_code(db: Session, c_code: str):
    return db.query(Company).filter(Company.c_code == c_code).first()