from sql_drafter.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    decks = relationship("Deck", back_populates="owner")
    drafts = relationship("Draft", secondary="draft_user", back_populates="users")
    drafts_ownded = relationship("Draft", back_populates="owner")


class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="decks")
    cards = relationship("Card", secondary="deck_card", back_populates="decks")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    nrdb_id = Column(Integer, index=True)
    deck = relationship("Deck", secondary="deck_card", back_populates="cards")


class Pack(Base):
    __tablename__ = "packs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cards = relationship("Card", secondary="pack_card", back_populates="packs")
    draft_id = Column(Integer, ForeignKey("drafts.id"))


class Draft(Base):
    __tablename__ = "drafts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    packs = relationship("Pack", back_populates="draft")
    users = relationship("User", secondary="draft_user", back_populates="drafts")
    owner = relationship("User", back_populates="drafts_ownded")


pack_card = Table(
    "pack_card",
    Base.metadata,
    Column("pack_id", Integer, ForeignKey("packs.id")),
    Column("card_id", Integer, ForeignKey("cards.id")),
)

deck_card = Table(
    "deck_card",
    Base.metadata,
    Column("deck_id", Integer, ForeignKey("decks.id")),
    Column("card_id", Integer, ForeignKey("cards.id")),
    Column("quantity", Integer, default=1),
)

draft_user = Table(
    "draft_user",
    Base.metadata,
    Column("draft_id", Integer, ForeignKey("drafts.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)
