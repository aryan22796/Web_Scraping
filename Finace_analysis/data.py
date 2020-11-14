import re
import json
import csv
from io import StringIO
from bs4 import BeautifulSoup ,soup
from selenium import webdriver
import requests

driver=webdriver.Chrome(executable_path="F:\Web_Scraping\chromedriver.exe")


url_status='https://in.finance.yahoo.com/quote/{}/key-statistics?p={}'
url_profile='https://in.finance.yahoo.com/quote/{}/profile?p={}'
url_finacials='https://in.finance.yahoo.com/quote/{}/financials?p={}'

stock='F'

response= requests.get(url_finacials.format(stock,stock))


pattern= re.compile(r'\s--\sData\s--\s')
script_data=soup.find('script',text=pattern).contents[0]

start =script_data.find("context")-2

json_data=json.loads(script_data[start:-12])

annual_is=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
quertly_is=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistoryQuarterly']['incomeStatementHistory']

anunual_cf=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
quertly_cf=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistoryQuarterly']['cashflowStatements']

annual_bs=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']
quertly_bs=json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistoryQuarterly']['balanceSheetStatements']