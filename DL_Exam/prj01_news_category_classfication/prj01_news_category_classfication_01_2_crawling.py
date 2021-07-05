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

driver.implicitly_wait(10)  #페이지가 변환되는 시간을 나타냄(너무 오래주면 에러가 난다)
#네이버 메인 뉴스 url
# url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=1'

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']  #기사별 카테고리
df_title = pd.DataFrame()  #나중에 타이틀을 넣기 위해 빈데이터프레임 생성
page_num = [334, 423, 400, 87, 128, 74]  #각 카테고리별 기사마다 페이지 수

for l in range(0, 6):  #6개의 카테고리를 위한 for문
    df_section_title = pd.DataFrame()  # 빈 데이터프레임 생성
    for k in range(1, 2):  #페이지 변경을 위한 for문((1, page_num[l]) 이게 정석이지만 너무 오래걸려서 일단 2페이지만 긁어오기
        url = 'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page={}'.format(l, k)
        driver.get(url)
        time.sleep(0.8)
        title_list = []
        for j in range(1, 5):  #ul을 변경하기 위한 for문, 페이지에 기사가 20개씩 있는데 li는 5개씩 변하고 ul은
            for i in range(1, 6):   #li을 변경하기 위한 for문
                # 에러 예외처리의 try문
                try:
                    # 다음 기사와는 li[n]값이 1~5까지 바뀌고 6번째부턴 ul[2]/li[1]로 바껴서 for문으로 돌려주면 된다
                    title = driver.find_element_by_xpath(   #find_element_by_xpath = xpath로 엘리먼트를 찾아서 타이틀에 저장하라는 것
                        '//*[ @ id = "section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(j, i)
                    ).text
                    title = (re.compile('[^가-힣|a-z|A-Z]').sub(' ', title))  #기사제목만 추출([]만 남기고 나머지는 뺀 뒤, 뺀 자리에 ' '빈칸으로 채우기)
                    print(title)
                    title_list.append(title) #기사 제목을 빈 리스트에 추가
                except NoSuchElementException:
                    print('NoSuchElementException')
    df_section_title = pd.DataFrame(title_list, columns=['title'])  #리스트로 이뤄진 기사제목들을 데이터 프레임에 넣기
    df_section_title['category'] = category[l]  #for문에서 6개의 카테고리가 담긴 l을 인덱스, 카테고리를 컬럼으로 만들어서 해당되는 카테고리 넣기
    #df_section_title은 카테고리별로 안에 값들이 달라져서, 카테고리별로 통합할 데이터프레임이 필요해서 df_title에 concat으로 매 카테고리를 합쳐주는 것
    df_title = pd.concat([df_title, df_section_title], axis=0, ignore_index=True)  #axis=0 = 행으로 이어 붙임, 기사 제목과 카테고리를 넣은 데이터프레임을 합치기

driver.close() #드라이버 닫아주기
df_title.head(30)

df_title.to_csv(f'./crawling_data/naver_news_titles_{time.strftime("%Y-%m-%d", time.localtime(time.time()))}.csv')  #크롱링한 데이터 csv파일로 저장