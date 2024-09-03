import logging
from flask import Flask
from flask_wtf import CSRFProtect
from .config import get_config
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from .routes.books import books_bp 
from .routes.members import members_bp
from .routes.transactions import transactions_bp
from .routes.import_books import import_books_bp
from .routes.errors import register_error_handlers

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    csrf.init_app(app)

    # Set up logging
    logging.basicConfig(level=app.config['LOGGING_LEVEL'])

    try:
        client = MongoClient(app.config['MONGO_URI'], server_api=ServerApi('1'))
        app.db = client.luna 
    except Exception as e:
        logging.error("Could not connect to MongoDB: %s", e)
        raise

    # Register blueprints
    app.register_blueprint(books_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(import_books_bp)

    # Register error handlers
    register_error_handlers(app)

    return app