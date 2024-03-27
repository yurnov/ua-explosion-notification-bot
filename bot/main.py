#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import os
from dotenv import load_dotenv
import time
from datetime import datetime
import pytz

"""
This is a simple telegram bot that every 30 secound get API http://alerts.net.ua/explosives_statuses_v2.json and send
message to telegram chat

Example of JSON answer:

{"version":2,"states":{"Сумська область":"2024-03-25T07:36:13+00:00",
                        "Харківська область":"2024-03-23T20:21:31+00:00",
                        "Донецька область":"2024-03-24T11:11:20+00:00",
                        "Херсонська область":"2024-03-24T22:40:52+00:00",
                        "Миколаївська область":"2024-03-23T20:53:41+00:00",
                        "Одеська область":"2024-03-24T21:53:05+00:00",
                        "Київська область":"2024-03-21T02:23:32+00:00",
                        "Житомирська область":"2024-03-21T02:28:59+00:00",
                        "м. Київ":"2024-03-25T08:30:22+00:00",
                        "Дніпропетровська область":"2024-03-24T00:47:42+00:00",
                        "Львівська область":"2024-03-24T07:35:19+00:00",
                        "Волинська область":"2024-03-24T03:21:54+00:00"},
"info":{"last_update":"2024-03-25T09:33:52Z","last_id":126511}}

Bot send message only if date of last_id is changed and send message with all states that have changed date. Bot have
predefined list of regions that have changed date and send message only if this region is in this list.

Bot don't use telegram-python lib, just pure API call to telegram API.

"""

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = os.getenv("URL")
REGION_LIST = os.getenv("REGION_LIST").split(",") if os.getenv("REGION_LIST") else None
TIMEZONE = os.getenv("TIMEZONE")
SLIENT = os.getenv("SLIENT")

"""
Full list of regions:

["Сумська область", "Харківська область", "Донецька область", "Херсонська область",
"Миколаївська область", "Одеська область", "Київська область", "Житомирська область",
"м. Київ", "Автономна Республіка Крим", "Запорізька область", "Дніпропетровська область",
"Хмельницька область", "Полтавська область", "Львівська область", "Волинська область"]

"""

# Mapping of regions to grammatical case
regions_gram_case = {
    "Автономна Республіка Крим": "Автономній Республіці Крим",
    "Волинська область": "Волинській області",
    "Дніпропетровська область": "Дніпропетровській області",
    "Донецька область": "Донецькій області",
    "Житомирська область": "Житомирській області",
    "Запорізька область": "Запорізькій області",
    "Київська область": "Київській області",
    "Львівська область": "Львівській області",
    "м. Київ": "м. Києві",
    "Миколаївська область": "Миколаївській області",
    "Одеська область": "Одеській області",
    "Полтавська область": "Полтавській області",
    "Сумська область": "Сумській області",
    "Харківська область": "Харківській області",
    "Херсонська область": "Херсонській області",
    "Хмельницька область": "Хмельницькій області",
}

MESSAGE = "💥За даними ЗМІ, зафіксовані вибухи у "

if not TOKEN or not CHAT_ID:
    logger.error("TOKEN or CHAT_ID is not defined in .env file or environment variables")
    exit()

if not URL:
    logger.warning(
        "URL is not defined in .env file, using a default URL http://alerts.net.ua/explosives_statuses_v2.json"
    )
    URL = "http://alerts.net.ua/explosives_statuses_v2.json"


if not REGION_LIST:
    logger.warning("REGION_LIST is not defined in .env file, using a default list of regions")
    # List of regions that bot will send message if date is changed
    REGION_LIST = [
        "Сумська область",
        "Харківська область",
        "Одеська область",
        "Київська область",
        "Житомирська область",
        "м. Київ",
        "Запорізька область",
        "Дніпропетровська область",
        "Хмельницька область",
        "Львівська область",
        "Волинська область",
    ]
else:
    REGION_LIST = [region.strip('"') for region in REGION_LIST]

if not TIMEZONE:
    logger.warning("TIMEZONE is not defined in .env file, using a default timezone Europe/Kiev")
    TIMEZONE = "Europe/Kiev"

if not SLIENT or SLIENT.lower not in lower["true", "false"]:
    logger.warning("SLIENT is not defined in .env file, or not a boolean, using a default value false")
    SLIENT = "false"
else:
    SLIENT = SLIENT.lower()

logger.info(f"Bot started with CHAT_ID: {CHAT_ID} and SLIENT: {SLIENT}")
logger.info(f"Following regions will be monitored: {REGION_LIST}")


def get_data():
    try:
        response = requests.get(URL, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while getting data: {e}")
        return None
    return response.json()


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&disable_notification={SLIENT}&text={text}"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while sending message: {e}")
        return None
    return response.json()


def main():
    last_data = None

    while True:
        data = get_data()
        if not data:
            time.sleep(30)
            continue

        if last_data is None:
            last_data = data
        else:
            last_id = last_data["info"]["last_id"]
            current_id = data["info"]["last_id"]

            if current_id != last_id:
                states = data["states"]
                message = MESSAGE

                for region, date in states.items():
                    if region in REGION_LIST and date != last_data["states"].get(region):
                        logger.info(f"Explosion in region: {region}, date: {date}")

                        message += f"{regions_gram_case.get(region, region)} о {datetime\
                                        .strptime(date,'%Y-%m-%dT%H:%M:%S+00:00').replace(tzinfo=pytz.utc)\
                                        .astimezone(tz=pytz.timezone(TIMEZONE)).strftime('%H:%M')}\n"

                if message != MESSAGE:
                    message += "\nЙобанарусня!"
                    send_message(message)

                last_data = data

        time.sleep(30)


if __name__ == "__main__":
    main()
