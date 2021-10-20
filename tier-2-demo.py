import pandas as pd 
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from selenium import webdriver
import time

html='https://uktiersponsors.co.uk/'
driver = webdriver.Chrome()

data_dict = dict()

column_names = ["Company", "Website url", "Social url", "Town", "Industry", "Main Tier", "Sub tier", "Date Added"]
pd.DataFrame(columns=column_names).to_csv("uk-tier-2.csv", index=False, sep="\t", encoding="UTF-8")
def page_scrape(html):
    # url='https://uktiersponsors.co.uk/'
    # driver = webdriver.Chrome()
    # driver.get(html)
    html=driver.page_source
    soup_doc= BeautifulSoup(html,'lxml')
    for element in soup_doc.select('[id^="MUIDataTableBodyRow-"]'):
        # data_dict = dict()
        temp_data=element.select_one('.jss404')
        if(temp_data):
            data_dict["Company"]=temp_data.text
            if(temp_data.select_one('[id^="MuiDataTableBodyCell-"]')):
                data_dict["Social url"] = temp_data.select_one('a[href]', href=True)["href"]
            
            # if(temp_data.select_one('td.jss381 a[href]')):
            #     data_dict["Social url"] = temp_data.select_one('a[href]', href=True)["href"]
            # if(temp_data.select_one('[id^=""]')):
            #     data_dict["Town"] = temp_data.text.split("\n")
        else:
            continue

        temp_data = element.select_one('tr.jss349.jss351.jss396.jss397.jss399 a[href]')
        if(temp_data):
            temp_list=temp_data["href"]
            data_dict["Website url"] = temp_list

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
        
        
        pd.json_normalize(data_dict)
        pd.DataFrame([data_dict], columns=column_names).to_csv("uk-tier-2.csv", index=False, header=False, sep="\t", encoding="UTF-8", mode="a")        
        print(data_dict)


def click_more(driver):
    driver.find_element_by_xpath('//*[@id="pagination-next"]/span[1]').click()

try:
    driver.get("https://uktiersponsors.co.uk/")
    while True:
        click_more(driver)
        html = driver.page_source
        page_scrape(html)
        time.sleep(1)
               
finally:
    driver.quit()






        

