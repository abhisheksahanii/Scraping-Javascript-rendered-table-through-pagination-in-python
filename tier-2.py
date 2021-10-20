import pandas as pd 
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import re
import pyshorteners

url='https://uktiersponsors.co.uk/'
url_r=requests.get(url)


driver = webdriver.Chrome()
driver.get(url)


html = driver.page_source
soup_doc= BeautifulSoup(html,'lxml')
shortener=pyshorteners.Shortener()

column_names = ["Company", "Website url", "Social url", "Town", "Industry", "Main Tier", "Sub tier", "Date Added"]
pd.DataFrame(columns=column_names).to_csv("uk-tier-2.csv", index=False, sep="\t", encoding="UTF-8")
def scrape_table():
    for element in soup_doc.select_one('[class~="jss395"]'):
        data_dict = dict()
        temp_data=element.select('[id^="MUIDataTableBodyRow-"]')
        if(temp_data):
            data_dict["Company"]=temp_data.select_one('.jss404').text
            if(temp_data.select_one('[data-testid^="MuiDataTableBodyCell-1-0"]')):
                data_dict["Website url"] = shortener.tinyurl.short(temp_data.select_one('a[href]', href=True)["href"])
            # if(temp_data.select_one('td.jss381 a[href]')):
            #     data_dict["Social url"] = temp_data.select_one('a[href]', href=True)["href"]
            # if(temp_data.select_one('[id^=""]')):
            #     data_dict["Town"] = temp_data.text.split("\n")    
        else:
            continue

        temp_data = element.select_one('tr.jss349.jss351.jss396.jss397.jss399')
        for a in temp_data.select('a[href]',href=True):
            temp_list=a["href"]
            data_dict["Social url"] = temp_list

        temp_list=[]
        if(temp_data):
            rows=element.find_all('td')
            for row in rows:
                temp_list.append(row.text.strip())
            
            data_dict['Town'] = temp_list[7]
            data_dict['Industry'] = temp_list[9]
            data_dict['Main Tier'] = temp_list[11]
            data_dict['Sub tier'] = temp_list[13]
            data_dict['Date Added'] = temp_list[15]

        for key in data_dict.keys():
            if(type(data_dict[key]) == str):
                data_dict[key] = re.sub(r"\s+", " ", data_dict[key]).strip()

        pd.DataFrame([data_dict], columns=column_names).to_csv("uk-tier-2.csv", index=False, header=False, sep="\t", encoding="UTF-8", mode="a")

