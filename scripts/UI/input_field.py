import pygame

from scripts.UI.element import UIElement
from scripts.UI.text import TextView


# Class InputField - a text input UI element (this class draws a rectangle and
# renders its content with TextView, so it reuses the cached-font text rendering).
# Hovering highlights it, clicking inside focuses it (the field is then "active" and
# accepts typed characters), clicking somewhere else leaves it. The typed text is
# available with get_text() / the text property. active (activate() / deactivate())
# is the same enabled flag Button has: an inactive field is visible but ignores input.
class InputField(UIElement):
    def __init__(self, pos, size, color=(210, 210, 210), hover_color=(180, 180, 180),
                 focused_color=(230, 230, 230), border_color=(0, 0, 0),
                 text_color=(0, 0, 0), border_width=2, border_radius=6, size_font=24,
                 placeholder="", placeholder_color=(150, 150, 150),
                 max_length=None) -> None:
        self.rect = pygame.Rect(pos, size)
        self.color = color
        self.hover_color = hover_color
        self.focused_color = focused_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.padding = 8
        self.placeholder = placeholder
        self.max_length = max_length
        self._text = ""
        self.text_view = TextView("", text_color, size_font)
        self.placeholder_view = TextView(placeholder, placeholder_color, size_font)

        self._visible = True
        self.hovered = False
        self.focused = False
        self.active = True
        self.submitted = False

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value) -> None:
        self.set_text(value)

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value) -> None:
        self._visible = value
        if not value:
            self.unfocus()  # a hidden field must not keep receiving typed characters

    def is_hovered(self, mouse_pos) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event) -> bool:
        return (self.visible
                and self.active
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.is_hovered(event.pos))

    def is_typing(self) -> bool:
        """True while typed characters are accepted (shown, enabled and focused)."""
        return self.visible and self.active and self.focused

    def focus(self) -> None:
        """Start editing, so typed characters land in the field."""
        if self.visible and self.active:
            self.focused = True

    def unfocus(self) -> None:
        """Stop editing, so typed characters are ignored again."""
        self.focused = False

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False
        self.unfocus()

    def set_text(self, text) -> None:
        """Replace the whole content (characters past max_length are dropped)."""
        if self.max_length is not None:
            text = text[:self.max_length]
        self._text = text
        self.text_view.set_text(text)

    def get_text(self) -> str:
        """The text the user typed in (an empty string when nothing was typed)."""
        return self._text

    def clear(self) -> None:
        self.set_text("")

    def type_text(self, text) -> None:
        """Append typed characters - only accepted while the field is editing."""
        if not self.is_typing():
            return
        self.set_text(self._text + text)

    def backspace(self) -> None:
        """Remove the last typed character - only accepted while editing."""
        if not self.is_typing():
            return
        self.set_text(self._text[:-1])

    def update(self, mouse_pos) -> None:
        self.hovered = self.visible and self.active and self.is_hovered(mouse_pos)

    def handle_input(self, event) -> None:
        if not self.visible or not self.active:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered(event.pos):
                self.focus()
            else:
                self.unfocus()
            return
        if not self.focused:
            return  # only the focused field reacts to typed characters
        if event.type == pygame.TEXTINPUT:
            self.type_text(event.text)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.backspace()
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.submitted = True
            elif event.key == pygame.K_ESCAPE:
                self.unfocus()

    def draw(self, screen) -> None:
        if not self.visible:
            return
        color = self.color
        if self.hovered:
            color = self.hover_color
        if self.focused:
            color = self.focused_color
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.border_color, self.rect,
                         width=self.border_width, border_radius=self.border_radius)

        height = self.text_view.text_surface.get_height()
        pos = (self.rect.x + self.padding, self.rect.centery - height // 2)
        if self._text:
            self.text_view.print(screen, pos, False)
        elif self.placeholder:
            self.placeholder_view.print(screen, pos, False)
        if self.focused:  # caret marks where the next character lands
            caret_x = pos[0] + self.text_view.text_surface.get_width() + 2
            pygame.draw.line(screen, self.border_color,
                             (caret_x, pos[1] + 3), (caret_x, pos[1] + height - 3), 2)

    def reset(self) -> None:
        self.submitted = False
