import os
import json
from dataclasses import dataclass, asdict, field
from uuid import uuid4
from typing import Callable

DATA_FILE = "books.json"

C_CYAN = "\033[36m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_RED = "\033[31m"
C_BOLD = "\033[1m"
C_RESET = "\033[0m"


@dataclass
class Book:
    title: str
    author: str = ""
    year: int | None = None
    genre: str = ""
    rating: int | None = None
    status: str = "unread"
    id: str = field(default_factory=lambda: uuid4().hex[:8])

    def __str__(self) -> str:
        parts = [self.title]
        if self.author:
            parts.append(f"by {self.author}")
        if self.year:
            parts.append(f"({self.year})")
        rating_str = f"{self.rating}/5" if self.rating is not None else "unrated"
        parts.append(f"[{rating_str}, {self.status}]")
        return " ".join(parts)


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause() -> None:
    input(f"\n{C_YELLOW}Press Enter to continue...{C_RESET}")


def save_books(books: list[Book]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([asdict(b) for b in books], f, indent=2, ensure_ascii=False)


def load_books() -> list[Book]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return [Book(**item) for item in data if isinstance(item, dict)]
    except (json.JSONDecodeError, IOError):
        return []


def display_books(books: list[Book], header: str = "Your books:") -> None:
    if not books:
        print(f"{C_YELLOW}No books in the list.{C_RESET}")
        return
    print(f"\n{C_BOLD}{header}{C_RESET}")
    sep = "-" * 95
    print(sep)
    print(f"{'#':<3} {'Title':<30} {'Author':<20} {'Year':<5} {'Genre':<15} {'Rating':<6} {'Status'}")
    print(sep)
    for i, book in enumerate(books, 1):
        rating_str = f"{book.rating}/5" if book.rating is not None else "-"
        year_str = str(book.year) if book.year is not None else "-"
        status_str = f"{'Read' if book.status == 'read' else 'Unread':6}"
        color = C_GREEN if book.status == "read" else C_YELLOW
        line = f"{i:<3} {book.title:<30} {book.author:<20} {year_str:<5} {book.genre:<15} {rating_str:<6} {status_str}"
        print(f"{color}{line}{C_RESET}")
    print(sep)
    total_read = sum(1 for b in books if b.status == "read")
    print(f"{C_CYAN}Total: {len(books)} book(s) — {total_read} read, {len(books) - total_read} unread{C_RESET}")


def add_book(books: list[Book]) -> None:
    title = input("Enter book title: ").strip()
    if not title:
        print(f"{C_RED}Book title cannot be empty.{C_RESET}")
        return
    author = input("Author (optional): ").strip()
    year_str = input("Year (optional): ").strip()
    year = int(year_str) if year_str.isdigit() else None
    if year_str and not year_str.isdigit():
        print(f"{C_YELLOW}Invalid year, ignoring.{C_RESET}")
        year = None
    genre = input("Genre (optional): ").strip()
    book = Book(title=title, author=author, year=year, genre=genre)
    books.append(book)
    print(f'{C_GREEN}"{title}" added successfully.{C_RESET}')


def add_multiple_books(books: list[Book]) -> None:
    titles = input("Enter book titles separated by commas: ").strip()
    if not titles:
        print(f"{C_YELLOW}No titles entered.{C_RESET}")
        return
    titles_list = [t.strip() for t in titles.split(",") if t.strip()]
    for title in titles_list:
        books.append(Book(title=title))
    print(f'{C_GREEN}{len(titles_list)} book(s) added successfully.{C_RESET}')


def view_books(books: list[Book]) -> None:
    display_books(books)


def search_book(books: list[Book]) -> None:
    print(f"\n{C_BOLD}Search by:{C_RESET}")
    print("1. Title")
    print("2. Author")
    print("3. Genre")
    field_choice = input("Choose (1-3): ").strip()
    field_map = {"1": "title", "2": "author", "3": "genre"}
    field = field_map.get(field_choice, "title")
    query = input(f"Enter {field} to search: ").strip().lower()
    if not query:
        print(f"{C_RED}Search query cannot be empty.{C_RESET}")
        return
    print(f"\n{C_BOLD}Search mode:{C_RESET}")
    print("1. Contains (default)")
    print("2. Starts with")
    print("3. Exact match")
    mode = input("Choose (1-3): ").strip()
    attr_lower = lambda b: getattr(b, field).lower()
    if mode == "2":
        found = [b for b in books if attr_lower(b).startswith(query)]
    elif mode == "3":
        found = [b for b in books if attr_lower(b) == query]
    else:
        found = [b for b in books if query in attr_lower(b)]
    if found:
        display_books(found, f"Found ({len(found)}):")
    else:
        print(f"{C_YELLOW}No matching book found.{C_RESET}")


def select_book(books: list[Book], action: str) -> Book | None:
    if not books:
        print(f"{C_YELLOW}No books in the list.{C_RESET}")
        return None
    display_books(books)
    while True:
        try:
            choice = int(input(f"\nEnter the number of the book to {action}: "))
            if 1 <= choice <= len(books):
                return books[choice - 1]
            print(f"{C_RED}Please enter a number between 1 and {len(books)}.{C_RESET}")
        except ValueError:
            print(f"{C_RED}Please enter a valid number.{C_RESET}")


def delete_book(books: list[Book]) -> None:
    book = select_book(books, "delete")
    if book:
        books.remove(book)
        print(f'{C_GREEN}"{book.title}" deleted successfully.{C_RESET}')


def edit_book(books: list[Book]) -> None:
    book = select_book(books, "edit")
    if not book:
        return
    while True:
        print(f"\n{C_BOLD}Editing:{C_RESET} {book}")
        print("1. Edit title")
        print("2. Edit author")
        print("3. Edit year")
        print("4. Edit genre")
        print("5. Done")
        choice = input("Choose (1-5): ").strip()
        if choice == "1":
            new_val = input(f"New title [{book.title}]: ").strip()
            if new_val:
                book.title = new_val
                print(f"{C_GREEN}Title updated.{C_RESET}")
            else:
                print(f"{C_RED}Title cannot be empty.{C_RESET}")
        elif choice == "2":
            new_val = input(f"New author [{book.author}]: ").strip()
            book.author = new_val
            print(f"{C_GREEN}Author updated.{C_RESET}")
        elif choice == "3":
            new_val = input(f"New year [{book.year or ''}]: ").strip()
            if new_val:
                try:
                    book.year = int(new_val)
                    print(f"{C_GREEN}Year updated.{C_RESET}")
                except ValueError:
                    print(f"{C_RED}Invalid year.{C_RESET}")
            else:
                book.year = None
                print(f"{C_GREEN}Year cleared.{C_RESET}")
        elif choice == "4":
            new_val = input(f"New genre [{book.genre}]: ").strip()
            book.genre = new_val
            print(f"{C_GREEN}Genre updated.{C_RESET}")
        elif choice == "5":
            print(f'{C_GREEN}"{book.title}" updated.{C_RESET}')
            return
        else:
            print(f"{C_RED}Invalid choice.{C_RESET}")


def rate_book(books: list[Book]) -> None:
    book = select_book(books, "rate")
    if not book:
        return
    while True:
        try:
            rating = int(input(f'Enter rating for "{book.title}" (1-5): '))
            if 1 <= rating <= 5:
                book.rating = rating
                print(f'{C_GREEN}"{book.title}" rated {rating}/5.{C_RESET}')
                return
            print(f"{C_RED}Rating must be between 1 and 5.{C_RESET}")
        except ValueError:
            print(f"{C_RED}Please enter a valid number.{C_RESET}")


def toggle_read(books: list[Book]) -> None:
    book = select_book(books, "toggle read status")
    if not book:
        return
    book.status = "read" if book.status == "unread" else "unread"
    status_text = f"{C_GREEN}Read{C_RESET}" if book.status == "read" else f"{C_YELLOW}Unread{C_RESET}"
    print(f'"{book.title}" marked as {status_text}.')


def view_by_rating(books: list[Book]) -> None:
    rated = [b for b in books if b.rating is not None]
    unrated = [b for b in books if b.rating is None]
    if not rated:
        print(f"{C_YELLOW}No rated books yet.{C_RESET}")
        if unrated:
            show = input(f"\nShow {len(unrated)} unrated book(s)? (y/n): ").strip().lower()
            if show == "y":
                display_books(unrated, "Unrated books:")
        return
    print(f"\n{C_BOLD}Sort by:{C_RESET}")
    print("1. Highest rated first")
    print("2. Lowest rated first")
    sort_choice = input("Choose (1-2): ").strip()
    reverse = sort_choice != "2"
    sorted_books = sorted(rated, key=lambda b: b.rating, reverse=reverse)
    display_books(sorted_books, "Rated books:")
    if unrated:
        show = input(f"\nShow {len(unrated)} unrated book(s)? (y/n): ").strip().lower()
        if show == "y":
            display_books(unrated, "Unrated books:")


menu_items: dict[str, tuple[str, Callable | None]] = {
    "1": ("Add a book", add_book),
    "2": ("View all books", view_books),
    "3": ("Search books", search_book),
    "4": ("Edit a book", edit_book),
    "5": ("Delete a book", delete_book),
    "6": ("Rate a book", rate_book),
    "7": ("Toggle read/unread", toggle_read),
    "8": ("View by rating", view_by_rating),
    "9": ("Add multiple books", add_multiple_books),
    "10": ("Exit", None),
}


def show_menu(book_count: int) -> None:
    clear_screen()
    print(f"\n{C_BOLD}{C_CYAN}--- Book Manager ---{C_RESET}")
    print(f"Books: {book_count}")
    for key, (label, _) in menu_items.items():
        print(f"  {key}. {label}")


def main() -> None:
    books: list[Book] = load_books()
    while True:
        show_menu(len(books))
        choice = input(f"Choose an option (1-{len(menu_items)}): ").strip()
        if choice not in menu_items:
            print(f"{C_RED}Invalid choice. Please enter a number between 1 and {len(menu_items)}.{C_RESET}")
            pause()
            continue
        _, func = menu_items[choice]
        if func is None:
            save_books(books)
            print(f"{C_GREEN}Books saved. Goodbye!{C_RESET}")
            break
        func(books)
        save_books(books)
        pause()


if __name__ == "__main__":
    main()
