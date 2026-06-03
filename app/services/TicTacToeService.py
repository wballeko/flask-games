from domain.tictactoe import TicTacToeGame, TicTacToe
from infrastructure.repositories.tictactoe_repository import TicTacToeRepository, TicTacToeGameRecord


class TicTacToeService:

    def __init__(self, repository: TicTacToeRepository):
        self._repository = repository

    def create_game(
            self,
            player_1_name: str,
            player_2_name: str,
    ) -> TicTacToeGameRecord:
        tictactoe = TicTacToe()
        game = TicTacToeGame(
            player_1_name=player_1_name,
            player_2_name=player_2_name,
            tictactoe=tictactoe
        )

        return self._repository.save(game)

    def apply_turn(
            self,
            game_id: int,
            row: int,
            col: int,
    ) -> TicTacToeGameRecord:
        game = self._repository.get_by_id(game_id)

        if game is None:
            raise ValueError(f"Game with id {game_id} does not exist")

        game.apply_turn(row, col)

        return self._repository.save(game)
