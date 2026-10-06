import pygame

from scripts.UI.button import Button
from scripts.UI.element import UIElement
from scripts.UI.text import TextView
from scripts.UI.ui import UI


class FakeElement(UIElement):
    def __init__(self):
        self.updates = []
        self.events = []
        self.draws = 0
        self.resets = 0

    def update(self, mouse_pos) -> None:
        self.updates.append(mouse_pos)

    def handle_input(self, event) -> None:
        self.events.append(event)

    def reset(self) -> None:
        self.resets += 1

    def draw(self, screen) -> None:
        self.draws += 1


def test_add_registers_element():
    ui = UI()
    element = FakeElement()

    ui.add(element)

    assert element in ui.elements


def test_update_passes_mouse_pos_to_elements():
    ui = UI()
    element = FakeElement()
    ui.add(element)

    ui.update((10, 20))

    assert element.updates == [(10, 20)]


def test_handle_input_passes_event_to_elements():
    ui = UI()
    element = FakeElement()
    ui.add(element)
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (0, 0)})

    ui.handle_input(event)

    assert element.events == [event]


def test_draw_draws_every_element(screen):
    ui = UI()
    first = FakeElement()
    second = FakeElement()
    ui.add(first)
    ui.add(second)

    ui.draw(screen)

    assert first.draws == 1
    assert second.draws == 1


def test_draw_draws_a_button(screen):
    TextView.fonts = {}
    ui = UI()
    button = Button("Reset", (10, 10), (100, 40), color=(210, 210, 210))
    button.update((500, 500))
    ui.add(button)
    screen.fill((255, 255, 255))

    ui.draw(screen)

    assert screen.get_at((13, 30)) == pygame.Color(210, 210, 210)


def test_draw_draws_a_text_view(screen):
    TextView.fonts = {}
    ui = UI()
    label = TextView("x", (0, 0, 0), 20, pos=(0, 0), center=False)
    ui.add(label)
    screen.fill((255, 255, 255))

    ui.draw(screen)

    changed = any(
        screen.get_at((x, y)) != pygame.Color(255, 255, 255)
        for x in range(label.text_surface.get_width())
        for y in range(label.text_surface.get_height())
    )
    assert changed


def test_reset_resets_every_element():
    ui = UI()
    first = FakeElement()
    second = FakeElement()
    ui.add(first)
    ui.add(second)

    ui.reset()

    assert first.resets == 1
    assert second.resets == 1
