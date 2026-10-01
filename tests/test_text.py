import pygame

from scripts.UI.text import TextView


def test_render_creates_surface():
    TextView.fonts = {}

    label = TextView("hello", (0, 0, 0), 20)

    assert label.text_surface.get_width() > 0
    assert label.text_surface.get_height() > 0


def test_font_is_cached_by_size():
    TextView.fonts = {}

    a = TextView("a", (0, 0, 0), 24)
    b = TextView("b", (0, 0, 0), 24)

    assert a.font is b.font
    assert len(TextView.fonts) == 1


def test_different_sizes_use_different_fonts():
    TextView.fonts = {}

    TextView("a", (0, 0, 0), 20)
    TextView("b", (0, 0, 0), 40)

    assert len(TextView.fonts) == 2


def test_print_blits_centered(screen):
    TextView.fonts = {}
    label = TextView("centered", (0, 0, 0), 20)
    screen.fill((255, 255, 255))

    label.print(screen, (160, 120), True)

    assert screen.get_at((160, 120)) != pygame.Color(255, 255, 255)


def test_print_blits_at_top_left(screen):
    TextView.fonts = {}
    label = TextView("x", (0, 0, 0), 20)
    screen.fill((255, 255, 255))

    label.print(screen, (0, 0), False)

    changed = any(
        screen.get_at((x, y)) != pygame.Color(255, 255, 255)
        for x in range(label.text_surface.get_width())
        for y in range(label.text_surface.get_height())
    )
    assert changed
