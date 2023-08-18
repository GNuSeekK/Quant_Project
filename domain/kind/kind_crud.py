from domain.kind.kind_schema import KindCreate
from models import *
from sqlalchemy.orm import Session
from datetime import datetime


def create_kind(db: Session, kind_create: KindCreate):
    db_kind = Kind(
        kind=kind_create.kind,
        k_name=kind_create.k_name
    )
    
    db.add(db_kind)
    db.commit()

def get_kind_by_kind(db: Session, kind: str):
    return db.query(Kind).filter(Kind.kind == kind).first()