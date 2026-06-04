from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Optional


class TicTacToeFieldType(Enum):
    CROSS = "cross"
    NAUGHT = "naught"
    EMPTY = "empty"


class TicTacToeState(Enum):
    IN_PROGRESS = "in_progress"
    CROSS_WON = "cross_won"
    NAUGHT_WON = "naught_won"
    DRAW = "draw"


@dataclass
class TicTacToe:
    fields: list[list[TicTacToeFieldType]] = field(
        default_factory=lambda: [
            [TicTacToeFieldType.EMPTY for _ in range(3)] for _ in range(3)
        ]
    )

    @property
    def available_fields(self) -> list[tuple[int, int]]:
        return [
            (row, col)
            for row in range(3)
            for col in range(3)
            if self.fields[row][col] == TicTacToeFieldType.EMPTY
        ]

    @property
    def current_turn(self) -> TicTacToeFieldType:
        if self.state != TicTacToeState.IN_PROGRESS:
            return TicTacToeFieldType.EMPTY

        crosses = sum(
            field == TicTacToeFieldType.CROSS for row in self.fields for field in row
        )

        naughts = sum(
            field == TicTacToeFieldType.NAUGHT for row in self.fields for field in row
        )

        return (
            TicTacToeFieldType.NAUGHT if crosses > naughts else TicTacToeFieldType.CROSS
        )

    def turn_is_valid(self, row: int, col: int) -> bool:
        if not (0 <= row < len(self.fields)):
            return False

        if not (0 <= col < len(self.fields[row])):
            return False

        if self.current_turn == TicTacToeFieldType.EMPTY:
            return False

        return self.fields[row][col] == TicTacToeFieldType.EMPTY

    def apply_turn(self, row: int, col: int):
        if self.turn_is_valid(row, col):
            self.fields[row][col] = self.current_turn

    @property
    def state(self) -> TicTacToeState:
        lines = []

        # Rows
        lines.extend(self.fields)

        # Columns
        for col in range(3):
            lines.append(
                [
                    self.fields[0][col],
                    self.fields[1][col],
                    self.fields[2][col],
                ]
            )

        # Diagonals
        lines.append(
            [
                self.fields[0][0],
                self.fields[1][1],
                self.fields[2][2],
            ]
        )

        lines.append(
            [
                self.fields[0][2],
                self.fields[1][1],
                self.fields[2][0],
            ]
        )

        for line in lines:
            if all(field == TicTacToeFieldType.CROSS for field in line):
                return TicTacToeState.CROSS_WON

            if all(field == TicTacToeFieldType.NAUGHT for field in line):
                return TicTacToeState.NAUGHT_WON

        if all(
            field != TicTacToeFieldType.EMPTY for row in self.fields for field in row
        ):
            return TicTacToeState.DRAW

        return TicTacToeState.IN_PROGRESS

    @property
    def winning_cells(self) -> list[tuple[int, int]] | None:
        lines = []

        # Rows
        for row in range(3):
            lines.append([(row, col) for col in range(3)])

        # Columns
        for col in range(3):
            lines.append([(row, col) for row in range(3)])

        # Diagonals
        lines.append([(0, 0), (1, 1), (2, 2)])
        lines.append([(0, 2), (1, 1), (2, 0)])

        for line in lines:
            values = [self.fields[r][c] for r, c in line]
            if all(v == TicTacToeFieldType.CROSS for v in values):
                return line
            if all(v == TicTacToeFieldType.NAUGHT for v in values):
                return line

        return None


@dataclass
class TicTacToeTurn:
    col: int
    row: int
    player: TicTacToeFieldType


@dataclass
class TicTacToeGame:
    player_1_name: str
    player_2_name: str
    tictactoe: TicTacToe
    turn_history: list[TicTacToeTurn] = field(default_factory=list)
    id: Optional[int] = None
    vs_com: bool = False

    def apply_turn(self, row: int, col: int) -> bool:
        turn_is_valid = self.tictactoe.turn_is_valid(row, col)
        if turn_is_valid:
            current_player = self.tictactoe.current_turn
            self.tictactoe.apply_turn(row, col)
            self.turn_history.append(
                TicTacToeTurn(col=col, row=row, player=current_player)
            )
        return turn_is_valid

    def convert_type_to_player_name(self, field_type: TicTacToeFieldType) -> str:
        match field_type:
            case TicTacToeFieldType.CROSS:
                return self.player_1_name
            case TicTacToeFieldType.NAUGHT:
                return self.player_2_name
            case _:
                return ""

    @property
    def current_turn_name(self) -> str:
        match self.tictactoe.current_turn:
            case TicTacToeFieldType.CROSS:
                return self.player_1_name
            case TicTacToeFieldType.NAUGHT:
                return self.player_2_name
            case TicTacToeFieldType.EMPTY:
                return ""
            case _:
                raise NotImplementedError()

    @property
    def winner_name(self) -> str:
        match self.tictactoe.state:
            case TicTacToeState.IN_PROGRESS:
                return "active"
            case TicTacToeState.DRAW:
                return "draw"
            case TicTacToeState.CROSS_WON:
                return self.player_1_name
            case TicTacToeState.NAUGHT_WON:
                return self.player_2_name
            case _:
                raise NotImplementedError()


class TicTacToeComputerPlayer:
    def choose_move(self, board: TicTacToe) -> tuple[int, int]:
        valid_moves = board.available_fields
        return random.choice(valid_moves)
