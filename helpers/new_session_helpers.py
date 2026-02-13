import requests
import os
import time

from dotenv import load_dotenv


def get_actual_base_url():
    return f"{os.getenv('BASE_URL')}:8000/v2"
