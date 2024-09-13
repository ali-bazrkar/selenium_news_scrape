from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
from functions import *

all_news_list = []

url = "https://www.shahrekhabar.com"

for group in ["اخبار-ورزشی", "اخبار-سیاسی", "اخبار-اقتصادی", "اخبار-جهان", "اخبار-پزشکی-سلامت"]:
    for i in range(1, 4):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(f"{url}/{group}?page={i}")
        news_list = driver.find_elements(By.CSS_SELECTOR, "ul.news-list-items li")

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

df["زمان"] = df["زمان"].apply(time_cleaner)
df["عنوان"] = df["عنوان"].apply(title_cleaner)
df["لینک"] = df["لینک"].apply(lambda item: np.NaN if url not in item else item)
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

df.to_excel("news.xlsx", index=False)
df.to_csv("news.csv", index=False)
