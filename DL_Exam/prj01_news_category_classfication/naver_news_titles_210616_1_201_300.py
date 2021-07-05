"""
프로젝트 - 네이버 기사 중 '경제' 분야의 기사 헤드라인을 크롤링해오기 (그 중 201-300페이지를 크롤링)
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import re

options = webdriver.ChromeOptions()  #크롬을 열 때 옵션사항
#options.add_argument('headless')  #드라이브를 직접 닫지 못한다
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver', options=options)
driver.implicitly_wait(10)  #로딩시간을 최대 10초까지 기다려준다 (그 전에 끝나면 넘어감)

df_title = pd.DataFrame()  #나중에 타이틀을 넣기 위해 빈데이터프레임 생성
title_list = []

for k in range(201, 300):
    url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101#&date=%2000:00:00&page={}'.format(k)
    driver.get(url)
    time.sleep(0.8)
    for j in range(1, 5):  #ul을 변경하기 위한 for문, 페이지에 기사가 20개씩 있는데 li는 5개씩 변하고 ul은 4개의 숫자로 이루어져있다
        for i in range(1, 6):   #li을 변경하기 위한 for문
            # 에러 예외처리의 try문
            try:
                # 다음 기사와는 li[n]값이 1~5까지 바뀌고 6번째부턴 ul[2]/li[1]로 바껴서 for문으로 돌려주면 된다
                title = driver.find_element_by_xpath(   #find_element_by_xpath = xpath로 엘리먼트를 찾아서 타이틀에 저장하라는 것
                        '//*[ @ id = "section_body"]/ul[{}]/li[{}]/dl/dt[last()]/a'.format(j, i)
                ).text
                title = (re.compile('[^가-힣|a-z|A-Z]').sub(' ', title))  #기사제목만 추출([]만 남기고 나머지는 뺀 뒤, 뺀 자리에 ' '빈칸으로 채우기)
                print(title)
                title_list.append(title) #기사 제목을 빈 리스트에 추가
            except NoSuchElementException:
                print('NoSuchElementException')
df_section_title = pd.DataFrame(title_list, columns=['title'])  #리스트로 이뤄진 기사제목들을 데이터 프레임에 넣기
df_section_title['category'] = 'Economic'
df_title = pd.concat([df_title, df_section_title], axis=0,
                     ignore_index=True)

driver.close() #드라이버 닫아주기

df_title.to_csv(
    f'./crawling_data/naver_eco_titles_201-300_{time.strftime("%Y-%m-%d", time.localtime(time.time()))}.csv',
    index=False)