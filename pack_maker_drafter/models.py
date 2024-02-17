from source import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from source.pack_creation import make_corp_pack
from source.utils import get_card
import random

draft_user = db.Table(
    "draft_user",
    db.Column("draft_id", db.Integer, db.ForeignKey("draft.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)

deck_card = db.Table(
    "deck_card",
    db.Column("deck_id", db.Integer, db.ForeignKey("deck.id"), primary_key=True),
    db.Column("card_id", db.Integer, db.ForeignKey("card.id"), primary_key=True),
)

pack_card = db.Table(
    "pack_card",
    db.Column("pack_id", db.Integer, db.ForeignKey("pack.id"), primary_key=True),
    db.Column("card_id", db.Integer, db.ForeignKey("card.id"), primary_key=True),
)


class CardPool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cardpool_name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return f"<CardPool {self.cardpool_name}>"

    def add_pool_to_db(self, cardpool_df):
        for row in cardpool_df.iterrows():
            card = Card(
                card_name=row[1]["Card"], rarity=row[1]["Rarity"], cardpool=self
            )
            card.fill_data()


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nrdb_id = db.Column(db.Integer, index=True)
    card_name = db.Column(db.String(128), index=True)
    faction = db.Column(db.String(64), index=True)
    card_type = db.Column(db.String(64), index=True)
    agenda_points = db.Column(db.Integer, index=True)
    rarity = db.Column(db.String(64), index=True)
    cardpool_id = db.Column(
        db.Integer, db.ForeignKey("card_pool.id", name="fk_cardpool_id")
    )
    cardpool = db.relationship("CardPool", backref="cards")
    picked = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Card {self.card_name}>"

    def fill_data(self):
        data = get_card(self.card_name)["data"]["attributes"]
        self.faction = data["faction_id"]
        self.card_type = data["card_type_id"]
        if self.card_type == "agenda":
            self.agenda_points = data["agenda_points"]
        self.nrdb_id = data["latest_printing_id"]
        db.session.add(self)
        db.session.commit()


class Pack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cards = db.relationship("Card", secondary=pack_card, backref="pack")
    draft_id = db.Column(db.Integer, db.ForeignKey("draft.id", name="fk_draft_id"))
    draft = db.relationship("Draft", backref="packs")
    active_user_id = db.Column(db.Integer, db.ForeignKey("user.id", name="fk_user_id"))
    active_user = db.relationship("User", backref="packs")
    round = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Pack {self.id}>"

    def valid_cards(self):
        return [card for card in self.cards if card.picked is False]  # type: ignore

    def pick_card(self, card: Card):
        if card not in self.valid_cards():
            raise ValueError("Card not in pack")
        card.picked = True
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), index=True, unique=True)
    drafts = db.relationship("Draft", secondary=draft_user, backref="users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_active_pack(self, draft_id: int = None):
        # Get the pack with the lowest round number and highest number of cards
        # From the packs that are assigned to the player
        packs = self.packs
        if len(packs) == 0:
            return None
        packs = [pack for pack in packs if pack.draft.id == draft_id]
        if packs[0] is None:
            return None
        min_round = min([pack.round for pack in packs])
        packs = [pack for pack in packs if pack.round == min_round]
        return max(packs, key=lambda x: len(x.cards))

    def get_draft_deck(self, draft_id: int):
        return [deck for deck in self.decks if deck.draft.id == draft_id][0]

    # TODO: write a method to pick a card and pass to the next player
    # Need to know which draft it's in, which pack it's picking from, and the pick, and the deck it's going to
    def pick_card(self, card: Card):
        pack = self.get_active_pack()
        pack.pick_card(card)
        draft = pack.draft
        draft.pass_pack_to_next_player(pack, self)
        # get the deck that the user is currently drafting
        # add the card to the deck
        deck = self.get_draft_deck(draft)
        deck.cards.append(card)
        db.session.add(deck)
        db.session.commit()


class Draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.relationship("User", secondary=draft_user, overlaps="drafts,users")
    cardpool_id = db.Column(
        db.Integer, db.ForeignKey("card_pool.id", name="fk_cardpool_id")
    )
    cardpool = db.relationship("CardPool", backref="drafts")
    current_round = db.Column(db.Integer, default=0)
    total_rounds = db.Column(db.Integer, default=5)
    player_order = db.Column(db.JSON, default=[])

    def start_draft(self, players: list[User]):
        if len(players) != 8:
            raise ValueError("Draft must have 8 players")
        if self.current_round != 0:
            raise ValueError("Draft has already started")
        self.current_round = 1

        for player in players:
            pack = self.make_pack()
            pack.active_user = player
            db.session.add(pack)
            db.session(
                Deck(draft=self, user=player, deck_name=f"{player.username}'s Deck")
            )
        db.session.commit()

    def pass_pack_to_next_player(self, pack: Pack, user: User):
        if pack not in self.packs:
            raise ValueError("Pack not in draft")
        if user not in self.player_order:  # type: ignore
            raise ValueError("User not in draft")
        if len(pack.valid_cards()) == 0:
            raise ValueError("Pack is empty")
        current_index = self.player_order.index(user)
        next_index = (current_index + 1) % len(self.player_order)
        next_player = self.player_order[next_index]

        # Update the pack's draft relationship
        pack.active_user = next_player
        db.session.add(pack)
        db.session.commit()

    def make_pack(self):
        pack = make_corp_pack()
        card_ids = [
            Card.query.filter_by(card_name=card, cardpool=self.cardpool).first()
            for card in pack["Card"].values
        ]
        pack = Pack(cards=card_ids, draft=self, round=self.current_round)
        db.session.add(pack)
        db.session.commit()
        return pack


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    draft_id = db.Column(db.Integer, db.ForeignKey("draft.id"))
    draft = db.relationship("Draft", backref="decks")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="decks")
    deck_name = db.Column(db.String(128), index=True)
    cards = db.relationship("Card", secondary=deck_card, backref="deck")
