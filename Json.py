# Создание jsonА
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import lxml

def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    }

    url = "https://eec.eaeunion.org/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="news-pane-item")

    news_dict = {}  # словарь для наших статей
    for article in articles_cards:
        article_title = article.find("span", class_="news-pane-item__h").text.strip()
        article_desc = article.find("span", class_="news-pane-item__text").text.strip()
        article_url = f'https://eec.eaeunion.org{article.find("a").get("href")}'
        article_date_timestamp = article.find('span', class_='news-pane-item__date').get_text(strip=True)

        article_id = article_url.split("/")[-2] # убедиться, что эта переменная разная на каждом этапе цикла. Он перезаписывает одну новость другой - ПОДСКАЗКА
        article_id = article_id

        # print('article id is ', article_id) ПОДСКАЗКА
        news_dict[article_id] = {
            "article_date_timestamp": article_date_timestamp,
            "article_title": article_title,
            "article_url": article_url,
            "article_desc": article_desc
        }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

def main():
    get_first_news()
    #print(check_news_update())

if __name__ == '__main__':
    main()










