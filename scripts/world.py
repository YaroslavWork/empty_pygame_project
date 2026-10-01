from scripts import settings as s
from scripts.camera import CameraModel
from scripts.field import FieldModel
from scripts.player import PlayerModel


class WorldModel:
    """
    Data model of the whole world.
    Owns the game models, applies input intents and exposes a snapshot.
    This class holds only the state and the math (no pygame, no drawing).
    """

    def __init__(self, camera_model=None, field_model=None) -> None:
        self.camera_model = camera_model or CameraModel(
            x=s.CAMERA_START_X,
            y=s.CAMERA_START_Y,
            distance=s.CAMERA_START_DISTANCE,
        )
        self.field_model = field_model or FieldModel()
        self.players = {}

    def add_player(self, player_id, player_model=None):
        """
        This function add a player to the world.
        Player ids are normalized to strings so they survive a JSON round trip.
        :param player_id: Identifier of the player (ex. a client)
        :param player_model: Optional player model to use
        :return: The added player model
        """
        player = player_model or PlayerModel()
        self.players[str(player_id)] = player

        return player

    def remove_player(self, player_id) -> None:
        """
        This function remove a player from the world.
        :param player_id: Identifier of the player
        :return: None
        """
        self.players.pop(str(player_id), None)

    def step(self, dt, intents) -> None:
        """
        This function advance the whole world by dt.
        It applies zoom intents to the camera and movement intents to every
        player in the world (singleplayer has exactly one player).
        :param dt: Delta time
        :param intents: Collection of action strings (ex. "left", "zoom_in")
        :return: None
        """
        self.step_players(dt, {player_id: intents for player_id in self.players})

        intents = set(intents)

        if "zoom_in" in intents:
            self.camera_model.scale_in(s.CAMERA_ZOOM_SPEED, dt)
        if "zoom_out" in intents:
            self.camera_model.scale_out(s.CAMERA_ZOOM_SPEED, dt)

    def step_players(self, dt, intents_by_player) -> None:
        """
        This function advance every player by dt using per-player intents.
        :param dt: Delta time
        :param intents_by_player: Mapping of player_id to a collection of action strings
        :return: None
        """
        for player_id, player in self.players.items():
            self.step_player(player, set(intents_by_player.get(player_id, ())), dt)

    def step_player(self, player, intents, dt) -> None:
        """
        This function advance a single player by dt using its intents.
        :param player: The player model to advance
        :param intents: Collection of action strings (ex. "left")
        :param dt: Delta time
        :return: None
        """
        if "left" in intents:
            player.move_left(s.PLAYER_MOVE_SPEED, dt)
        if "right" in intents:
            player.move_right(s.PLAYER_MOVE_SPEED, dt)
        if "up" in intents:
            player.move_up(s.PLAYER_MOVE_SPEED, dt)
        if "down" in intents:
            player.move_down(s.PLAYER_MOVE_SPEED, dt)

    def snapshot(self) -> dict:
        """
        This function convert the whole world state to a plain dict.
        :return: World state as a dict
        """
        return {
            "camera": self.camera_model.to_dict(),
            "field": self.field_model.to_dict(),
            "players": {player_id: player.to_dict() for player_id, player in self.players.items()},
        }

    def apply_snapshot(self, data) -> None:
        """
        This function restore the whole world state from a plain dict.
        :param data: World state as a dict
        :return: None
        """
        self.camera_model.from_dict(data["camera"])
        self.field_model.from_dict(data["field"])
        self.apply_players_snapshot(data.get("players", {}))

    def apply_players_snapshot(self, players_data) -> None:
        """
        This function sync the players in place with a plain dict of players,
        creating and removing players as needed so views keep stable references.
        :param players_data: Mapping of player_id to player state as a dict
        :return: None
        """
        players_data = {str(player_id): player_data for player_id, player_data in players_data.items()}

        for player_id in list(self.players):
            if player_id not in players_data:
                self.remove_player(player_id)

        for player_id, player_data in players_data.items():
            if player_id not in self.players:
                self.add_player(player_id)

            self.players[player_id].from_dict(player_data)

