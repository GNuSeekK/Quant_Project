from quant_infos.wics_code import *
from domain.company import company_crud
from domain.price import price_crud
from domain.price.price_schema import *
from database import get_db
import datetime
import requests
from models import *
from sqlalchemy.orm import Session
from dateutil.relativedelta import relativedelta
import pandas as pd
import Keesung_logging
from bs4 import BeautifulSoup
from tqdm import tqdm
import numpy as np
import datetime as dt

def update_price_table():
    with get_db() as db:
        company_list = company_crud.get_company_code_list(db = db)

    logger = Keesung_logging.my_logger()
    timeframe = 'day'
    count = '1000'

    for code in tqdm(company_list, desc='ftbl update'):
        code = code.c_code
        try:
            url = 'https://fchart.stock.naver.com/sise.nhn?requestType=0'
            # price_url = url + '&symbol=' + code + '&timeframe=' + timeframe + '&count=' + count
            price_url = f'{url}&symbol={code}&timeframe={timeframe}&count={count}'
            price_data = requests.get(price_url)
            price_data_bs = BeautifulSoup(price_data.text, 'lxml')
            item_list = price_data_bs.find_all('item')
            
            

            with get_db() as db:
                for item in item_list:
                    temp_data = item['data']
                    datas = temp_data.split('|') # 날짜, 시가, 고가, 저가, 종가, 거래량
                    date = dt.datetime.strptime(datas[0], '%Y%m%d')
                    price = PriceCreate(
                        p_date = date,
                        price = datas[4]
                    )
                    company = company_crud.get_company_by_code(db = db, c_code = code)
                    if price_crud.get_price_by_code_date(db = db, company = company, p_date = date) is None:
                        price_crud.create_price(db = db, price_create = price, company = company)
                    # 수정 주가 반영하는 코드 추가 필요
                    
        except Exception as e:
            logger.error(f'{code} - {e}')
    logger.error_check()