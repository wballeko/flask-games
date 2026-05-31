from flask import Blueprint, render_template

general_routes = Blueprint('general', __name__)


@general_routes.route('/')
def index():
    return render_template('index.html')