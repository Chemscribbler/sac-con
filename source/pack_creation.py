import pandas as pd
from source.models import Card, Pack
from source import db

CARDPOOL_PATH = (
    "/Users/jeff/Documents/Netrunner/sac-con/corp_spreadsheets/CorpPool_Draft1.csv"
)
CARDPOOL = pd.read_csv(CARDPOOL_PATH)


def upgrade_rarities(draft_pack: pd.DataFrame, rarity: str, cardpool: pd.DataFrame):
    """
    Upgrade the rarities of the cards in the draft pack
    If the card is an agenda, only upgrade to other agendas
    Otherwise upgrade from any other type to any other type (excluding agendas)
    """
    if rarity not in ["R", "N"]:
        raise ValueError("Rarity must be R or N")
    for row in draft_pack.iterrows():
        if row[1]["Type"] == "Agenda":
            rare_pool = cardpool[
                (cardpool["Rarity"] == rarity) & (cardpool["Type"] == row[1]["Type"])
            ].copy()
        else:
            rare_pool = cardpool[
                (cardpool["Rarity"] == rarity) & (cardpool["Type"] != "Agenda")
            ].copy()
        rare_card = rare_pool.sample(1)
        row[1]["Card"] = rare_card["Card"].values[0]
        row[1]["Rarity"] = rare_card["Rarity"].values[0]
        row[1]["Faction"] = rare_card["Faction"].values[0]
        row[1]["Type"] = rare_card["Type"].values[0]
        row[1]["Function"] = rare_card["Function"].values[0]
    return draft_pack


def get_commons_baseline(cardpool: pd.DataFrame):
    """
    Get the number of commons in the cardpool

    TODO: Need to put checker for duplicate commons in the same pack
    """
    df = cardpool[cardpool["Rarity"] == "C"].copy()
    agendas = df[df["Type"] == "Agenda"].sample(2)
    ice = df[df["Type"] == "Ice"].sample(3)
    operations = df[df["Type"] == "Operation"].sample(2)
    assets = df[df["Type"] == "Asset"].sample(2)
    flex = df.sample(4)
    df = pd.concat([agendas, ice, operations, assets, flex])
    return df


def upgrade_baseline(commons_dataframe: pd.DataFrame, cardpool: pd.DataFrame):
    pack_rares = commons_dataframe.iloc[:1, :]
    pack_uncommons = commons_dataframe.iloc[1:, :]
    pack_rares = upgrade_rarities(pack_rares, "R", cardpool)
    pack_uncommons = upgrade_rarities(pack_uncommons, "N", cardpool)
    return commons_dataframe


def faction_checker(pack: pd.DataFrame, faction_list):
    """
    Check to see if the pack has all 5 factions
    """
    for faction in faction_list:
        if pack[pack["Faction"] == faction].shape[0] == 0:
            return faction
    return None


def faction_replace(pack: pd.DataFrame, faction: str, cardpool: pd.DataFrame):
    """
    Replace a card in the pack with a card from the cardpool
    """
    to_be_replaced_card = pack.sample(1)

    card = cardpool[
        (cardpool["Faction"] == faction)
        & (cardpool["Rarity"] == to_be_replaced_card["Rarity"].values[0])
    ].sample(1)
    cols = list(pack.columns)
    pack.loc[pack["Card"] == to_be_replaced_card["Card"].values[0], cols] = card[
        cols
    ].values[0]
    return pack


def faction_swap(
    pack: pd.DataFrame,
    cardpool: pd.DataFrame,
    faction_list=["haas-bioroid", "jinteki", "nbn", "weyland", "Neutral"],
):
    while True:
        deduplicator(pack, cardpool)
        missing_faction = faction_checker(pack, faction_list)
        if missing_faction is None:
            return pack
        pack = faction_replace(pack, missing_faction, cardpool)


def deduplicator(pack: pd.DataFrame, cardpool: pd.DataFrame):
    # Find duplicate cards in the pack and replace them with cards of the same rarity
    duplicated_cards = pack[pack.duplicated(subset=["Card"])]
    unique_cards = pack[~pack.duplicated(subset=["Card"])]
    cols = list(pack.columns)
    for row in duplicated_cards.iterrows():
        card = cardpool[
            (cardpool["Rarity"] == row[1]["Rarity"])
            & (cardpool["Type"] == row[1]["Type"])
        ].sample(1)
        for col in cols:
            row[1][col] = card[col].values[0]
    new_pack = pd.concat([unique_cards, duplicated_cards])
    if new_pack.duplicated(subset=["Card"]).sum() > 0:
        return deduplicator(new_pack, cardpool)
    return new_pack


def make_corp_pack(cardpool: pd.DataFrame):
    """
    13 card packs - with 5 rounds of drafting gets you 65 cards

    Guranteed:
    - 2 Agendas
    - 3 Ice
    - 2 Operations
    - 2 Assets
    - 4 Flex cards

    Rarity Breadown:
    1 Rares
    5 Uncommons
    7 Commons

    From the common pool fill out the guranteed card types
    Randomly upgrade 2 rares and 4 uncommons
    Then check for all factions present - swapping out as needed for the same type
    optional - check for ice duplication
    """
    pack = get_commons_baseline(cardpool).reset_index(drop=True)
    pack_upgrades = pack.sample(6)
    pack_commons = pack[~pack.isin(pack_upgrades)].dropna()
    pack_upgrades = upgrade_baseline(pack_upgrades, cardpool)
    pack = pd.concat([pack_upgrades, pack_commons])
    pack = faction_swap(pack, cardpool)
    return pack


def add_pack_to_db(pack: pd.DataFrame):
    card_ids = [
        Card.query.filter_by(card_name=card).first() for card in pack["Card"].values
    ]
    pack = Pack(cards=card_ids)
    db.session.add(pack)
    db.session.commit()
