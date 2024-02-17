from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import TypeVar, Generic

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: ModelType):
        self.model = model

    def get(self, db: Session, id: int) -> ModelType:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: BaseModel) -> ModelType:
        for field in obj_in.model_dump(exclude_unset=True):
            setattr(db_obj, field, getattr(obj_in, field))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int) -> None:
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()


from sql_drafter.schemas import (
    User,
    UserCreate,
    Deck,
    DeckCreate,
    DeckCard,
    Draft,
    DraftUser,
)


class UserCRUD(BaseCRUD[User, UserCreate]):
    pass


class DeckCRUD(BaseCRUD[Deck, DeckCreate]):
    def add_card_to_deck(self, db: Session, deck_id: int, card_id: int) -> None:
        deck = self.get(db, deck_id)
        if deck:
            deck_card = DeckCard(deck_id=deck_id, card_id=card_id)
            db.add(deck_card)
            db.commit()

    def remove_card_from_deck(self, db: Session, deck_id: int, card_id: int) -> None:
        db.query(DeckCard).filter_by(deck_id=deck_id, card_id=card_id).delete()
        db.commit()


class DraftUserCRUD(BaseCRUD):
    def add_user_to_draft(self, db: Session, draft_id: int, user_id: int) -> None:
        draft = db.query(Draft).filter(Draft.id == draft_id).first()
        user = db.query(User).filter(User.id == user_id).first()
        if draft and user:
            draft_user = DraftUser(draft_id=draft_id, user_id=user_id)
            db.add(draft_user)
