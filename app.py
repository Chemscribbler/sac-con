from pack_maker_drafter import app, db
from pack_maker_drafter.models import User, Card, Pack, Draft, Deck
from pack_maker_drafter import utils


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Card": Card,
        "Pack": Pack,
        "Draft": Draft,
        "Deck": Deck,
        "utils": utils,
    }
