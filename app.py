import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
import models

from resources.user import bp as UserBlueprint
from resources.transaction import bp as TransactionBlueprint

from blocklist import BLOCKLIST


def create_app(db_url=None):
    app = Flask(__name__, url_prefix='/moneyapp-api')

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Moneyapp REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["APPLICATION_ROOT"] = '/moneyapp-api'
    db.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "AJA$JP@i7btg9szQK?&m8nznJde5N$X8ykxc64cr"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message": "The token has been revoked.",
                "error": "token_revoked"
            }),
            401
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message": "The token has expired.",
                "error": "token_expired"
            }),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "message": "Signature verification failed.",
                "error": "invalid_token"
            }),
            401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({
                "message": "Request does not contain an access token.",
                "error": "authorization_required"
            }),
            401
        )

    with app.app_context():
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(TransactionBlueprint)

    return app
