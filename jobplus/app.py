# coding=utf8
from flask import Flask
from jobplus.models import db, User
from jobplus.config import configs
from .handlers import front, user, company, job, admin
from flask_migrate import Migrate
from flask_login import LoginManager


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_extentions(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(front)
    app.register_blueprint(job)
    app.register_blueprint(company)
    app.register_blueprint(user)
    app.register_blueprint(admin)


def register_extentions(app):
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'
