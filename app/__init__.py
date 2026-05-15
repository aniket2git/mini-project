from flask import Flask

from config import Config

from extensions import (
    db,
    login_manager,
    migrate
)

from app.models.models import User


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)

    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"


    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))


    from app.routes.main import main

    from app.routes.auth import auth

    from app.routes.admin import admin

    from app.routes.courses import courses

    app.register_blueprint(main)

    app.register_blueprint(auth)

    app.register_blueprint(admin)

    app.register_blueprint(courses)

    return app