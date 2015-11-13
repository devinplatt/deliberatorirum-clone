# Base of app for shared db stuff if ever necessary.

from flask import Flask
from database import db

def create_app(config_filename = 'cf'):
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config.from_pyfile('config.py', silent=False)
    db.init_app(app)
    # app.register_blueprint(bp)

    return app

app = create_app()
