import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# создаем функцию и словарь заголовков, помещаем в него user agent. Сохраняем все в словарь
def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    }

    url = "https://eec.eaeunion.org/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")

# далее идет сбор новостей
    articles_cards = soup.find_all("div", class_="news-pane-item")

# забираем заголовок статьи, дату, краткое описание и ссылку
    news_dict = {} # словарь для наших статей
    for article in articles_cards:
        article_title = article.find("span", class_="news-pane-item__h").text.strip()
        article_desc = article.find("span", class_="news-pane-item__text").text.strip()
        article_url = f'https://eec.eaeunion.org{article.find("a").get("href")}'
        article_date_timestamp = article.find('span', class_='news-pane-item__date').get_text(strip=True)

        # получим id каждой новости. Сделаем это на основе уникального значения каждого url. Потом используем id в качестве ключа в словаре
        article_id = article_url.split("/")[-2]
        article_id = article_id

        # проверка работы сбора информации:
        # print(f"{article_title} | {article_url} | {article_desc} | {article_date_timestamp}")

    #get_first_news()

# ключи - id статей, а значения - словари с собранными данными
        news_dict[article_id] = {
            "article_date_timestamp": article_date_timestamp,
            "article_title": article_title,
            "article_url": article_url,
            "article_desc": article_desc
        }
# сохраняем результат работы в json-файл
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

# функция проверки поступления новых статей
def check_news_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    }

    url = "https://eec.eaeunion.org/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="news-pane")

    fresh_news = {}
    for article in articles_cards:
        article_url = f'https://eec.eaeunion.org{article.find("a").get("href")}'
        article_id = article_url.split("/")[-1]
        article_id = article_id
        
        # если id есть в подгружаемом словаре, то continue. Если совпадений не найдено, то надо собрать данные на новость как прежде
        if article_id in news_dict:
            continue
        else:
            article_title = article.find("span", class_="news-pane-item__h").text.strip()
            article_desc = article.find("span", class_="news-pane-item__text").text.strip()
            article_date_timestamp = article.find('span', class_='news-pane-item__date').get_text(strip=True)

            news_dict[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

            fresh_news[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news

# создаем функцию по сбору статей
def main():
    get_first_news()
    #print(check_news_update())


if __name__ == '__main__':
    main()
