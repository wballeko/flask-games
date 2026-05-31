from flask import Blueprint, render_template, redirect, url_for, request, abort

from domain.tictactoe import TicTacToeGame, TicTacToe
from infrastructure.repositories.tictactoe_repository import TicTacToeRepository

BLUEPRINT_NAME = "tictactoe"

tictactoe_routes = Blueprint(
    BLUEPRINT_NAME,
    __name__,
    url_prefix=f"/{BLUEPRINT_NAME}"
)

repo = TicTacToeRepository()


def get_game_or_404(game_id: int) -> TicTacToeGame:
    game = repo.get_by_id(game_id)
    if not game:
        abort(404)
    return game


@tictactoe_routes.route('/')
def index():
    games = repo.get_all()
    return render_template(
        f"{BLUEPRINT_NAME}/index.html",
        games=games
    )


@tictactoe_routes.route('/<int:game_id>')
def details(game_id):
    game = get_game_or_404(game_id)
    return render_template(f"{BLUEPRINT_NAME}/game.html", game=game)


@tictactoe_routes.route('/create', methods=['POST'])
def create():
    tictactoe = TicTacToe()
    new_game = TicTacToeGame(
        player_1_name=request.form['player_1_name'],
        player_2_name=request.form['player_2_name'],
        tictactoe=tictactoe
    )
    game = repo.save(new_game)
    return redirect(url_for('.details', game_id=game.id))


@tictactoe_routes.route('/<int:game_id>/turn/<int:row>/<int:col>', methods=['POST'])
def turn(game_id, row, col):
    game = get_game_or_404(game_id)
    game.tictactoe.apply_turn(row, col)
    game = repo.save(game)
    return redirect(url_for('.details', game_id=game.id))
