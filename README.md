# Book Manager CLI

A Python CLI application for managing a personal book collection with metadata, ratings, reading status, and persistent storage.

## Features

- **Add books** — required title with optional author, year, and genre
- **Bulk add** — add multiple books at once by comma-separated titles
- **View all books** — color-coded table (green = read, yellow = unread) with summary stats
- **Advanced search** — by title, author, or genre with 3 modes (contains, starts with, exact match)
- **Edit books** — update title, author, year, or genre interactively
- **Delete books** — remove a book from the collection
- **Rate books** — assign a rating from 1 to 5
- **Toggle read/unread** — flip reading status with one click
- **View by rating** — sort highest or lowest, optionally show unrated books
- **Auto-save** — persists to `books.json` after every action

## Data Schema

| Field    | Type            | Default    | Description                |
|----------|-----------------|------------|----------------------------|
| `title`  | `str`           | *(required)* | Book title               |
| `author` | `str`           | `""`       | Author name                |
| `year`   | `int \| None`   | `None`     | Publication year           |
| `genre`  | `str`           | `""`       | Book genre/category        |
| `rating` | `int \| None`   | `None`     | Rating (1–5)               |
| `status` | `str`           | `"unread"` | Reading status (`read` / `unread`) |
| `id`     | `str`           | UUID (8 chars) | Unique identifier      |

## Menu

```
1. Add a book
2. View all books
3. Search books
4. Edit a book
5. Delete a book
6. Rate a book
7. Toggle read/unread
8. View by rating
9. Add multiple books
10. Exit
```

## Requirements

- **Python 3.10+** — uses `list[type]` and `type | None` syntax
- **No external dependencies** — built entirely with the standard library (`os`, `json`, `dataclasses`, `uuid`, `typing`)

## Usage

```bash
# Start the application
python app.py

# Run tests
python -m unittest test_app.py -v
```
