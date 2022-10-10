# TelegramBotDaraev
1. The topic of work is a telegram bot that parses news from the site https://eec.eaeunion.org/news/

2. Libraries used: requests, BeautifulSoup, aiogram

3. Work algorithm:

- main.py:
1. requesting data from the site via requests
2. processing the received data by BeautifulSoup
3. create a dictionary and put the collected articles there. Keys - articles id (unique value of each link)
4. save the dictionary in json

- tg_bot_MY.py:
5. transfer information to the telegram bot. Menu buttons have been created
