''' stock news crwalling and send slack bot

2021.04.19 pylint all clear.
'''
# ----------------------imports----------------------
import time
from datetime import datetime
import os
import locale
import requests
from selenium import webdriver
# from bs4 import BeautifulSoup
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError
# import json

# -----------definition and basic setting-----------
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options)

# setting locale to use Korean
locale.setlocale(locale.LC_ALL, '')

# setting slack token
MYTOKEN = "yy"

def post_message(token, channel, text):
    ''' this function send slack message
     : token: slack bot token
     : channel: channel name to send messages using slack bot
     : text: messages, it must be 'str' type variable.
    '''
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)

def get_articles(news_msg):
    ''' this function get articles from hankyung.com

     : news_msg: news text variable. it must be 'str' type variable.
    '''
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
    now = datetime.now()
    news_list = []

    today = now.date().strftime('%Y년 %m월 %d일 %A')
    news_list.append(today+' 경제 뉴스 모음\n\n\n')
    # page_num = 101

    for page_num in range(102,112):
        # move section of topic
        url_temp = url + str(page_num).zfill(4)
        driver.get(url_temp)
        time.sleep(3)

        # save the section name
        xpath_val = "/html/body/div/div[3]/div[1]/div[1]/div[1]/h2"
        section_name = driver.find_element_by_xpath(xpath_val).text
        news_list.append('\n\n---------------- '+section_name+' ------------------')

        # set article rowvnchs
        selectarticle_ul = 1
        selectarticle_li = 1
        subpage = 2
        day_diff = 0

        while True:
            if selectarticle_ul < 5:
                xpath_val = "/html/body/div/div[3]/div[1]/div[1]/ul["+str(selectarticle_ul)+"]/li["+str(selectarticle_li)+"]/div[2]/span"
                articletime = driver.find_element_by_xpath(xpath_val).text
                parcetime = datetime.strptime(articletime, "%Y.%m.%d %H:%M")
                date_diff = now - parcetime
                day_diff = date_diff.days
                print("DEBUG MESSAGE: 일 수 차이:",day_diff," Parce Date:",parcetime," ul:",selectarticle_ul," li:",selectarticle_li," page:",page_num," subpage:",subpage)	# 일 수 차이 : 15
                if day_diff > 0:
                    if selectarticle_ul == 1 and selectarticle_li == 1 and subpage == 2:
                        print("DEBUG MESSAGE: This section has no new article.")
                    # 1페이지 안에 하루치 뉴스 다 있는 경우
                    # 그니까 다음 섹션 넘어가야 함.
                    break

                # 제목 불러오기 및 스트링 저장, 배열 저장 (슬랙 메세지 만들기)
                xpath_val = "/html/body/div/div[3]/div[1]/div[1]/ul["+str(selectarticle_ul)+"]/li["+str(selectarticle_li)+"]/div[1]/h3/a"
                news_title = driver.find_element_by_xpath(xpath_val).text
                news_list.append(news_title)
                print("DEBUG MESSAGE: 기사 제목:'",news_title,"' list added.")
                news_url = driver.find_element_by_xpath(xpath_val).get_attribute("href")
                news_list.append(news_url)
                print("DEBUG MESSAGE: 기사 URL:'",news_url,"' list added.")

            if selectarticle_ul >= 5:
                # url change or click next page
                subpage += 1
                # url_sub_temp = url_temp + "?page" + str(subpage)
                xpath_val = "/html/body/div/div[3]/div[1]/div[1]/div[2]/a["+str(subpage)+"]"
                elem = driver.find_element_by_xpath(xpath_val)
                driver.execute_script("arguments[0].click();", elem)

                #driver.get(url_sub_temp)
                time.sleep(1)
                selectarticle_ul = 1
                selectarticle_li = 1
                # 1페이지 안에 하루치 다 모자란 경우
                # 같은 섹션 2페이지로 넘어감
            elif selectarticle_li == 5:
                selectarticle_li = 1
                selectarticle_ul += 1
            else:
                selectarticle_li += 1

    time.sleep(1)
    # driver.close()
    news_list.append('\n\n---------------- 뉴스 끝 ------------------')
    # news_list.append('https://finviz.com/map.ashx')
    # print("DEBUG MESSAGE: page closed.")
    # print(news_list)

    # get US stock data 
    time.sleep(1)
    news_list.append('\n\n------------- 미 증시 map ------------------')
    # url = "https://finviz.com/map.ashx"
    # driver.get(url)
    # time.sleep(1)
    # xpath_val = "/html/body/div[2]/div/div[1]/div[3]/div/a[1]"
    # driver.find_element_by_xpath(xpath_val).click()
    # time.sleep(5)
    # pict = driver.find_element_by_class_name("export-image").get_attribute("src")
    # news_list.append(pict)
    pict = "https://finviz.com/map.ashx"
    news_list.append(pict)

    driver.close()
    print("DEBUG MESSAGE: page closed.")
    news_list.append('\n\n------------- 미 증시 map 끝 ------------------')

    for msg in news_list:
        news_msg = news_msg+'\n'+msg
    print(news_msg)

    return news_msg

    

# create variable
NEWS = ''

# send slack bot all messages
post_message(MYTOKEN,'#general',get_articles(NEWS))
print("DEBUG MESSAGE: send slack message:",NEWS)

print("DEBUG MESSAGE: program closed.")
os._exit(1)
