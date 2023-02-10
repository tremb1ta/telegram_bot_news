[![Tech News](https://img.shields.io/twitter/url?label=Tech%20News&logo=Telegram&style=social&url=https%3A%2F%2Ft.me%2Ftech_news_tremb1ta)](https://t.me/tech_news_tremb1ta)
[![Economics News](https://img.shields.io/twitter/url?label=Economics%20News&logo=Telegram&style=social&url=https%3A%2F%2Ft.me%2Feconomics_news_tremb1ta)](https://t.me/economics_news_tremb1ta)
[![Worldwide News](https://img.shields.io/twitter/url?label=Worldwide%20News&logo=Telegram&style=social&url=https%3A%2F%2Ft.me%2Fworldwide_news_tremb1ta)](https://t.me/worldwide_news_tremb1ta)
[![Ukraine News](https://img.shields.io/twitter/url?label=Ukraine%20News&logo=Telegram&style=social&url=https%3A%2F%2Ft.me%2Fukraine_news_tremb1ta)](https://t.me/ukraine_news_tremb1ta)


# RSS Bot

A Telegram bot that sends latest news articles from selected RSS feeds to designated Telegram channels. This bot utilizes the `feedparser` library to parse the RSS feeds, `pyTelegramBotAPI` library to interact with Telegram API, `schedule` library to schedule tasks, and `psycopg2` library to store information in a PostgreSQL database. The bot also includes error logging functionality with the `logging` library.

## Requirements

-   Python 3.6 or higher
-   `feedparser`
-   `telebot`
-   `schedule`
-   `psycopg2`
-   `logging`
-   `datetime`
-   A Telegram bot token and access to desired Telegram channels
-   A PostgreSQL database

## Configuration

You will need to configure the following in `db_config.py` file:
```python
host = "<host>"
dbname = "<dbname>"
user = "<user>"
password = "<password>"
```

Also in `config.py` file:
```python
bot_token = "<bot_token>"
channel_id1 = "<channel_id1>"
channel_id2 = "<channel_id2>"
...
```
In `rss_links.py` file:
```python
rss_tech1 = ["<rss_feed_1>", "<rss_feed_2>", ...]
rss_tech2 = ["<rss_feed_1>", "<rss_feed_2>", ...]
...
```

## Usage

To run the script, execute the following command in your terminal:

```bash
python bot.py
```

## Note

-   The bot will only send the first entry of each RSS feed.
-   The bot will keep track of the links of the entries that have already been sent and will not send duplicates.
-   The links of the entries sent more than 9 days ago will be deleted from the database.