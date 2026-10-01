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

## Multiplayer

The same `App` runs solo and online — it only ever talks to a `Client`
interface (`scripts/net/client.py`). Singleplayer uses an in-process
`LocalClient`; online uses a `NetClient` over TCP while the server owns the
authoritative `WorldModel` and broadcasts snapshots.

```bash
# host (authoritative server)
.venv/bin/python main.py --server

# join from another terminal / machine
.venv/bin/python main.py --connect 127.0.0.1:5000
```

Host, port and buffer size come from `scripts/settings.py` (`NET_HOST`,
`NET_PORT`, `NET_BUFFER_SIZE`). Intents are plain action strings (`"left"`,
`"right"`, `"up"`, `"down"`, `"zoom_in"`, `"zoom_out"`) sent as length-prefixed
JSON frames.

Every connection gets its own player: the server keeps a player per client and
broadcasts all of them in the snapshot, so both windows see each other's
rectangles move independently. The camera stays shared and `Q` / `E` zoom it.
Players are removed from the world when a client disconnects.

### Motion smoothing (interpolation)

The server only steps the world at its own tick rate, so snapshots arrive in
coarse jumps. To keep motion smooth, each `PlayerModel` tracks two positions:

- `x` / `y` — the **authoritative** position from the snapshot (the source of truth).
- `render_x` / `render_y` — the **drawn** position, smoothed toward `x` / `y` every frame.

`PlayerModel.interpolate` closes the gap by a frame-rate-safe fraction
(`s.PLAYER_INTERPOLATION_SPEED`, `blend = min(1, speed * dt / 1000)`), and
`PlayerView` draws `render_x` / `render_y`. `App.update_physics` calls
`world.interpolate_players(dt)` after applying the snapshot, so at a high frame
rate the rectangle glides between the lower-rate server updates instead of
snapping. A faster `PLAYER_INTERPOLATION_SPEED` reacts quicker (snappier/more
jitter); a slower one glides more (smoother/laggier).

### Two windows on one machine

Run the server and two clients in three terminals:

```bash
# terminal 1 — authoritative server
.venv/bin/python main.py --server

# terminal 2 — first client
.venv/bin/python main.py --connect 127.0.0.1:5000

# terminal 3 — second client
.venv/bin/python main.py --connect 127.0.0.1:5000
```

Two windows open, each showing a differently-coloured player rectangle. Move
with `WASD` in one window and you will see the other window update that
rectangle in real time — that is the server relaying both players. (Each client
is a full pygame window; run them as separate OS processes, not threads, so each
owns its own event loop and display.)

## Settings

All tunables and static values live in `scripts/settings.py`: window size and
name, FPS, colors, camera start values and speeds, the map-scale/HUD layout, and
the network defaults. Import it anywhere with `from scripts import settings as s`.
There are no magic numbers in feature code — change behavior through settings.

## Controls

`WASD` moves **your player** (a random-coloured rectangle); `Q` / `E` zoom the
camera. Your player is the same entity solo and online. Move speed is
`PLAYER_MOVE_SPEED` (meters per second) in `scripts/settings.py`.

| Key | Action |
|-----|--------|
| `W` / `↑` | Move player up |
| `S` / `↓` | Move player down |
| `A` / `←` | Move player left |
| `D` / `→` | Move player right |
| `E` | Zoom in |
| `Q` | Zoom out |

## Structure

Strict model/view split, one responsibility per class. Each feature lives in its
own package folder.

```
main.py                  entry point, runs the App loop (--server / --connect)
scripts/
  settings.py            window, colors, player/camera/HUD/scale, network defaults
  app.py                 App: orchestrates the frame, talks to a Client
  world.py               WorldModel — owns the models, step/snapshot (no pygame)
  camera/
    model.py             CameraModel  — position, zoom, coordinate math (no pygame)
    view.py              CameraView   — draws the map scale
  field/
    model.py             FieldModel   — game world state (no pygame)
    view.py              FieldView    — draws the world
  player/
    model.py             PlayerModel  — position, random color, movement + interpolation (no pygame)
    view.py              PlayerView   — draws a player rectangle
  net/
    protocol.py          length-prefixed JSON framing
    client.py            Client / LocalClient / NetClient
    server.py            authoritative asyncio server
  UI/
    text.py              TextView     — cached-font text rendering
```

### The model/view rule

- **`*Model`** holds state and math only — never imports pygame, never draws.
- **`*View`** reads a model and draws it — never mutates the model.
- **`App`** is the orchestrator. One frame runs four blocks:

  1. `handle_input` — reads mouse, events, keyboard, collects intents
  2. `update_physics` — sends intents to the `Client`, applies the snapshot
  3. `render` — draws via the views
  4. `update_display` — flips the display, updates `dt`

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
4. Add the tunables to `scripts/settings.py` and read them via `s.NAME`.
5. Wire it into `App`: update in `update_physics`, draw in `render`.
6. Add tests under `tests/`.

## Tests

```bash
.venv/bin/pytest
```

131 tests run headless (`conftest.py` forces `SDL_VIDEODRIVER=dummy`), so they
work in a terminal or CI without a display.

## Conventions

See `RULES.md`.
