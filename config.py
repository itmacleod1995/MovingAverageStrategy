import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("key")
secret = os.getenv("API_SECRET")
BASE_URL = "https://paper-api.alpaca.markets"