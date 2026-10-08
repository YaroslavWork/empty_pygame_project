import pygame

from scripts.UI.button import Button
from scripts.UI.element import UIElement
from scripts.UI.group import UIGroup
from scripts.UI.text import TextView


def test_group_is_a_ui_element():
    assert isinstance(UIGroup(), UIElement)


def test_group_starts_empty():
    assert UIGroup().elements == []


def test_add_puts_element_in_group():
    group = UIGroup()
    button = Button("Reset", (10, 10), (100, 40))

    group.add(button)

    assert button in group.elements


def test_hide_hides_every_element():
    group = UIGroup()
    button = Button("Reset", (10, 10), (100, 40))
    label = TextView("hi", (0, 0, 0), 20)
    group.add(button)
    group.add(label)

    group.hide()

    assert not group.visible
    assert not button.visible
    assert not label.visible


def test_show_shows_every_element_again():
    group = UIGroup()
    button = Button("Reset", (10, 10), (100, 40))
    group.add(button)
    group.hide()

    group.show()

    assert group.visible
    assert button.visible


def test_setting_visible_false_hides_every_element():
    group = UIGroup()
    button = Button("Reset", (10, 10), (100, 40))
    group.add(button)

    group.visible = False

    assert not button.visible


def test_element_added_to_hidden_group_is_hidden():
    group = UIGroup()
    button = Button("Reset", (10, 10), (100, 40))
    group.hide()

    group.add(button)

    assert not button.visible


def test_update_forwards_to_elements():
    group = UIGroup()
    button = Button("Reset", (10, 10), (100, 40))
    group.add(button)

    group.update((50, 30))

    assert button.hovered


def test_handle_input_forwards_to_elements():
    group = UIGroup()
    button = Button("Reset", (10, 10), (100, 40))
    group.add(button)
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 30)})

    group.handle_input(event)

    assert button.pressed


def test_reset_forwards_to_elements():
    group = UIGroup()
    button = Button("Reset", (10, 10), (100, 40))
    button.clicked = True
    group.add(button)

    group.reset()

    assert not button.clicked


def test_draw_draws_every_element(screen):
    TextView.fonts = {}
    group = UIGroup()
    button = Button("Reset", (10, 10), (100, 40), color=(210, 210, 210))
    group.add(button)
    screen.fill((255, 255, 255))

    group.draw(screen)

    assert screen.get_at((13, 30)) == pygame.Color(210, 210, 210)


def test_hidden_group_draws_nothing(screen):
    TextView.fonts = {}
    group = UIGroup()
    button = Button("Reset", (10, 10), (100, 40), color=(210, 210, 210))
    group.add(button)
    group.hide()
    screen.fill((255, 255, 255))

    group.draw(screen)

    assert screen.get_at((13, 30)) == pygame.Color(255, 255, 255)


def test_hidden_group_button_is_not_clickable():
    group = UIGroup()
    button = Button("Reset", (10, 10), (100, 40))
    group.add(button)
    group.hide()
    press = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 30)})
    release = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (50, 30)})

    group.handle_input(press)
    group.handle_input(release)

    assert not button.clicked


def test_showing_group_after_hide_restores_pressing():
    group = UIGroup()
    button = Button("Reset", (10, 10), (100, 40))
    group.add(button)
    group.hide()
    group.show()
    press = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (50, 30)})
    release = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (50, 30)})

    group.handle_input(press)
    group.handle_input(release)

    assert button.clicked


def test_nested_group_visibility_cascades():
    outer = UIGroup()
    inner = UIGroup()
    button = Button("Reset", (10, 10), (100, 40))
    inner.add(button)
    outer.add(inner)

    outer.hide()

    assert not inner.visible
    assert not button.visible
