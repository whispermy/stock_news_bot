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
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller as AutoChrome
import shutil
# from bs4 import BeautifulSoup
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError
# import json

def chromedriver_update():
    ''' this function auto update chrome driver
     : there is no arguments
    '''
    chrome_ver = AutoChrome.get_chrome_version().split('.')[0]

    current_list = os.listdir(os.getcwd()) 			
    chrome_list = []
    for i in current_list:
        path = os.path.join(os.getcwd(), i) 			
        if os.path.isdir(path): 				
            if 'chromedriver.exe' in os.listdir(path): 		
                chrome_list.append(i) 				

    old_version = list(set(chrome_list)-set([chrome_ver])) 	

    for i in old_version:
        path = os.path.join(os.getcwd(),i) 			
        shutil.rmtree(path) 					

    if not chrome_ver in current_list: 				
        AutoChrome.install(True) 				
    else : pass 					

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
    news_list = []
    now = datetime.now()
    today = now.date().strftime('%Y년 %m월 %d일 %A')
    news_list.append(today+' 경제 뉴스 모음\n\n\n')
    
    # setting url
    url = "https://www.hankyung.com/all-news/"

    url_sub = ['economy', 'finance', 'realestate', 'it']
    
    driver.get(url)
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[1]/div[2]/ul/li[2]/a').click()
    
    print(driver.window_handles)
    time.sleep(5)

    # close popup
    main = driver.window_handles
    for handle in main:
        if handle != main[0]:
            driver.switch_to.window(handle)
            driver.close()
    
    print("DEBUG Message: All popup closed.\n")
    driver.switch_to.window(main[0])
    
    for i in url_sub:
        url_temp = url + i
        driver.get(url_temp)
        news_list.append('\n\n---------------- '+i+' ------------------')
        subject = driver.find_element(By.CLASS_NAME, 'day_article')
        subject_lis = subject.find_elements(By.TAG_NAME, 'li')
        
        for li in subject_lis:
            aTag = li.find_element(By.TAG_NAME,'a')
            href = aTag.get_attribute('href')
            news_list.append(aTag.text)
            news_list.append(href)
            # print("기사제목: " + aTag.text)
            # print("기사링크: " + href)

    time.sleep(1)
    news_list.append('\n\n---------------- 뉴스 끝 ------------------')

    # get US stock data 
    time.sleep(1)
    news_list.append('\n\n------------- 미 증시 map ------------------')
    pict = "https://finviz.com/map.ashx"
    news_list.append(pict)

    driver.close()
    print("DEBUG MESSAGE: page closed.")
    news_list.append('\n\n------------- 미 증시 map 끝 ------------------')

    for msg in news_list:
        news_msg = news_msg+'\n'+msg
    print(news_msg)

    return news_msg

# auto update chrome driver
chromedriver_update()

chrome_ver = AutoChrome.get_chrome_version().split('.')[0]
path = os.path.join(os.getcwd(),chrome_ver)
path = os.path.join(path,'chromedriver.exe')
print(path)

# -----------definition and basic setting-----------
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(path, options=options)

# setting locale to use Korean
locale.setlocale(locale.LC_ALL, '')

# setting slack token
MYTOKEN = ""
    
# create variable
NEWS = ''

# send slack bot all messages
post_message(MYTOKEN,'#general',get_articles(NEWS))
print("DEBUG MESSAGE: send slack message:",NEWS)

print("DEBUG MESSAGE: program closed.")
os._exit(1)
