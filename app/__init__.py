from flask import Flask

from app.config import SECRET_KEY


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.secret_key = SECRET_KEY

    from app.routes.web import web

    app.register_blueprint(web)
    return app