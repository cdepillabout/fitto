from flask import Flask
from flaskext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)
from . import views, settings


def init_fitto():
    app.config.from_object('fitto.settings')
    db.init_app(app)

def run_fitto(debug=None, host='localhost'):
    init_fitto()

    if debug is not None:
        app.run(debug=debug, host=host)
    else:
        app.run(host=host)

