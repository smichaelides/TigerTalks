from flask import Flask
from server.api.routes.root import root


def register_routes(app: Flask):

    app.register_blueprint(root)
