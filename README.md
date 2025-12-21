# Inspiration Board Backend

This backend create boards and cards, and view or delete them. It uses Flask, PostgreSQL, SQLAlchemy (with Migrate/Alembic), venv, python-dotenv, gunicorn, pytest, and flask_cors.

## What It Does
- Boards are containers (like topics).
- Cards are short messages inside a board.
- One board has many cards. Each card belongs to one board.

## Data Models

Board
- `id`: number
- `title`: required string
- `owner`: required string (from user story)
- `created_at`, `updated_at`: timestamps
- `cards`: list of cards (deleted when board is deleted)

Card
- `id`: number
- `card_message`: required string, up to 40 characters
- `likes`: number (starts at 0)
- `board_id`: number (the board this card belongs to)
- `created_at`, `updated_at`: timestamps

## Validation (Plain Rules)
- Board must have a non-empty `title` and `owner`.
- Card must have a non-empty `card_message` (≤ 40 chars) and a valid `board_id`.
- If input is invalid, return status `400` with JSON: `{ "details": "Invalid data" }`.

## API Endpoints

Boards
- GET `/boards` → list of boards: `[ { id, title, card_count } ]`
- POST `/boards` → create board with `{ title, owner }`, returns `201 { id, title, card_count }`
- GET `/boards/:id` → one board with its cards: `{ id, title, cards: [Card] }`
- DELETE `/boards/:id` → delete a board and its cards, returns `204`
- GET `/boards/:id/cards` → list cards for that board: `[Card]`

Cards
- POST `/cards` → create card with `{ card_message, board_id }`, returns `201 { id, card_message, likes, board_id }`
- GET `/cards/:id` → one card: `{ id, card_message, likes, board_id }`
- PUT `/cards/:id` → update card `{ card_message?, likes? }`, returns updated card
- PATCH `/cards/:id/like` → increase `likes` by 1, returns updated card
- DELETE `/cards/:id` → delete a card, returns `204`

## Error Responses
- Not found → `404 { "message": "Board 1 not found" }` or `404 { "message": "Card 1 not found" }`
- Invalid data → `400 { "details": "Invalid data" }`

## Environment & Setup

Create a `.env` file:
```
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://user:pass@localhost:5432/inspiration_board
SQLALCHEMY_TEST_DATABASE_URI=postgresql+psycopg2://user:pass@localhost:5432/inspiration_board_test
```

Set up venv and install:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Migrations:
```
flask db init   # already present in this repo, skip
flask db migrate -m "init tables"
flask db upgrade
```

Run (development):
```
flask run
```

Run (production):
```
gunicorn "app:create_app()"
```

## Testing
- Tests are in `tests/board` and `tests/card`.
- Run tests:
```
pytest -q
```

## Status Checklist
- [x] Basic CRUD for boards and cards
- [x] Errors for not found and invalid data
- [x] Board↔Card relationship with cascade delete
- [ ] Add `owner` to Board in code and routes
- [ ] Enforce 40-char limit for card messages in routes
- [ ] Implement `GET /boards/:id/cards` and `PATCH /cards/:id/like`
