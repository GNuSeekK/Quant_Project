from quant_infos.wics_code import *
from domain.company import company_crud, company_schema
from domain.kind import kind_crud
from database import get_db
import datetime
import requests
from models import *
from sqlalchemy.orm import Session
import pandas as pd

def update_company_table(dt : datetime.datetime = datetime.datetime.now()):
    company_wics = {}
    for wics in WICS:
        if 10000 > wics >= 1000:
            url = wics_url(dt.strftime('%Y%m%d'), wics)
            while True:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if data['list'] == []:
                        dt = dt - datetime.timedelta(days=1)
                        url = wics_url(dt.strftime('%Y%m%d'), wics)
                    else:
                        for company in data['list']:
                            company_wics[company["CMP_CD"]] = wics
                        break
    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
    krx = pd.read_html(url,header=0)[0]
    # 데이터 정리
    krx = krx[['종목코드','회사명', '업종', '상장일']]
    krx['종목코드'] = krx['종목코드'].map('{:06d}'.format)
    krx['상장일'] = pd.to_datetime(krx['상장일'])
    with get_db() as db:
        for i in range(len(krx)):
            company = company_schema.CompanyCreate(
                c_code = krx['종목코드'][i],
                c_name = krx['회사명'][i],
                real_kind = krx['업종'][i],
                public_date = krx['상장일'][i]
            )
            try:
                if company_crud.get_company_by_code(db = db, c_code = krx['종목코드'][i]) is None:
                    kind = kind_crud.get_kind_by_kind(db = db, kind = company_wics[krx['종목코드'][i]])
                    company_crud.create_company(db = db, company_create = company, kind = kind)
            except:
                print(f'error occured : {krx["회사명"][i]}')