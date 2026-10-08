import pygame

from scripts.UI.element import UIElement
from scripts.UI.input_field import InputField
from scripts.UI.text import TextView


def mouse_down(pos=(50, 30), button=1):
    return pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": button, "pos": pos})


def typed(text):
    return pygame.event.Event(pygame.TEXTINPUT, {"text": text})


def key_down(key):
    return pygame.event.Event(pygame.KEYDOWN, {"key": key, "unicode": "", "mod": 0})


def test_input_field_is_a_ui_element():
    assert isinstance(InputField((10, 10), (100, 40)), UIElement)


def test_input_field_uses_text_view():
    field = InputField((10, 10), (100, 40))

    assert isinstance(field.text_view, TextView)


def test_input_field_starts_empty():
    assert InputField((10, 10), (100, 40)).get_text() == ""


def test_is_hovered_returns_true_inside():
    field = InputField((10, 10), (100, 40))

    assert field.is_hovered((50, 30))


def test_is_hovered_returns_false_outside():
    field = InputField((10, 10), (100, 40))

    assert not field.is_hovered((500, 500))


def test_is_clicked_on_left_click_inside():
    field = InputField((10, 10), (100, 40))

    assert field.is_clicked(mouse_down())


def test_is_not_clicked_outside():
    field = InputField((10, 10), (100, 40))

    assert not field.is_clicked(mouse_down((500, 500)))


def test_is_not_clicked_with_right_button():
    field = InputField((10, 10), (100, 40))

    assert not field.is_clicked(mouse_down(button=3))


def test_is_not_clicked_on_mouse_up():
    field = InputField((10, 10), (100, 40))
    event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (50, 30)})

    assert not field.is_clicked(event)


def test_update_sets_hovered_when_inside():
    field = InputField((10, 10), (100, 40))

    field.update((50, 30))

    assert field.hovered


def test_update_clears_hovered_when_outside():
    field = InputField((10, 10), (100, 40))
    field.hovered = True

    field.update((500, 500))

    assert not field.hovered


def test_inactive_field_is_not_hovered():
    field = InputField((10, 10), (100, 40))
    field.deactivate()

    field.update((50, 30))

    assert not field.hovered


def test_hidden_field_is_not_hovered():
    field = InputField((10, 10), (100, 40))
    field.hide()

    field.update((50, 30))

    assert not field.hovered


def test_click_inside_focuses_the_field():
    field = InputField((10, 10), (100, 40))

    field.handle_input(mouse_down())

    assert field.focused


def test_click_outside_unfocuses_the_field():
    field = InputField((10, 10), (100, 40))
    field.handle_input(mouse_down())

    field.handle_input(mouse_down((500, 500)))

    assert not field.focused


def test_click_on_inactive_field_does_not_focus():
    field = InputField((10, 10), (100, 40))
    field.deactivate()

    field.handle_input(mouse_down())

    assert not field.focused


def test_click_on_hidden_field_does_not_focus():
    field = InputField((10, 10), (100, 40))
    field.hide()

    field.handle_input(mouse_down())

    assert not field.focused


def test_focus_sets_focused():
    field = InputField((10, 10), (100, 40))

    field.focus()

    assert field.focused


def test_unfocus_clears_focused():
    field = InputField((10, 10), (100, 40))
    field.focus()

    field.unfocus()

    assert not field.focused


def test_deactivate_unfocuses_the_field():
    field = InputField((10, 10), (100, 40))
    field.focus()

    field.deactivate()

    assert not field.focused


def test_hide_unfocuses_the_field():
    field = InputField((10, 10), (100, 40))
    field.focus()

    field.hide()

    assert not field.focused


def test_reactivated_field_can_be_focused_again():
    field = InputField((10, 10), (100, 40))
    field.deactivate()
    field.activate()

    field.handle_input(mouse_down())

    assert field.focused


def test_is_typing_requires_visible_active_and_focused():
    field = InputField((10, 10), (100, 40))
    field.focus()

    assert field.is_typing()

    field.deactivate()

    assert not field.is_typing()


def test_focused_field_accepts_typed_characters():
    field = InputField((10, 10), (100, 40))
    field.focus()

    field.handle_input(typed("a"))

    assert field.get_text() == "a"


def test_typed_characters_are_appended():
    field = InputField((10, 10), (100, 40))
    field.focus()

    field.handle_input(typed("a"))
    field.handle_input(typed("b"))
    field.handle_input(typed("c"))

    assert field.get_text() == "abc"


