import feedparser
import telebot
import schedule
import time
import psycopg2
import logging
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(filename='bot.log', level=logging.ERROR)

# Import configuration
import db_config
from config import channel_id1, bot_token1, channel_id2, bot_token2
from rss_links import rss_feeds_wide1, rss_feeds_wide2, rss_feeds_techonomy1, rss_feeds_techonomy2

bot1 = telebot.TeleBot(bot_token1)
bot2 = telebot.TeleBot(bot_token2)

# Connect to the database
conn = psycopg2.connect(f"host={db_config.host} dbname={db_config.dbname} user={db_config.user} password={db_config.password}")
cursor = conn.cursor()

# Create a table to store the sent links
cursor.execute('''CREATE TABLE IF NOT EXISTS sent_links
                 (link TEXT, timestamp TIMESTAMP DEFAULT now())''')
conn.commit()


def send_new_entries(bot, channel_id, rss_feeds):
    for feed_url in rss_feeds:
        # Fetch the RSS feed
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            logging.error(f"Error parsing feed: {e}")
            continue

        if len(feed['entries']) > 0:
            first_entry = feed['entries'][0]

            # Check if the entry's link has already been sent
            cursor.execute('''SELECT * FROM sent_links WHERE link = %s''', (first_entry['link'],))
            if not cursor.fetchone():
                # Send the title and link of the first entry to the channel
                try:
                    bot.send_message(channel_id, f"<b>{first_entry['title']}</b>"\
                       + "\n\n" + f"<i>{first_entry['description']}</i>" + "\n\n" + first_entry['link'], parse_mode= 'HTML')
                except Exception as e:
                    logging.error(f"Error sending message: {e}")
                    continue

                # Add the entry's link to the list of sent links
                cursor.execute('''INSERT INTO sent_links (link) VALUES (%s)''', (first_entry['link'],))
                conn.commit()
        else:
            logging.error(f"No entries found in the feed {feed_url}")


def send_new_entries_no_description(bot, channel_id, rss_feeds):
    for feed_url in rss_feeds:
        # Fetch the RSS feed
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            logging.error(f"Error parsing feed: {e}")
            continue

        if len(feed['entries']) > 0:
            first_entry = feed['entries'][0]

            # Check if the entry's link has already been sent
            cursor.execute('''SELECT * FROM sent_links WHERE link = %s''', (first_entry['link'],))
            if not cursor.fetchone():
                # Send the title and link of the first entry to the channel
                try:
                    bot.send_message(channel_id, f"<b>{first_entry['title']}</b>"\
                       + "\n\n" + first_entry['link'], parse_mode= 'HTML')
                except Exception as e:
                    logging.error(f"Error sending message: {e}")
                    continue

                # Add the entry's link to the list of sent links
                cursor.execute('''INSERT INTO sent_links (link) VALUES (%s)''', (first_entry['link'],))
                conn.commit()
        else:
            logging.error(f"No entries found in the feed {feed_url}")


def delete_old_entries():
    # Calculate the date 9 days ago
    delete_before = datetime.now() - timedelta(days=9)

    # Delete the entries that are older than 9 days
    cursor.execute('''DELETE FROM sent_links WHERE timestamp < %s''', (delete_before,))
    conn.commit()


# Schedule the task to run every 1 minute
schedule.every(1).minutes.do(send_new_entries, bot1, channel_id1, rss_feeds_wide1)
schedule.every(1).minutes.do(send_new_entries_no_description, bot1, channel_id1, rss_feeds_wide2)
schedule.every(1).minutes.do(send_new_entries, bot2, channel_id2, rss_feeds_techonomy1)
schedule.every(1).minutes.do(send_new_entries_no_description, bot2, channel_id2, rss_feeds_techonomy2)

# Schedule the task to run every 5 days
schedule.every(5).days.do(delete_old_entries)


# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)

