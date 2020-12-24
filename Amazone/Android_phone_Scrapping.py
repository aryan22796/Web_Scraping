#all together
import csv
from bs4 import BeautifulSoup
from selenium import webdriver

def get_url(search_item):
    template="https://www.amazon.in/s?k={}&crid=1GNY6Q6AHOOKS&sprefix=and%2Caps%2C524&ref=nb_sb_ss_ts-oa-p_1_3"
    search_item=search_item.replace(' ','+')
    #add query tool
    url =template.format(search_item)
    url+='&page{}'
    return url
def extract_record(item):
    #description Url and heading
    atag=item.h2.a
    description=atag.text.strip()
    url="https://www.amazon.in/" +atag.get('href')
    try:
        
        #price
        price_present=item.find('span','a-price')
        price=price_present.find('span' ,'a-offscreen').text
    except AttributeError:
        return
    try:
        
        #rating and review
        rating=item.i.text
        review_count = item.find('span',{'class':'a-size-base','dir':'auto'}).text
    except AttributeError:
        rating=''
        review_count
    results=(description,price,rating,review_count,url)
    
    return results

def main(search_item):
    driver=webdriver.Chrome(executable_path="chromedriver.exe")
    
    record=[]
    url=get_url(search_item)
    
    for page in range(1,21):
        driver.get(url.format(page))
        soup=BeautifulSoup(driver.page_source,'html.parser')
        results =soup.find_all('div',{"data-component-type":"s-search-result"})
        
        for item in results:
            record =extract_record(item)         
            if record:
                records.append(record)
        
    driver.close()
        
    #save data as csv file
    with open('results_vs.csv','w',newline='',encoding='utf-8')as f:
        writer=csv.writer(f)
        writer.writerow(['Description','Price','Rating','ReviewCount','url'])
        writer.writerows(records)
        
    
    print(main('android phone'))