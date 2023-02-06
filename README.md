# RSS Bot

This is a Python script that fetches the latest entries from multiple RSS feeds and posts them to Telegram channels using the `pyTelegramBotAPI` library. The sent links are stored in a PostgreSQL database and checked to avoid posting duplicates. Old entries are deleted after 9 days.

## Required Libraries

-   `feedparser`
-   `telebot`
-   `schedule`
-   `psycopg2`
-   `logging`
-   `datetime`

## Configuration

Before running the script, you need to set the following variables in `config.py`:

-   `channel_id1` and `bot_token1`: the ID of the first Telegram channel and the API token of the bot that will post to it.
-   `channel_id2` and `bot_token2`: the ID of the second Telegram channel and the API token of the bot that will post to it.
-   `rss_feeds_wide1`, `rss_feeds_wide2`, `rss_feeds_techonomy1`, and `rss_feeds_techonomy2`: lists of URLs of the RSS feeds you want to fetch.

You also need to set the database configuration in `db_config.py`:

-   `host`, `dbname`, `user`, and `password`: the host name, database name, user name, and password for the PostgreSQL database, respectively.

## Usage

To run the script, execute the following command in your terminal:

```bash
python bot.py
```

The script will run continuously and post the latest entries from the RSS feeds to the Telegram channels every 1 minute. Error messages will be logged to `bot.log`.