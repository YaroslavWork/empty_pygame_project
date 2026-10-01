import random

from scripts import settings as s


def get_random_color() -> tuple:
    """
    This function generate a random readable color (not too dark).
    :return: Color as an (r, g, b) tuple
    """
    return (
        random.randint(50, 255),
        random.randint(50, 255),
        random.randint(50, 255),
    )


class PlayerModel:
    """
    Data model of a player.
    This class holds only the state and the math (no pygame, no drawing).
    It represents one controllable rectangle in the world.
    """

    def __init__(self, x=None, y=None, color=None, size=None) -> None:
        self.x = s.PLAYER_START_X if x is None else x
        self.y = s.PLAYER_START_Y if y is None else y
        self.color = color or get_random_color()
        self.size = s.PLAYER_SIZE if size is None else size

        # Drawn position (smoothed toward the authoritative x, y between snapshots)
        self.render_x = self.x
        self.render_y = self.y

    def move_left(self, speed, dt) -> None:
        """
        This function move the player to the left side.
        :param speed: The speed of the player
        :param dt: Delta time
        :return: None
        """
        self.x -= speed * dt / 1000

    def move_right(self, speed, dt) -> None:
        """
        This function move the player to the right side.
        :param speed: The speed of the player
        :param dt: Delta time
        :return: None
        """
        self.x += speed * dt / 1000

    def move_up(self, speed, dt) -> None:
        """
        This function move the player up.
        :param speed: The speed of the player
        :param dt: Delta time
        :return: None
        """
        self.y -= speed * dt / 1000

    def move_down(self, speed, dt) -> None:
        """
        This function move the player down.
        :param speed: The speed of the player
        :param dt: Delta time
        :return: None
        """
        self.y += speed * dt / 1000

    def interpolate(self, dt, speed=None) -> None:
        """
        This function smooth the drawn position (render_x, render_y) toward the
        authoritative position (x, y). Called every frame so movement looks
        continuous between the lower-rate network snapshots.
        :param dt: Delta time
        :param speed: How fast the drawn position catches up (default from settings)
        :return: None
        """
        speed = s.PLAYER_INTERPOLATION_SPEED if speed is None else speed
        blend = min(1, speed * dt / 1000)  # Fraction to close this frame (frame-rate safe)

        self.render_x += (self.x - self.render_x) * blend
        self.render_y += (self.y - self.render_y) * blend

    def to_dict(self) -> dict:
        """
        This function convert player state to a plain dict (for network/save).
        :return: Player state as a dict
        """
        return {
            "x": self.x,
            "y": self.y,
            "color": list(self.color),
            "size": self.size,
        }

    def from_dict(self, data) -> None:
        """
        This function restore player state from a plain dict.
        :param data: Player state as a dict
        :return: None
        """
        self.x = data["x"]
        self.y = data["y"]
        self.color = tuple(data["color"])
        self.size = data["size"]
