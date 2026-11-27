# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A UI test suite (pytest + Playwright, sync API, Python) for the **live production site** https://backpack.exchange. No app code lives here. It is a public portfolio project: every line must be clear enough for the owner to explain in an interview.

## Hard rules

- Public pages only. Never log in, never use real credentials.
- Clicking the "Log in" and "Sign up" navigation links is allowed: they only open `/login` and `/signup`. Never click the "Log in" or "Open account" submit buttons.
- Fake data lives only in `tests/data.py` (example.com email). It is typed into forms, never submitted.
- Run tests gently: no loops or repeated runs against the live site.
- Never run `git push` and never commit to `main`. Work on a branch; the human reviews every diff before committing.
- Don't change `.github/workflows/`, `Dockerfile`, `requirements.txt`, `requirements-dev.txt` or `ruff.toml` unless asked.

## Browser exploration (Playwright MCP)

- Use a 1280x720 viewport. A narrow window shows the mobile layout, which our tests don't cover.
- Read the page with the accessibility snapshot, not with JavaScript. The snapshot shows the roles and names our locators use.
- Only open and read pages. Never click anything that trades, logs in or creates an account.
- When the exploration is finished, always close the browser with `browser_close`. Don't leave it running.

## Test design

- Before writing a test, list its cases and name the technique used: equivalence partitioning, boundary values, decision table, state transition, error guessing, or use case testing. Show this list in the plan for review first.
- Pick the technique that fits: a form with several inputs → decision table; a value with limits → boundary values; tabs, menus or open/closed states → state transition; following a link to another page → use case testing. If no technique fits (e.g. a page simply opens), say so honestly instead of forcing a label.
- One behaviour per test. Check the "before" state too when a test checks a change (e.g. a menu is hidden before it opens).
- Name the technique in the comment above the test, for example: `# Decision table: email filled, password empty -> button disabled`.
- Use `pytest.mark.parametrize` when several cases share the same steps.
- After writing or changing code, run `ruff check --fix .` and `ruff format .` first, then run only the changed test file once (`pytest <file> -v`) and report the result. Never re-run the whole suite in a loop.

## Commands

Local (venv in `.venv/`, Windows):
- Install: `pip install -r requirements-dev.txt` (includes `requirements.txt`) then `playwright install chromium`
- All tests: `pytest`
- Smoke suite (what CI runs): `pytest -m smoke -v`
- Regression suite (P2 and P3, not in CI yet): `pytest -m regression -v`
- Single test: `pytest tests/test_login_page.py::test_login_form_is_visible`
- Watch the browser: add `--headed` (and `--slowmo 500` if needed)

Lint and format (Ruff, settings in `ruff.toml`, line length 120; CI fails if these fail):
- Lint and auto-fix: `ruff check --fix .`
- Format: `ruff format .`
- Check only, change nothing (what CI runs): `ruff check .` and `ruff format --check .`

Docker (same image as CI):
- `docker build -t backpack-ui-tests .`
- `docker run --rm --ipc=host -v "${PWD}/test-results:/app/test-results" backpack-ui-tests`

On failure, traces and screenshots go to `test-results/` (configured in `pytest.ini`). Open a trace with `playwright show-trace <path>/trace.zip`.

## Architecture

- `pytest.ini` sets `base_url`, so page paths are relative (`/login`), and `pythonpath = .`, so `pages` and `tests` import from the repo root.
- `pages/base_page.py`: `BasePage` holds the Playwright `page`; `open()` calls `goto(self.PATH, wait_until="domcontentloaded")`. Don't wait for full load: the site streams charts and live data.
- Page objects (`pages/*_page.py`) subclass `BasePage` and set `PATH`: as a class attribute for a fixed page (`LoginPage`), or in `__init__` when the address depends on a parameter (`TradePage(page, market="SOL_USD_PERP")`). Larger pages are made of components in `pages/components/` (plain classes taking `page`, not `BasePage` subclasses). Example: `TradePage` has `order_book` and `order_form`.
- Locators are defined as attributes in `__init__` (lazy; nothing is searched yet). Tests call `expect(...)` on them directly. Page-object methods only perform user actions (`fill_form`, `open_trade_menu`); assertions stay in tests.
- `conftest.py` provides fixtures (`landing_page`, `login_page`, `signup_page`, `markets_page`, `trade_page`) that build the page object and already open it. It also raises the global `expect` timeout to 10 s.
- Tests mark the whole module with `pytestmark`: `pytest.mark.smoke` for P1 user paths (run in CI), `pytest.mark.regression` for P2 and P3 checks (new files, not run in CI yet).

## Conventions and gotchas

- Locator style: prefer `get_by_role` / `get_by_label` with `exact=True`. Scope to a container (`header`, `main`, or a component `root`) when the same text appears twice on the page (e.g. two "Sign up" buttons). For elements without stable ids, describe them by content (see `OrderBook.root`) and match numbers by regex pattern, never by live values.
- `to_be_hidden()` also passes when the element doesn't exist. To prove something is absent, use `to_have_count(0)`; to prove a locator is right, also check it is visible in some state.
- Region differences: the CI runners are in the US, and Backpack shows US visitors a different landing page (no Stocks, shorter descriptions). Assert only on text common to all regions.
- A contains-match without `exact=True` is allowed only on purpose, with a comment saying why (see `LandingHeader.trade_menu_perpetuals`).
- Version pinning: `playwright` in `requirements.txt` must match the Docker base image tag in `Dockerfile` (`mcr.microsoft.com/playwright/python:vX.Y.Z-noble`). Bump them together. Ruff is pinned in `requirements-dev.txt`.
- Code style: a short comment above every test, fixture and method, and a docstring for every class, explaining *what* and *why* in plain English. Layout and import order are left to Ruff.
- CI (`.github/workflows/ui-tests.yml`) has two jobs on every push and PR to `main`: `lint` (Ruff) and `smoke` (builds the Docker image and runs the smoke suite). Failure artifacts are uploaded for 7 days.