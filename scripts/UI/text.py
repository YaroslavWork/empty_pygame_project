import pygame

from scripts.UI.element import UIElement


# Class TextView - represents text in the model (this class optimizes the use of fonts and a text surface
# because pygame.font.Font is very slow)
class TextView(UIElement):
    fonts = {}  # Dictionary of fonts

    def __init__(self, text, color, size_font, type_font=None, pos=(0, 0), center=True) -> None:
        if size_font in TextView.fonts:
            self.font = TextView.fonts[size_font]
        else:
            if type_font:
                self.font = pygame.font.Font("fonts/" + type_font + ".ttf", size_font)
            else:
                self.font = pygame.font.Font(None, size_font)
            TextView.fonts[size_font] = self.font
        self.color = color
        self.pos = pos
        self.center = center
        self.text_surface = self.font.render(text, True, color)

    def set_text(self, text) -> None:
        self.text_surface = self.font.render(text, True, self.color)

    def print(self, screen, pos, center=True) -> None:
        if center:
            screen.blit(self.text_surface, self.text_surface.get_rect(center=pos))
        else:
            screen.blit(self.text_surface, pos)

    def draw(self, screen) -> None:
        self.print(screen, self.pos, self.center)
