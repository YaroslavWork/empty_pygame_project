import pygame

from scripts import settings as s
from scripts.camera.model import CameraModel
from scripts.UI.text import TextView


class CameraView:
    """
    Visual representation of the camera.
    This class is responsible only for drawing camera related things
    (for example the map scale UI). It reads the state from CameraModel
    and never changes it.
    """

    def __init__(self, model: CameraModel) -> None:
        self.model = model

    def get_scale_value(self, min_pixels_scale=s.SCALE_MIN_PIXELS,
                        max_pixels_scale=s.SCALE_MAX_PIXELS,
                        first_digital=s.SCALE_FIRST_DIGITAL) -> float:
        """
        This function calculate the closest "nice" distance (in meters)
        for the map scale based on the current camera zoom.
        :param min_pixels_scale: The value of min pixels scale
        :param max_pixels_scale: The value of max pixels scale
        :param first_digital: The first digital for scale (ex. (1, 2, 5))
        :return: The distance (in meters) represented by the map scale
        """
        resolution = self.model.resolution
        distance = self.model.distance

        min_distance = min_pixels_scale / resolution[0] * distance  # Calculate distance for min pixels scale
        max_distance = max_pixels_scale / resolution[0] * distance  # Calculate distance for max pixels scale
        mean_distance = (min_distance + max_distance) / 2  # Mean distance

        # Find the closest digit to the mean distance (ex. if mean distance is 120, then the closest digit is 100)
        digit_amount = len(str(int(mean_distance)))  # Calculate amount of digits
        multiply = 10 ** (digit_amount - 1)  # Calculate multiply for the closest digit
        close_digit = mean_distance / multiply  # Calculate closest digit
        close_digit = min(first_digital, key=lambda x: abs(x - close_digit))  # Find the closest digit
        close_digit = close_digit * multiply  # Add multiplying to the closest digit

        return close_digit

    # This function draw map scale on the screen (the part of UI)
    def draw_map_scale(self, screen, min_pixels_scale=s.SCALE_MIN_PIXELS,
                       max_pixels_scale=s.SCALE_MAX_PIXELS,
                       first_digital=s.SCALE_FIRST_DIGITAL,
                       offset=s.SCALE_OFFSET,
                       stick_width=s.SCALE_STICK_WIDTH) -> None:
        """
        This function draw map scale on the screen (the part of UI)
        :param screen: Screen for drawing
        :param min_pixels_scale: The value of min pixels scale
        :param max_pixels_scale: The value of max pixels scale
        :param first_digital: The first digital for scale (ex. (1, 2, 5))
        :param offset: Offset for scale (for UI)
        :param stick_width: Width of the stick
        :return: None
        """
        resolution = self.model.resolution
        distance = self.model.distance
        color = s.COLORS["scale"]

        # Calculate the closest digit for the current zoom level
        close_digit = self.get_scale_value(min_pixels_scale, max_pixels_scale, first_digital)

        # Calculate line length for the closest digit
        line_length = close_digit / distance * resolution[0]

        # Calculate line length (left and right points)
        left_pos = (resolution[0] - offset[0] - line_length, resolution[1] - offset[1])
        right_pos = (resolution[0] - offset[0], resolution[1] - offset[1])

        # Draw lines
        pygame.draw.line(screen, color, left_pos, right_pos, s.SCALE_LINE_WIDTH)
        pygame.draw.line(screen,
                         color,
                         (left_pos[0], left_pos[1] - stick_width),
                         (left_pos[0], left_pos[1] + stick_width),
                         s.SCALE_LINE_WIDTH)
        pygame.draw.line(screen, color,
                         (right_pos[0], right_pos[1] + stick_width),
                         (right_pos[0], right_pos[1] - stick_width),
                         s.SCALE_LINE_WIDTH)

        # Text
        text_pos = (right_pos[0] + s.SCALE_LABEL_OFFSET[0], right_pos[1] + s.SCALE_LABEL_OFFSET[1])
        if close_digit >= 1000:
            TextView(str(int(close_digit / 1000)) + " km", color, s.HUD_FONT_SIZE).print(screen, text_pos, True)
        else:
            TextView(str(int(close_digit)) + " m", color, s.HUD_FONT_SIZE).print(screen, text_pos, True)
