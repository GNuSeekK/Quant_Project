from domain.finance.finance_schema import FinanceCreate
from models import *
from sqlalchemy.orm import Session
from datetime import datetime


def create_finance(db: Session, finance_create: FinanceCreate, company: Company):
    db_finance = Finance(
        company=company,
        f_date=finance_create.f_date,
        sales=finance_create.sales,
        gm=finance_create.gm,
        ni=finance_create.ni,
        asset=finance_create.asset,
        ca=finance_create.ca,
        cl=finance_create.cl,
        issued_shares=finance_create.issued_shares,
        bps=finance_create.bps,
        eps=finance_create.eps
    )
    
    db.add(db_finance)
    db.commit()

def get_finance_by_code(db: Session, company: Company):
    return db.query(Finance).filter(Finance.company == company).all()

def get_finance_by_code_date(db: Session, company: Company, f_date: datetime):
    return db.query(Finance).filter(Finance.company == company).filter(Finance.f_date == f_date).first()