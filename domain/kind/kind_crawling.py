from quant_infos.wics_code import *
from domain.kind import kind_crud, kind_schema
from database import get_db
import datetime
import requests
from models import *
from sqlalchemy.orm import Session

def wics_company_crawling(
        wics : str, 
        dt : datetime.datetime = datetime.datetime.now()):
    while True:
        url = wics_url(dt.strftime('%Y%m%d'), wics)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['list'] == []:
                dt = dt - datetime.timedelta(days=1)
            else:
                return data['list']
        else:
            return None
        
def update_kindtable():
    for wics in WICS:
        # data = wics_company_crawling(wics)
        kind = kind_schema.KindCreate(
            kind = wics,
            k_name = WICS[wics]
        )
        with get_db() as db:
            if kind_crud.get_kind_by_kind(db = db, kind = wics) is None:
                kind_crud.create_kind(db = db, kind_create = kind)
                print(f'new kind created : {wics}')
        
