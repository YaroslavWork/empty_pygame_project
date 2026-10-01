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

## Project facts

- Python 3.11 inside `.venv` (created with `uv`). System Python is 3.14 and
  lacks pygame — always use `.venv`.
- Dependency: `pygame==2.6.1` (see `requirements.txt`).
- Entry point: `main.py` -> `scripts.app.App.update()` loop.
- Run: `.venv/bin/python main.py` (or press F5, which uses `.vscode/launch.json`).

## Workflow

- Before editing, read the files involved. Get latest context first.
- After editing, verify: byte-compile / import check / run headless if possible.
- Prefer small precise edits over rewrites.
- Ask before making structural or behavior-changing decisions I'm unsure about.
- Keep changes scoped to the request; do not reformat unrelated code.
