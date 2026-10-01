import pygame

from scripts.field.model import FieldModel


class FieldView:
    """
    Visual representation of the field.
    This class is responsible only for drawing the field (the game world).
    It reads the state from FieldModel and never changes it.
    """

    def __init__(self, model: FieldModel) -> None:
        self.model = model

    def draw(self, screen, camera_model) -> None:
        """
        This function draw the field on the screen.
        :param screen: Screen for drawing
        :param camera_model: The camera model used to convert global coordinates to local
        :return: None
        """
        pass

