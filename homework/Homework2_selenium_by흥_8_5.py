# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 18:13:33 2017

@author: hslee3
"""

from selenium import webdriver as wb
from bs4 import BeautifulSoup as bs
import datetime
import re

driver = wb.Chrome('C:/Users/Whi Kwon/Documents/GitHub/python_script/chromedriver.exe')
driver.implicitly_wait(2)

today = datetime.date.today()
week_ago = today - datetime.timedelta(7)
week_day_ago = today - datetime.timedelta(8)
today = today.strftime('%Y/%m/%d')
week_ago = week_ago.strftime('%Y/%m/%d')
week_day_ago = week_day_ago.strftime('%Y/%m/%d')

pattern = re.compile('(대전|충청|충북|충남|세종)')

#%%
#조달청계약요청
driver.get("http://www.g2b.go.kr:8091/cm/contstus/fwdPpsItemContractReqStus.do")
driver.find_element_by_xpath('//*[@id="prodNm"]').send_keys('전반')
driver.find_element_by_xpath('//*[@id="srchFrm"]/div[2]/div/a[1]/span').click()

date_list = []
price_list = []
number_list = []
region_list = []

pages = 3

for i in range(pages):
    # html source 
    html = driver.page_source
    # soup
    soup = bs(html, 'lxml')
    # 데이터 가져오기
    date = [j.text.strip() for j in soup.find_all(attrs = {'class':'tc'}) if '/' in j.text]
    price = [j.text.strip() for j in soup.find_all(attrs = {'class':'tr'}) if '원' in j.text]
    price = [int(i.replace('원','').replace(',','')) for i in price]  # string to int 변환
    number = [j.text.strip() for j in soup.find_all(name = 'a', attrs = {'href' : '#'}) if len(j.text) > 15]
    # region
    region = [j.text.strip() for j in soup.find_all(attrs = {'class':'tl'})]
    region = region[1::2]
    
    # for문 대상은 date수를 대상으로.
    for j in range(len(date)):
        # 가격 2억 기준 if문
        if price[j] >= 2e8:
            # 패턴 매칭
            if re.match(pattern, region[j]):
                region_list.append(region[j])
            # 패턴 없을 경우, 내용 확인
            else:
                driver.find_element_by_link_text(number[j]).click()
                # 추가 기업 정보 확인 필요 
                # Nice 기업 정보 "https://www.nicebizinfo.com/ep/EP0100M001GE.nice?itgSrch=리젠코+정순희"
                # 뒤로 가기
                driver.back()
        # 2억 안 넘을 경우 continue 
        else:
            continue
    # date수가 30면 다음 게시판으로
    if len(date) == 30:
        driver.find_element_by_xpath('//*[@id="pagination"]/a').click()
    # date수가 30개 안 되면 종료
    else:
        print("{} Pages loaded, work finished.".format(i+1))
        break

