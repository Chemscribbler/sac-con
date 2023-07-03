from source import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

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


class Pack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cards = db.relationship("Card", secondary=pack_card, backref="pack")


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nrdb_id = db.Column(db.Integer, index=True)
    card_name = db.Column(db.String(128), index=True)
    faction = db.Column(db.String(64), index=True)
    card_type = db.Column(db.String(64), index=True)
    agenda_points = db.Column(db.Integer, index=True)
    rarity = db.Column(db.String(64), index=True)
    cardpool = db.Column(db.String(64), index=True)

    def __repr__(self):
        return f"<Card {self.card_name}>"


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


class Draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    draft_id = db.Column(db.Integer, db.ForeignKey("draft.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="decks")
    deck_name = db.Column(db.String(128), index=True)
    cards = db.relationship("Card", secondary=deck_card, backref="deck")
