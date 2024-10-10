import os

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    Swagger(app, template_file=os.path.join(os.path.dirname(__file__), 'docs', 'api_docs.yaml'))

    with app.app_context():
        from . import routes
        routes.register_routes(app)
        db.create_all()

    return app
