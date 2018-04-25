# coding=utf8
from flask import Flask
from .models import db, User
from .config import configs
from .handlers import front, user
from flask_migrate import Migrate
from flask_login import LoginManager

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_blueprints(app)
    register_extentions(app)
    return app


def register_blueprints(app):
    app.register_blueprint(front)
    #app.register_blueprint(job)
    #app.register_blueprint(company)
    app.register_blueprint(user)
    

def register_extentions(app):
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'
