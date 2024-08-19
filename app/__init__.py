import logging
from flask import Flask
from .config import get_config
from pymongo import MongoClient

from .routes.books import books_bp
from .routes.members import members_bp
from .routes.transactions import transactions_bp
from .routes.errors import register_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    # Set up logging
    logging.basicConfig(level=app.config['LOGGING_LEVEL'])

    try:
        client = MongoClient(app.config['MONGO_URI'])
        app.db = client.luna 
    except Exception as e:
        logging.error("Could not connect to MongoDB: %s", e)
        raise

    # Register blueprints
    app.register_blueprint(books_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(transactions_bp)

    # Register error handlers
    register_error_handlers(app)

    return app