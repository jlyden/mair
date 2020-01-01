import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

#    from . import db
#    db.init_app(app)

    db = SQLAlchemy(app)
    migrate - Migrate(app, db)

    from . import game
    app.register_blueprint(game.bp)
    
    # sanity check
    @app.route('/')
    def sanity_check():
        return 'This is a sanity check.'
    
    return app