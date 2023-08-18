import contextlib # 의존성 주입

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

config = Config('.env')
SQLALCHEMY_DATABASE_URL = Config('SQLALCHEMY_DATABASE_URL') # 디비 접속 주소, 프로젝트 루트 디렉터리에 저장한다는 의미
SQLALCHEMY_DATABASE_URL = 'sqlite:///./quant.db'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread' : False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# autocommit은 commit 사인 줄대 저장하게 만드는 것

Base = declarative_base()    
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)

@contextlib.contextmanager # 어노테이션 적용
def get_db():
    db = SessionLocal()
    try:
        yield db # 제너레이터로 next를 통해 불러오게 함
    finally:
        db.close()
# with get_db() as db: 가 사용 가능해짐