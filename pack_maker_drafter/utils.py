import requests
import re
import pandas as pd
from pack_maker_drafter import db

# from source.models import Card
from tqdm import tqdm


def replace_special_chars(string):
    # Replace spaces and special characters with a single underscore
    pattern = r"\s+|[^a-zA-Z0-9_]+"
    result = re.sub(pattern, "_", string)
    result = result.strip("_")
    return result


def get_card(card_name: str):
    clean_cardname = replace_special_chars(card_name).lower()
    url = f"https://api-preview.netrunnerdb.com/api/v3/public/cards/{clean_cardname}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {card_name}: {response.status_code}")
