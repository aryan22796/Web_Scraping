#all together
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import requests

def get_url(location):
    template="http://schoolsearchlist.com/schools-in-city/{}"
    url=template.format(location)
    return url

def get_record(card):
    
    atag=card.h3.a
    school_title=atag.get('head3')
    school_url=atag.get('href')
    title=atag.text.strip()
    try:
        phone=card.find('span','htxt').text.strip()
    except AttributeError:
        phone='none'
    record = (title,phone)
        
    return record

def main(location):
    records=list()
    url=get_url(location)
    #save data as csv file
    
    while True:        
        response=requests.get(url)
        soup=BeautifulSoup(response.text,'html.parser')
        cards =soup.find_all('div','address')

    
        for card in cards:
            record=get_record(card)
            records.append(record)
        try:
            url="http://schoolsearchlist.com/" + soup.find('a',{'arial-label':'Next'}).get('href')
        except AttributeError:
            break
        
    with open('kolkata.csv','w',newline='',encoding='utf-8')as f:
            writer=csv.writer(f)
            writer.writerow(['Name','phone'])
            writer.writerows(records)
main("kolkata")