from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def time_cleaner(time):

    if "ساعت پیش" in time:
        time = time.replace("ساعت پیش", "").strip()
        return datetime.now() - timedelta(hours=time)

    elif "دقیقه پیش" in time:
        time = time.replace("دقیقه پیش", "").strip()
        return datetime.now() - timedelta(minutes=time)

    elif "روز پیش" in time:
        time = time.replace("روز پیش", "").strip()
        return datetime.now() - timedelta(days=time)

    elif "ثانیه پیش" in time:
        time = time.replace("ثانیه پیش", "").strip()
        return datetime.now() - timedelta(seconds=time)


def text_cleaner(text):
    if r"\u200c" in text:
        return text.replace(r"\u200c", " ")
    else:
        return text


all_news_list = []

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

df = pd.DataFrame(all_news_list)

df["زمان"] = df["زمان"].apply(view_cleaner)

df.to_excel("news.xlsx", index=False)
