from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config['TEMPLATES_AUTO_RELOAD'] = True

    from .routes.general import general_routes
    from .routes.tictactoe import tictactoe_routes

    app.register_blueprint(general_routes)
    app.register_blueprint(tictactoe_routes)

    return app
