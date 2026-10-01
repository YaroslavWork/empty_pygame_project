import pygame

from scripts.player.model import PlayerModel


class PlayerView:
    """
    Visual representation of a player.
    This class is responsible only for drawing a player rectangle.
    It reads the state from PlayerModel and never changes it.
    """

    def __init__(self, model: PlayerModel) -> None:
        self.model = model

    def draw(self, screen, camera_model) -> None:
        """
        This function draw the player on the screen.
        :param screen: Screen for drawing
        :param camera_model: The camera model used to convert global coordinates to local
        :return: None
        """
        center_x, center_y = camera_model.get_local_point(self.model.x, self.model.y)
        half_size = camera_model.get_local_radius(self.model.size / 2)

        rect = pygame.Rect(0, 0, half_size * 2, half_size * 2)
        rect.center = (center_x, center_y)

        pygame.draw.rect(screen, self.model.color, rect)
