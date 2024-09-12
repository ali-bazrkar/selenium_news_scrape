import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

all_news_list = []

# TODO : replace "\u200c" with " " in title

url = "https://www.shahrekhabar.com"

for group in ["اخبار-ورزشی", "اخبار-سیاسی", "اخبار-اقتصادی", "اخبار-جهان"]:
    for i in (1, 4):
        driver = webdriver.Chrome()
        driver.get(f"{url}/{group}?page={i}")
        news_list = driver.find_elements(By.CSS_SELECTOR, '.col-sm-12 ul.news-list-items li')

        for news in news_list:
            my_list = news.text.split("\n")

            # دریافت لینک منحصر به فرد هر خبر
            link = news.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
            my_list.append(link)

            news_dict = {
                "عنوان": my_list[0],
                "منبع": my_list[1],
                "گروه": group,
                "زمان": my_list[2],
                "لینک": my_list[3]
            }
            all_news_list.append(news_dict)

driver.quit()