def test_multi_character_input_is_appended_whole():
    field = InputField((10, 10), (100, 40))
    field.focus()

    field.handle_input(typed("hello"))

    assert field.get_text() == "hello"


def test_typing_is_ignored_when_not_focused():
    field = InputField((10, 10), (100, 40))

    field.handle_input(typed("a"))

    assert field.get_text() == ""


def test_typing_is_ignored_when_inactive():
    field = InputField((10, 10), (100, 40))
    field.focus()
    field.deactivate()

    field.handle_input(typed("a"))

    assert field.get_text() == ""


def test_typing_is_ignored_after_clicking_outside():
    field = InputField((10, 10), (100, 40))
    field.handle_input(mouse_down())
    field.handle_input(mouse_down((500, 500)))

    field.handle_input(typed("a"))

    assert field.get_text() == ""


def test_typing_is_ignored_when_hidden():
    field = InputField((10, 10), (100, 40))
    field.focus()
    field.hide()
    field.show()

    field.handle_input(typed("a"))

    assert field.get_text() == ""


def test_keydown_alone_does_not_append_characters():
    field = InputField((10, 10), (100, 40))
    field.focus()

    field.handle_input(key_down(pygame.K_a))

    assert field.get_text() == ""


def test_backspace_removes_the_last_character():
    field = InputField((10, 10), (100, 40))
    field.focus()
    field.set_text("abc")

    field.handle_input(key_down(pygame.K_BACKSPACE))

    assert field.get_text() == "ab"


def test_backspace_is_ignored_when_not_focused():
    field = InputField((10, 10), (100, 40))
    field.set_text("abc")

    field.handle_input(key_down(pygame.K_BACKSPACE))

    assert field.get_text() == "abc"


def test_backspace_on_empty_field_stays_empty():
    field = InputField((10, 10), (100, 40))
    field.focus()

    field.handle_input(key_down(pygame.K_BACKSPACE))

    assert field.get_text() == ""


def test_escape_unfocuses_the_field():
    field = InputField((10, 10), (100, 40))
    field.focus()

    field.handle_input(key_down(pygame.K_ESCAPE))

    assert not field.focused


def test_return_submits_the_field():
    field = InputField((10, 10), (100, 40))
    field.focus()

    field.handle_input(key_down(pygame.K_RETURN))

    assert field.submitted


def test_return_does_not_submit_when_not_focused():
    field = InputField((10, 10), (100, 40))

    field.handle_input(key_down(pygame.K_RETURN))

    assert not field.submitted


def test_reset_clears_submitted():
    field = InputField((10, 10), (100, 40))
    field.focus()
    field.handle_input(key_down(pygame.K_RETURN))

    field.reset()

    assert not field.submitted


def test_text_property_returns_the_typed_text():
    field = InputField((10, 10), (100, 40))
    field.focus()

    field.handle_input(typed("Bob"))

    assert field.text == "Bob"


def test_setting_text_replaces_the_content():
    field = InputField((10, 10), (100, 40))

    field.text = "Bob"

    assert field.get_text() == "Bob"


def test_set_text_updates_the_rendered_surface():
    TextView.fonts = {}
    field = InputField((10, 10), (100, 40))
    before = field.text_view.text_surface.get_width()

    field.set_text("a much longer content")

    assert field.text_view.text_surface.get_width() > before


def test_set_text_works_without_focus():
    field = InputField((10, 10), (100, 40))

    field.set_text("preset")

    assert field.get_text() == "preset"


def test_clear_empties_the_field():
    field = InputField((10, 10), (100, 40))
    field.set_text("preset")

    field.clear()

    assert field.get_text() == ""


def test_max_length_caps_typed_text():
    field = InputField((10, 10), (100, 40), max_length=3)
    field.focus()

    field.handle_input(typed("abcdef"))

    assert field.get_text() == "abc"


def test_max_length_caps_characters_typed_one_by_one():
    field = InputField((10, 10), (100, 40), max_length=2)
    field.focus()

    for character in "abcd":
        field.handle_input(typed(character))

    assert field.get_text() == "ab"


def test_max_length_truncates_set_text():
    field = InputField((10, 10), (100, 40), max_length=3)

    field.set_text("abcdef")

    assert field.get_text() == "abc"


def test_max_length_does_not_block_backspace():
    field = InputField((10, 10), (100, 40), max_length=3)
    field.focus()
    field.set_text("abc")

    field.handle_input(key_down(pygame.K_BACKSPACE))

    assert field.get_text() == "ab"


