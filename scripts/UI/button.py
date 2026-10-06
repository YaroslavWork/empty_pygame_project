import pygame

from scripts.UI.element import UIElement
from scripts.UI.text import TextView


# Class Button - a clickable UI element (this class draws a rectangle and renders
# its label with TextView, so it reuses the cached-font text rendering)
class Button(UIElement):
    def __init__(self, text, pos, size, color=(210, 210, 210),
                 hover_color=(180, 180, 180), pressed_color=(150, 150, 150),
                 border_color=(0, 0, 0), text_color=(0, 0, 0), border_width=2,
                 border_radius=6, size_font=24) -> None:
        self.rect = pygame.Rect(pos, size)
        self.color = color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.text_view = TextView(text, text_color, size_font)

        self.hovered = False
        self.pressed = False
        self.clicked = False

    def is_hovered(self, mouse_pos) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def is_pressed(self, event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.is_hovered(event.pos))

    def is_released(self, event) -> bool:
        return event.type == pygame.MOUSEBUTTONUP and event.button == 1

    def is_clicked(self, event) -> bool:
        return self.is_released(event) and self.pressed and self.is_hovered(event.pos)

    def update(self, mouse_pos) -> None:
        self.hovered = self.is_hovered(mouse_pos)

    def handle_input(self, event) -> None:
        if self.is_pressed(event):
            self.pressed = True
        elif self.is_clicked(event):
            self.clicked = True
            self.pressed = False
        elif self.is_released(event):
            self.pressed = False

    def draw(self, screen) -> None:
        color = self.color
        if self.hovered:
            color = self.hover_color
        if self.pressed:
            color = self.pressed_color
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.border_color, self.rect,
                         width=self.border_width, border_radius=self.border_radius)
        self.text_view.print(screen, self.rect.center, True)

    def reset(self) -> None:
        self.clicked = False
