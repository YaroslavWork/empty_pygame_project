# Empty Pygame Project

A reusable **pygame** starter template (Python 3.11) with a clean model/view
structure, a pan & zoom camera, and a pytest suite. Fork it and build your game
on top. It is intentionally empty: no game logic, just the scaffold.

## Requirements

- Python 3.11
- Dependencies in `requirements.txt` (pygame)

> Newest version of Python does **not** work: pygame 2.6.1 crashes on `pygame.font` import.

## Setup

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If you work on the code, also install the dev tools:

```bash
pip install -r requirements-dev.txt
```

## Run

```bash
.venv/bin/python main.py
```

Or press **F5** in VS Code (uses `.vscode/launch.json`).

## Controls

The empty camera already supports navigation, so you can see the structure work:

| Key | Action |
|-----|--------|
| `W` / `↑` | Pan up |
| `S` / `↓` | Pan down |
| `A` / `←` | Pan left |
| `D` / `→` | Pan right |
| `E` | Zoom in |
| `Q` | Zoom out |

## Structure

Strict model/view split, one responsibility per class. Each feature lives in its
own package folder.

```
main.py                  entry point, runs the App loop
scripts/
  settings.py            window size, name, FPS, colors
  app.py                 App: orchestrates the frame
  camera/
    model.py             CameraModel  — position, zoom, coordinate math (no pygame)
    view.py              CameraView   — draws the map scale
  field/
    model.py             FieldModel   — game world state (no pygame)
    view.py              FieldView    — draws the world
  UI/
    element.py           UIElement    — base interface for UI elements
    text.py              TextView     — UI element: cached-font text
    button.py            Button       — clickable rect with a TextView label
    ui.py                UI           — owns the elements: update / input / draw
```

### The model/view rule

- **`*Model`** holds state and math only — never imports pygame, never draws.
- **`*View`** reads a model and draws it — never mutates the model.
- **`App`** is the orchestrator. One frame runs four blocks:

  1. `handle_input` — reads mouse, events, keyboard (collects only)
  2. `update_physics` — mutates the models
  3. `render` — draws via the views
  4. `update_display` — flips the display, updates `dt`

### The UI layer

- Every UI element inherits from `UIElement` and implements `update`, `handle_input`,
  `draw` and `reset`. This includes `TextView`, so text is a managed element too.
- `UI` owns the elements and is the only place that updates them, feeds them input
  and draws them. A new element is registered with `ui.add(element)`.
- `App` delegates to it (`ui.handle_input` / `ui.update` / `ui.draw` / `ui.reset`).
  Elements only change their own `hovered` / `clicked` state; `App` still performs the
  actual model change in `update_physics`, so the model/view split stays intact.
- `ui.reset()` clears each element's one-frame input state at the end of the frame, so
  `App` never clears `button.clicked` by hand.
- A `TextView` is created once and its content changed with `set_text` (which re-renders
  the surface) instead of building a new one every frame — see `App.fps_text`.

### Coordinate system

- **Global** coordinates are the world (in meters) — the source of truth.
- **Local** coordinates are screen pixels.

`CameraModel` converts between them with `get_local_point` / `get_global_point`
(and `get_local_radius` / `get_global_radius`). `distance` is how many meters fit
across the window width; a larger `distance` = zoomed out.

## Adding a feature

1. Create a package: `scripts/<feature>/` with `model.py`, `view.py`, `__init__.py`.
2. Put state and math in the `*Model` (no pygame).
3. Put drawing in the `*View` (reads the model only).
4. Wire it into `App`: update in `update_physics`, draw in `render`.
5. Add tests under `tests/`.

## Tests

```bash
.venv/bin/pytest
```

69 tests run headless (`conftest.py` forces `SDL_VIDEODRIVER=dummy`), so they
work in a terminal or CI without a display.

## Conventions

See `RULES.md`.
