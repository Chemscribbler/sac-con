from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Deck(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int


class DeckCreate(Deck):
    pass


class CardBase(BaseModel):
    nrdb_id: int


class Card(CardBase):
    id: int

    class Config:
        orm_mode = True


class Pack(BaseModel):
    id: int
    draft_id: int


class DeckCard(BaseModel):
    deck_id: int
    card_id: int
    quantity: int = 1

    class Config:
        orm_mode = True


class PackCard(BaseModel):
    pack_id: int
    card_id: int

    class Config:
        orm_mode = True


class Draft(BaseModel):
    id: int
    owner_id: int
    name: str

    class Config:
        orm_mode = True


class DraftUser(BaseModel):
    draft_id: int
    user_id: int

    class Config:
        orm_mode = True
