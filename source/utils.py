import requests
import re
import pandas as pd
from source import db
from source.models import Card
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


def get_cardpool_names():
    """
    Get the names of all the cardpools in the database
    """
    unique_cardpools = Card.query.with_entities(Card.cardpool.distinct()).all()
    return [cardpool[0] for cardpool in unique_cardpools]


def drop_cards_by_cardpool(cardpool_name):
    # Delete cards with the specified cardpool name
    Card.query.filter_by(cardpool=cardpool_name).delete()

    # Commit the changes to the database
    db.session.commit()


def add_pool_to_db(
    cardpool_name: str,
    cardpool_path: str | None = None,
    cardpool_df: pd.DataFrame | None = None,
    overwrite: bool = False,
):
    """
    Add the cardpool to the database
    """
    # Check if cardpool name is already in the database
    if cardpool_name in get_cardpool_names() and not overwrite:
        raise ValueError("Cardpool already exists in the database")

    if cardpool_path is None and cardpool_df is None:
        raise ValueError("Must provide either a path or a dataframe")
    if cardpool_df is None:
        cardpool_df = pd.read_csv(cardpool_path)

    drop_cards_by_cardpool(cardpool_name)
    for row in tqdm(cardpool_df.iterrows()):
        card = Card(
            card_name=row[1]["Card"],
            rarity=row[1]["Rarity"],
            cardpool=cardpool_name,
        )
        fill_data(card)


def fill_data(card: Card):
    try:
        data = get_card(card.card_name)["data"]["attributes"]
        card.faction = data["faction_id"]
        card.card_type = data["card_type_id"]
        if card.card_type == "agenda":
            card.agenda_points = data["agenda_points"]
        card.nrdb_id = data["latest_printing_id"]
        db.session.add(card)
        db.session.commit()
    except Exception as e:
        print(e)
