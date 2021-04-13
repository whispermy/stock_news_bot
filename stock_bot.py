# from slacker import Slacker

# slack = Slacker('xoxb-1949658563270-1953364834789-Rxavpb60oLgZl1ma2LS3el8v')

# # Send a message to #general channel
# slack.chat.post_message('#stock-news-BOT', 'Hello fellow slackers!')

#----------------------imports----------------------
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

import time
from datetime import datetime

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json
#-----------definition and basic setting-----------
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options)

# send slack message function
def post_message(token, dict_val):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        #data={"channel": channel,"text": text}
        data=json.dumps(dict_val)
    )
    print(response)

# setting slack token
myToken = "xoxb-1949658563270-1953364834789-44sDT2LqthWpa8gD6qHquIUH"

# setting url
url = "https://www.hankyung.com/"

# open finance page
url = url + "finance/"
driver.get(url)
print(driver.window_handles) 
time.sleep(5)

# close popup
main = driver.window_handles
for handle in main: 
    if handle != main[0]: 
        driver.switch_to_window(handle) 
        driver.close()

print("DEBUG Message: All popup closed.\n")

# page initializing
driver.switch_to_window(main[0])
slack_msg = {'channel': '#general', 'text': ''}
# news_list = []
# page_num = 101

for page_num in range(102,112):
    # move section of topic
    url_temp = url + str(page_num).zfill(4)
    driver.get(url_temp)
    time.sleep(3)

    # save the section name
    section_name = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[1]/div[1]/h2").text
    #news_list.append(section_name)
    slack_msg['text'].append(section_name)

    # set article row
    selectArticle_ul = 1
    selectArticle_li = 1
    subpage = 2
    now = datetime.now()
    day_diff = 0

    while(True):
        if selectArticle_ul < 5:
            articleTime = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[1]/ul["+str(selectArticle_ul)+"]/li["+str(selectArticle_li)+"]/div[2]/span").text
            parceTime = datetime.strptime(articleTime, "%Y.%m.%d %H:%M")    
            date_diff = now - parceTime
            day_diff = date_diff.days
            print("DEBUG MESSAGE: 일 수 차이:",day_diff," Parce Date:",parceTime," ul:",selectArticle_ul," li:",selectArticle_li," page:",page_num," subpage:",subpage)	# 일 수 차이 : 15
            if day_diff > 0:
                if selectArticle_ul == 1 and selectArticle_li == 1 and subpage == 2:
                    print("DEBUG MESSAGE: This section has no new article.")
                # 1페이지 안에 하루치 뉴스 다 있는 경우
                # 그니까 다음 섹션 넘어가야 함.
                break

            # 제목 불러오기 및 스트링 저장, 배열 저장 (슬랙 메세지 만들기)
            news_title = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[1]/ul["+str(selectArticle_ul)+"]/li["+str(selectArticle_li)+"]/div[1]/h3/a").text
            #news_list.append(news_title)
            slack_msg['text'].append(news_title)
            print("DEBUG MESSAGE: 기사 제목:'",news_title,"' list added.")
            news_url = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[1]/ul["+str(selectArticle_ul)+"]/li["+str(selectArticle_li)+"]/div[1]/h3/a").get_attribute("href")
            #news_list.append(news_url)
            slack_msg['text'].append(news_url)
            print("DEBUG MESSAGE: 기사 URL:'",news_url,"' list added.")

        if selectArticle_ul >= 5:
            # url change or click next page
            subpage += 1
            url_sub_temp = url_temp + "?page" + str(subpage)
            elem = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[1]/div[1]/div[2]/a["+str(subpage)+"]")
            driver.execute_script("arguments[0].click();", elem)
            
            #driver.get(url_sub_temp)
            time.sleep(1)
            selectArticle_ul = 1
            selectArticle_li = 1
            # 1페이지 안에 하루치 다 모자란 경우
            # 같은 섹션 2페이지로 넘어감
        elif selectArticle_li == 5:
            selectArticle_li = 1
            selectArticle_ul += 1
        else:
            selectArticle_li += 1
        
time.sleep(1)
driver.close()
print("DEBUG MESSAGE: closed")
print(news_list)
# repeat all the tabs

# send slack bot example
post_message(myToken,slack_msg)

