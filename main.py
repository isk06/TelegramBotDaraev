import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Create a function and a dictionary of headers, put the user agent in it. Save everything to a dictionary
def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    }

    url = "https://eec.eaeunion.org/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")

# Next comes news gathering
    articles_cards = soup.find_all("div", class_="news-pane-item")

# We take the title of the article, date, short description and link
    news_dict = {} # Dictionary for our articles
    for article in articles_cards:
        article_title = article.find("span", class_="news-pane-item__h").text.strip()
        article_desc = article.find("span", class_="news-pane-item__text").text.strip()
        article_url = f'https://eec.eaeunion.org{article.find("a").get("href")}'
        article_date_timestamp = article.find('span', class_='news-pane-item__date').get_text(strip=True)

        # Get the id of each news. Let's do this based on the unique value of each url. Then we use id as a key in the dictionary
        article_id = article_url.split("/")[-2]
        article_id = article_id

        # Checking the work of information collecting:
        # print(f"{article_title} | {article_url} | {article_desc} | {article_date_timestamp}")

    #get_first_news()

# Keys - id articles, and values - dictionaries with collected data
        news_dict[article_id] = {
            "article_date_timestamp": article_date_timestamp,
            "article_title": article_title,
            "article_url": article_url,
            "article_desc": article_desc
        }
# Save the result of the work in a json file
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

# function that checks new articles
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
        
        # If id is in the loaded dictionary, then continue. If no matches are found, then you need to collect data on the news as before
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

# Create a function for collecting articles
def main():
    get_first_news()
    #print(check_news_update())


if __name__ == '__main__':
    main()
