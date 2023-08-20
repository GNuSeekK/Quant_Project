from quant_infos.wics_code import *
from domain.company import company_crud
from domain.finance import finance_crud
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

def update_finance_table():
    start_year = dt.datetime.now().year - 3
    with get_db() as db:
        company_list = company_crud.get_company_code_list(db = db)
    logger = Keesung_logging.my_logger()
    for code in tqdm(company_list, desc='ftbl update'):
        code = code.c_code
        try:
            invest_url = f'https://comp.fnguide.com/SVO2/ASP/SVD_Invest.asp?pGB=1&gicode=A{code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=105&stkGb=701'
            invest_page = requests.get(invest_url)
            fs_url = f'https://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{code}&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701'
            fs_page = requests.get(fs_url)
            soup = BeautifulSoup(invest_page.text, "html.parser")
            # 수정평균주식수
            stock = soup.find_all('tr', class_= 'c_grid1_1 rwf acd_dep2_sub')
            issued_shares = [x.text for x in stock if '주식수' in x.text] # 크롤링 데이터
            index = str(issued_shares).find('수정')
            issued_shares = str(issued_shares)[index:]
            issued_shares = issued_shares.replace('\\n', ' ')
            issued_shares = issued_shares.replace('\\xa0', '0')
            issued_shares = issued_shares.replace(',', '')
            issued_shares = issued_shares.split(' ')[:6]
            # 날짜, EPS, BPS
            invest_df = pd.read_html(invest_page.text, index_col = 0)[3]
            fs_df = pd.read_html(fs_page.text, index_col = 0)
            acc_month = invest_df.columns.tolist()[-2].split('/')[1] # account month 결산월
            df = []
            for year in range(start_year, dt.datetime.now().year):
                column = [x for x in invest_df.columns.tolist() if f'{year}/{acc_month}' in x]
                if len(column) > 0:
                    # 회사코드 append
                    text_list = []
                    text_list.append("'" + code + "'") 
                    # column 설정
                    column = column[0]
                    # f_date append
                    f_date = dt.datetime(year,int(acc_month),1) + relativedelta(months=5)
                    # f_date = f"'{str(f_date)[:10]}'"
                    text_list.append(f_date) 
                    # sales append (매출액)
                    sales = str(fs_df[0][column]['매출액']).split('.')[0]
                    text_list.append(sales)
                    # gm append (매출총이익)
                    gm = str(fs_df[0][column]['매출총이익']).split('.')[0]
                    text_list.append(gm)
                    # ni append (당기순이익)
                    ni = str(fs_df[0][column]['당기순이익']).split('.')[0]
                    text_list.append(ni)
                    # asset append (자산)
                    asset = str(fs_df[2][column]['자산']).split('.')[0]
                    text_list.append(asset)
                    # ca append (유동자산)
                    index = [x for x in fs_df[2].index.tolist() if '유동자산' in x][0]
                    ca = str(fs_df[2][column][index]).split('.')[0]
                    text_list.append(ca)
                    # cl append (유동부채)
                    index = [x for x in fs_df[2].index.tolist() if '유동부채' in x][0]
                    cl = str(fs_df[2][column][index]).split('.')[0]
                    text_list.append(cl)
                    # issued_shares append
                    index = invest_df.columns.tolist().index(column)
                    text_list.append(str(issued_shares[index+1]))
                    # bps append
                    index = [x for x in invest_df.index.tolist() if 'BPS계산' in x][0]
                    bps = invest_df[column][index] 
                    text_list.append(str(bps)) 
                    # eps append
                    index = [x for x in invest_df.index.tolist() if 'EPS계산' in x][0]
                    eps = invest_df[column][index]
                    text_list.append(str(eps))
                    if np.nan not in text_list:
                        df.append(text_list)
                    else:
                        logger.error(f'Error Code : You have Null Data in {code}')
            df = pd.DataFrame(df)
            with get_db() as db:
                company = company_crud.get_company_by_code(db = db, c_code = code)
                for i in range(len(df)):
                    finance = Finance(
                        f_date = df.iloc[i,1],
                        sales = df.iloc[i,2],
                        gm = df.iloc[i,3],
                        ni = df.iloc[i,4],
                        asset = df.iloc[i,5],
                        ca = df.iloc[i,6],
                        cl = df.iloc[i,7],
                        issued_shares = df.iloc[i,8],
                        bps = df.iloc[i,9],
                        eps = df.iloc[i,10],
                    )
                    if finance_crud.get_finance_by_code_date(db = db, c_code = code, f_date = finance.f_date) is None:
                        finance_crud.create_finance(db = db, finance_create = finance, company = company)
                    # print(f'{code} - {company.c_name} - {finance.f_date} - {finance.sales} - {finance.gm} - {finance.ni} - {finance.asset} - {finance.ca} - {finance.cl} - {finance.issued_shares} - {finance.bps} - {finance.eps}')
                    
        except Exception as e:
            logger.error(f'{code} - {e}')
    logger.error_check()