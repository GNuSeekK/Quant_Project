from domain.price.price_schema import PriceCreate
from models import *
from sqlalchemy.orm import Session
from datetime import datetime

def create_price(db: Session, price_create: PriceCreate, company: Company):
    db_price = Price(
        company=company,
        p_date=price_create.p_date,
        price=price_create.price
    )
    
    db.add(db_price)
    db.commit()

def get_price_by_code(db: Session, company: Company):
    return db.query(Price).filter(Price.company == company).all()

def get_price_by_code_date(db: Session, company: Company, p_date: datetime):
    return db.query(Price).filter(Price.company == company).filter(Price.p_date == p_date).first()