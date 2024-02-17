# env.py

import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CYANBOT_DATABASE_URL = os.getenv("CYANBOT_DATABASE_URL")
CYANBOT_DATABASE_NAME = os.getenv("CYANBOT_DATABASE_NAME")
CYANBOT_MESSAGE_COUNT = os.getenv("CYANBOT_MESSAGE_COUNT","60")