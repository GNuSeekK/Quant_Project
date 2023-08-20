from domain.company.company_schema import CompanyCreate
from models import *
from sqlalchemy.orm import Session
from datetime import datetime


def create_company(db: Session, company_create: CompanyCreate, kind: Kind):
    db_company = Company(
        c_code=company_create.c_code,
        c_name=company_create.c_name,
        kind = kind,
        real_kind=company_create.real_kind,
        public_date=company_create.public_date,
    )
    
    db.add(db_company)
    db.commit()

def get_company_by_code(db: Session, c_code: str):
    return db.query(Company).filter(Company.c_code == c_code).first()

def get_company_code_list(db: Session):
    return db.query(Company.c_code).all()