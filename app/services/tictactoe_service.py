from domain.tictactoe import TicTacToeComputerPlayer, TicTacToeGame, TicTacToe, TicTacToeState
from infrastructure.repositories.tictactoe_repository import (
    TicTacToeRepository,
    TicTacToeGameRecord,
)


class TicTacToeService:

    def __init__(self, repository: TicTacToeRepository):
        self._repository = repository

    def create_game(
        self,
        player_1_name: str,
        player_2_name: str,
        vs_com: bool
    ) -> TicTacToeGameRecord:
        tictactoe = TicTacToe()
        game = TicTacToeGame(
            player_1_name=player_1_name,
            player_2_name=player_2_name,
            tictactoe=tictactoe,
            vs_com=vs_com
        )

        return self._repository.save(game)

    def _apply_computer_turn(self, tictactoe: TicTacToeGame):
        computer = TicTacToeComputerPlayer()
        col, row = computer.choose_move(tictactoe.tictactoe)
        is_valid = tictactoe.apply_turn(col, row)
        while not is_valid:
            col, row = computer.choose_move(tictactoe.tictactoe)
            is_valid = tictactoe.apply_turn(col, row)

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
        
        if game.tictactoe.state == TicTacToeState.IN_PROGRESS and game.vs_com:
            self._apply_computer_turn(game)

        return self._repository.save(game)