def test_input_field_keeps_its_rect_when_text_changes():
    field = InputField((10, 10), (100, 40))
    rect = field.rect.copy()

    field.set_text("a very long content that does not fit")

    assert field.rect == rect


def test_idle_field_draws_its_base_colour(screen):
    TextView.fonts = {}
    field = InputField((10, 10), (100, 40), color=(210, 210, 210))
    screen.fill((255, 255, 255))

    field.draw(screen)

    assert screen.get_at((13, 30)) == pygame.Color(210, 210, 210)


def test_hovered_field_draws_its_hover_colour(screen):
    TextView.fonts = {}
    field = InputField((10, 10), (100, 40), color=(210, 210, 210),
                       hover_color=(180, 180, 180))
    field.update((50, 30))
    screen.fill((255, 255, 255))

    field.draw(screen)

    assert screen.get_at((13, 30)) == pygame.Color(180, 180, 180)


def test_focused_field_draws_its_focused_colour(screen):
    TextView.fonts = {}
    field = InputField((10, 10), (100, 40), color=(210, 210, 210),
                       hover_color=(180, 180, 180), focused_color=(230, 230, 230))
    field.update((50, 30))
    field.focus()
    screen.fill((255, 255, 255))

    field.draw(screen)

    assert screen.get_at((13, 30)) == pygame.Color(230, 230, 230)


def test_hidden_field_draws_nothing(screen):
    TextView.fonts = {}
    field = InputField((10, 10), (100, 40), color=(210, 210, 210), placeholder="Name")
    field.hide()
    screen.fill((255, 255, 255))

    field.draw(screen)

    assert screen.get_at((13, 30)) == pygame.Color(255, 255, 255)


def test_shown_field_draws_again(screen):
    TextView.fonts = {}
    field = InputField((10, 10), (100, 40), color=(210, 210, 210))
    field.hide()
    field.show()
    screen.fill((255, 255, 255))

    field.draw(screen)

    assert screen.get_at((13, 30)) == pygame.Color(210, 210, 210)


def test_focused_field_draws_a_caret(screen):
    TextView.fonts = {}
    field = InputField((10, 10), (120, 40), color=(210, 210, 210))
    field.set_text("ab")

    screen.fill((255, 255, 255))
    field.draw(screen)
    without_caret = [screen.get_at((x, 30)) for x in range(10, 131)]

    field.focus()
    screen.fill((255, 255, 255))
    field.draw(screen)

    assert [screen.get_at((x, 30)) for x in range(10, 131)] != without_caret


def test_focused_empty_field_draws_a_caret(screen):
    TextView.fonts = {}
    field = InputField((10, 10), (120, 40), color=(210, 210, 210))

    screen.fill((255, 255, 255))
    field.draw(screen)
    unfocused = [screen.get_at((x, 30)) for x in range(10, 131)]

    field.focus()
    screen.fill((255, 255, 255))
    field.draw(screen)

    assert [screen.get_at((x, 30)) for x in range(10, 131)] != unfocused


def test_placeholder_is_drawn_while_the_field_is_empty(screen):
    TextView.fonts = {}
    field = InputField((10, 10), (120, 40), color=(210, 210, 210), placeholder="Name")

    screen.fill((255, 255, 255))
    field.draw(screen)
    with_placeholder = [screen.get_at((x, 30)) for x in range(10, 131)]

    field.placeholder = ""
    field.placeholder_view.set_text("")
    screen.fill((255, 255, 255))
    field.draw(screen)

    assert [screen.get_at((x, 30)) for x in range(10, 131)] != with_placeholder


def test_placeholder_is_replaced_by_the_typed_text(screen):
    TextView.fonts = {}
    field = InputField((10, 10), (120, 40), color=(210, 210, 210), placeholder="Name")

    screen.fill((255, 255, 255))
    field.draw(screen)
    with_placeholder = [screen.get_at((x, 30)) for x in range(10, 131)]

    field.set_text("Bob")
    screen.fill((255, 255, 255))
    field.draw(screen)

    assert [screen.get_at((x, 30)) for x in range(10, 131)] != with_placeholder


def test_typed_text_is_drawn(screen):
    TextView.fonts = {}
    field = InputField((10, 10), (120, 40), color=(210, 210, 210))
    field.focus()
    field.handle_input(typed("Bob"))
    screen.fill((255, 255, 255))

    field.draw(screen)

    drawn = [screen.get_at((x, 30)) for x in range(18, 60)]

    assert pygame.Color(0, 0, 0) in drawn
