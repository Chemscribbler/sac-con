from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)  # This is the database object
migrate = Migrate(app, db)  # This is the migration engine

from pack_maker_drafter.models import User, Card, Draft, Deck, Pack
