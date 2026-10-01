from scripts.camera import CameraModel
from scripts.field import FieldModel

MOVE_SPEED = 1
ZOOM_SPEED = 1


class WorldModel:
    """
    Data model of the whole world.
    Owns the game models, applies input intents and exposes a snapshot.
    This class holds only the state and the math (no pygame, no drawing).
    """

    def __init__(self, camera_model=None, field_model=None) -> None:
        self.camera_model = camera_model or CameraModel(x=0, y=0, distance=10)
        self.field_model = field_model or FieldModel()

    def step(self, dt, intents) -> None:
        """
        This function advance the world by dt using a set of input intents.
        :param dt: Delta time
        :param intents: Collection of action strings (ex. "left", "zoom_in")
        :return: None
        """
        intents = set(intents)

        if "left" in intents:
            self.camera_model.move_left(MOVE_SPEED, dt)
        if "right" in intents:
            self.camera_model.move_right(MOVE_SPEED, dt)
        if "up" in intents:
            self.camera_model.move_up(MOVE_SPEED, dt)
        if "down" in intents:
            self.camera_model.move_down(MOVE_SPEED, dt)
        if "zoom_in" in intents:
            self.camera_model.scale_in(ZOOM_SPEED, dt)
        if "zoom_out" in intents:
            self.camera_model.scale_out(ZOOM_SPEED, dt)

    def snapshot(self) -> dict:
        """
        This function convert the whole world state to a plain dict.
        :return: World state as a dict
        """
        return {
            "camera": self.camera_model.to_dict(),
            "field": self.field_model.to_dict(),
        }

    def apply_snapshot(self, data) -> None:
        """
        This function restore the whole world state from a plain dict.
        :param data: World state as a dict
        :return: None
        """
        self.camera_model.from_dict(data["camera"])
        self.field_model.from_dict(data["field"])
