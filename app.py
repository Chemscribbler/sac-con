from source import app, db
from source.models import User, Card, Pack, Draft, Deck
from source import utils


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
