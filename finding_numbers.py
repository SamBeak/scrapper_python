from requests import get
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs
from selenium import webdriver

import json # json data
import openpyxl # excel data

filename = "business_listings_numbers.xlsx"
wb = openpyxl.Workbook()
sheet = wb.active


business_detail_list = []
with open('./business_number_listings.json', 'r', encoding='utf-8') as f:
    business_detail_list = json.load(f)


browser = webdriver.Chrome()

base_url = "https://bizno.net/article/"

for item in business_detail_list:
    for i in range(len(business_detail_list[item])):
        search_term = business_detail_list[item][i]["article"]
        print(f"{base_url}{license}{search_term}")
        browser.get(f"{base_url}{search_term}")     # selenium 을 사용해서 scraping을 해오겠다.

        results = []
        soup = BeautifulSoup(browser.page_source, "html.parser")
        tables = soup.find("table", class_="table_guide01")
        trs = tables.find_all("tr")
        for tr in trs:
            th = tr.find('th')
            if th.string == "전화번호":
                ph_num = tr.find('td')
            else:
                continue
        business_data = {
            'phnum' : ph_num.string
        }
        results.append(business_data)
        sheet.cell(row=i+1, column=1).value = business_data['phnum']
wb.save(filename)
browser.quit()