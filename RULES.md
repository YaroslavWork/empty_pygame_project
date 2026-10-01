# Rules for AI assistant (SpaceMan)

Rules I follow when editing this project. Keep them in sync with the codebase.

## Comments

- Do not write obvious or unnecessary comments. Code should explain itself.
- No comments that restate the code (`i += 1  # increment i`), no banner noise.
- Keep only comments that add information the code cannot: non-obvious math,
  "why" decisions, external constraints, or a `#`-explanation the author left.
- When I fix or change something, show only what I changed — no drive-by
  re-comments, no re-formatting of untouched lines.
- Do not add docstrings to trivial functions.

## Code style

- Match the existing style: 4-space indent, `-> None` return hints, type hints
  on params where the author uses them.
- Keep the author's naming conventions (`CameraModel`, `CameraView`, `get_*`,
  `update_*`).
- Preserve existing behavior unless asked to change it. Never silently "fix"
  logic that looks wrong — flag it instead.
- Two blank lines between top-level classes/functions; imports grouped
  `pygame` / project.

## Architecture

- Follow the existing model/view split. Data model (`*Model`) has no pygame and
  no drawing. View (`*View`) reads the model, never mutates it.
- One class per responsibility, one file per class where practical.
- `App` stays the orchestrator: `handle_input` collects input only,
  `update_physics` mutates the model, `render` draws, `update_display` flips.
- New features live in their own package folder (`scripts/<feature>/model.py`,
  `view.py`, `__init__.py`).

## Tests

- Framework: `pytest`. Tests live in `tests/` and mirror the package layout
  (`test_camera_model.py`, `test_app.py`, ...).
- Run: `.venv/bin/pytest` (or `.venv/bin/python -m pytest`). Config in `pytest.ini`.
- Tests run headless: `conftest.py` sets `SDL_VIDEODRIVER=dummy` /
  `SDL_AUDIODRIVER=dummy` and adds the project root to `sys.path`. Do not require
  a real display.
- Test behavior, not implementation details. Prefer clear function names
  (`test_move_right_increases_x`) over docstrings/comments.
- Use `pytest.approx` for float comparisons, never exact `==` on floats.
- Keep model tests free of pygame; only view/render tests touch a screen fixture.
- When a test reveals wrong behavior, do not silently fix the code — flag it and
  ask before changing behavior (see Code style).
- When fixing a flagged bug, update the test that documented it to assert the
  corrected behavior.
- Every new feature/class should get tests. Verify the suite still passes before
  finishing.

## Project facts

- Python 3.11 inside `.venv`.
- Dependency: see `requirements.txt` and `requirements-dev.txt`.
- Entry point: `main.py` -> `scripts.app.App.update()` loop.
- Run: `.venv/bin/python main.py` (or press F5, which uses `.vscode/launch.json`).
- Run a server: `.venv/bin/python main.py --server`.
- Join a server: `.venv/bin/python main.py --connect HOST:PORT`.
- Networking: `App` talks to a `scripts.net.client.Client` (`LocalClient` for
  singleplayer, `NetClient` over TCP). The server owns the authoritative
  `WorldModel`; clients send intents and apply snapshots.

## Workflow

- Before editing, read the files involved. Get latest context first.
- After editing, verify: byte-compile / import check / run headless if possible.
- Prefer small precise edits over rewrites.
- Ask before making structural or behavior-changing decisions I'm unsure about.
- Keep changes scoped to the request; do not reformat unrelated code.
