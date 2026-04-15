import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://ev.or.kr/nportal/partcptn/initQnaAction.do')

target_end_year = '2018'

css_wrap = '.board_con'
css_title = '.board_title'
css_date = '.date'
css_page_next = '#pageingPosition .next'

board_year_curr = target_end_year
data = []

while board_year_curr >= target_end_year:
    board = driver.find_elements(By.CSS_SELECTOR, css_wrap)
    btn_next = driver.find_element(By.CSS_SELECTOR, css_page_next)

    for x in board:
        title = x.find_element(By.CSS_SELECTOR, css_title)
        date = x.find_element(By.CSS_SELECTOR, css_date).text

        board_year_prev = board_year_curr
        board_year_curr = date[:4]

        if title.text[:6] == '[충전기운영':
            if board_year_prev == board_year_curr:
                title_re = title.find_element(By.TAG_NAME, 'em').text
                data.append(dict(제목 = title_re, 날짜 = date))
            else:
                with open(f'ev_or_kr_csv/ev_or_kr_{board_year_prev}.csv', mode='w', encoding='utf-8', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['날짜', '제목'])
                    writer.writeheader()
                    writer.writerows(data)
                
                data = []

    btn_next.click()
    time.sleep(5)
