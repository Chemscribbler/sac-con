from CubeWork import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Pack(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nrdb_id = db.Column(db.Integer, index=True, unique=True)
    pack_id = db.Column(db.Integer, db.ForeignKey("pack.id"))
    pack = db.relationship("Pack", backref="cards", lazy="dynamic")
    card_name = db.Column(db.String(128), index=True)
    faction = db.Column(db.String(64), index=True)
    card_type = db.Column(db.String(64), index=True)
    agenda_points = db.Column(db.Integer, index=True)
    deck_id = db.Column(db.Integer, db.ForeignKey("deck.id"))
    deck = db.relationship("Deck", backref="picks", lazy="dynamic")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), index=True, unique=True)
    drafts = db.relationship("Draft", backref="user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)


class Draft(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    draft_id = db.Column(db.Integer, db.ForeignKey("draft.id"))
    draft = db.relationship("Draft", backref="decks", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="decks", lazy="dynamic")
    deck_name = db.Column(db.String(128), index=True)
