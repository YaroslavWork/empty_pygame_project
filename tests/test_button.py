import pygame

from scripts.UI.button import Button
from scripts.UI.element import UIElement
from scripts.UI.text import TextView


def test_button_is_a_ui_element():
    assert isinstance(Button("Reset", (10, 10), (100, 40)), UIElement)


def test_button_uses_text_view():
    button = Button("Reset", (10, 10), (100, 40))

    assert isinstance(button.text_view, TextView)


def test_is_hovered_returns_true_inside():
    button = Button("Reset", (10, 10), (100, 40))

    assert button.is_hovered((50, 30))


def test_is_hovered_returns_false_outside():
    button = Button("Reset", (10, 10), (100, 40))

    assert not button.is_hovered((500, 500))


def test_is_pressed_with_left_click_inside():
    button = Button("Reset", (10, 10), (100, 40))
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 30)})

    assert button.is_pressed(event)


def test_is_not_pressed_outside():
    button = Button("Reset", (10, 10), (100, 40))
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (500, 500)})

    assert not button.is_pressed(event)


def test_is_not_pressed_with_right_button():
    button = Button("Reset", (10, 10), (100, 40))
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (50, 30)})

    assert not button.is_pressed(event)


def test_is_not_pressed_on_mouse_up():
    button = Button("Reset", (10, 10), (100, 40))
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (50, 30)})

    assert not button.is_pressed(event)


def test_is_clicked_on_release_after_press_inside():
    button = Button("Reset", (10, 10), (100, 40))
    button.handle_input(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 30)}))
    release = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (50, 30)})

    assert button.is_clicked(release)


def test_is_not_clicked_on_press():
    button = Button("Reset", (10, 10), (100, 40))
    press = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 30)})

    assert not button.is_clicked(press)


def test_is_not_clicked_on_release_without_press():
    button = Button("Reset", (10, 10), (100, 40))
    release = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (50, 30)})

    assert not button.is_clicked(release)


def test_is_not_clicked_on_release_outside_after_press():
    button = Button("Reset", (10, 10), (100, 40))
    button.handle_input(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 30)}))
    release = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (500, 500)})

    assert not button.is_clicked(release)


def test_is_not_clicked_with_right_button():
    button = Button("Reset", (10, 10), (100, 40))
    button.handle_input(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (50, 30)}))
    release = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 3, "pos": (50, 30)})

    assert not button.is_clicked(release)


def test_update_sets_hovered_when_inside():
    button = Button("Reset", (10, 10), (100, 40))

    button.update((50, 30))

    assert button.hovered


def test_update_clears_hovered_when_outside():
    button = Button("Reset", (10, 10), (100, 40))
    button.hovered = True

    button.update((500, 500))

    assert not button.hovered


def test_handle_input_press_inside_sets_pressed_not_clicked():
    button = Button("Reset", (10, 10), (100, 40))
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 30)})

    button.handle_input(event)

    assert button.pressed
    assert not button.clicked


def test_handle_input_press_outside_ignored():
    button = Button("Reset", (10, 10), (100, 40))
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (500, 500)})

    button.handle_input(event)

    assert not button.pressed
    assert not button.clicked


def test_handle_input_release_inside_after_press_clicks():
    button = Button("Reset", (10, 10), (100, 40))
    button.handle_input(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 30)}))

    button.handle_input(pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (50, 30)}))

    assert button.clicked
    assert not button.pressed


def test_handle_input_release_without_press_does_not_click():
    button = Button("Reset", (10, 10), (100, 40))
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (50, 30)})

    button.handle_input(event)

    assert not button.clicked


def test_handle_input_release_outside_after_press_does_not_click():
    button = Button("Reset", (10, 10), (100, 40))
    button.handle_input(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 30)}))

    button.handle_input(pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (500, 500)}))

    assert not button.clicked
    assert not button.pressed


def test_draw_uses_normal_color_when_not_hovered(screen):
    TextView.fonts = {}
    button = Button("Reset", (10, 10), (100, 40), color=(210, 210, 210))
    button.update((500, 500))
    screen.fill((255, 255, 255))

    button.draw(screen)

    assert screen.get_at((13, 30)) == pygame.Color(210, 210, 210)


def test_draw_uses_hover_color_when_hovered(screen):
    TextView.fonts = {}
    button = Button("Reset", (10, 10), (100, 40), hover_color=(180, 180, 180))
    button.update((50, 30))
    screen.fill((255, 255, 255))

    button.draw(screen)

    assert screen.get_at((13, 30)) == pygame.Color(180, 180, 180)


def test_draw_uses_pressed_color_when_pressed(screen):
    TextView.fonts = {}
    button = Button("Reset", (10, 10), (100, 40), pressed_color=(150, 150, 150))
    button.update((50, 30))
    button.handle_input(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 30)}))
    screen.fill((255, 255, 255))

    button.draw(screen)

    assert screen.get_at((13, 30)) == pygame.Color(150, 150, 150)


def test_reset_clears_clicked():
    button = Button("Reset", (10, 10), (100, 40))
    button.clicked = True

    button.reset()

    assert not button.clicked


def test_reset_keeps_pressed():
    button = Button("Reset", (10, 10), (100, 40))
    button.pressed = True

    button.reset()

    assert button.pressed
