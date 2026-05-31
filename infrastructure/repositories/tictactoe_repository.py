from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, Field, select

from domain.tictactoe import TicTacToeGame, TicTacToeFieldType, TicTacToe


class TicTacToeGameRecord(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    tictactoe_serialized: str
    player_1_name: str
    player_2_name: str


class TicTacToeSerializer:
    @classmethod
    def map_field_character(cls, field_type: TicTacToeFieldType) -> str:
        match field_type:
            case TicTacToeFieldType.CROSS:
                return "X"
            case TicTacToeFieldType.NAUGHT:
                return "O"
            case TicTacToeFieldType.EMPTY:
                return "_"
            case _:
                raise NotImplementedError()

    @classmethod
    def map_character_field(cls, string: str) -> TicTacToeFieldType:
        match string:
            case "X":
                return TicTacToeFieldType.CROSS
            case "O":
                return TicTacToeFieldType.NAUGHT
            case "_":
                return TicTacToeFieldType.EMPTY
            case _:
                raise NotImplementedError()

    @classmethod
    def serialize(cls, game: TicTacToe) -> str:
        output = ""
        for field_row in game.fields:
            for field in field_row:
                output += cls.map_field_character(field)
        return output

    @classmethod
    def deserialize(cls, game_string: str) -> TicTacToe:
        if len(game_string) != 9:
            raise ValueError()

        field_types = []
        for character in game_string:
            field_types.append(cls.map_character_field(character))

        size = 3
        fields = [field_types[i:i + size] for i in range(0, len(field_types), size)]

        return TicTacToe(fields=fields)


engine = create_engine("sqlite:///tictactoe.db")
SQLModel.metadata.create_all(engine)


class TicTacToeRepository:
    @classmethod
    def _to_record(cls, tictactoe_game: TicTacToeGame) -> TicTacToeGameRecord:
        tictactoe_serialized = TicTacToeSerializer.serialize(tictactoe_game.tictactoe)
        return TicTacToeGameRecord(
            id=tictactoe_game.id,
            player_1_name=tictactoe_game.player_1_name,
            player_2_name=tictactoe_game.player_2_name,
            tictactoe_serialized=tictactoe_serialized,
        )

    @classmethod
    def _to_domain(cls, tictactoe_game_record: TicTacToeGameRecord) -> TicTacToeGame:
        tictactoe_deserialized = TicTacToeSerializer.deserialize(tictactoe_game_record.tictactoe_serialized)
        return TicTacToeGame(
            id=tictactoe_game_record.id,
            player_1_name=tictactoe_game_record.player_1_name,
            player_2_name=tictactoe_game_record.player_2_name,
            tictactoe=tictactoe_deserialized,
        )

    def delete(self, id: int) -> bool:
        with Session(engine) as session:
            game = session.get(TicTacToeGameRecord, id)

            if game is None:
                return False

            session.delete(game)
            session.commit()
            return True

    def save(self, tictactoe_game: TicTacToeGame) -> TicTacToeGameRecord:
        with Session(engine) as session:
            record = session.merge(self._to_record(tictactoe_game))
            session.commit()
            session.refresh(record)
            return record

    def get_by_id(self, tictactoe_game_id: int) -> TicTacToeGame | None:
        with Session(engine) as session:
            tictactoe_record = session.get(TicTacToeGameRecord, tictactoe_game_id)
            if tictactoe_record is None:
                return None
            return self._to_domain(tictactoe_record)

    def get_all(self) -> list[TicTacToeGame]:
        with Session(engine) as session:
            records = session.exec(select(TicTacToeGameRecord).order_by(TicTacToeGameRecord.id.desc())).all()
            return [
                self._to_domain(record)
                for record in records
            ]
