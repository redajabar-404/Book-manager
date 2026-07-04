import unittest
import json
import os
import tempfile
from unittest.mock import patch
from io import StringIO

from app import Book, display_books, save_books, load_books, select_book, add_book, delete_book, rate_book, toggle_read, edit_book, search_book, view_by_rating, DATA_FILE, C_RESET


class TestBook(unittest.TestCase):
    def test_create_default(self):
        b = Book(title="Test")
        self.assertEqual(b.title, "Test")
        self.assertEqual(b.author, "")
        self.assertIsNone(b.year)
        self.assertEqual(b.genre, "")
        self.assertIsNone(b.rating)
        self.assertEqual(b.status, "unread")
        self.assertTrue(len(b.id) == 8)

    def test_create_full(self):
        b = Book(title="Test", author="Author", year=2020, genre="Fiction", rating=4, status="read")
        self.assertEqual(b.title, "Test")
        self.assertEqual(b.author, "Author")
        self.assertEqual(b.year, 2020)
        self.assertEqual(b.genre, "Fiction")
        self.assertEqual(b.rating, 4)
        self.assertEqual(b.status, "read")

    def test_str_with_all_fields(self):
        b = Book(title="Test", author="Author", year=2020, rating=4, status="read")
        s = str(b)
        self.assertIn("Test", s)
        self.assertIn("Author", s)
        self.assertIn("2020", s)
        self.assertIn("4/5", s)
        self.assertIn("read", s)

    def test_str_minimal(self):
        b = Book(title="Only Title")
        s = str(b)
        self.assertIn("Only Title", s)
        self.assertIn("unrated", s)
        self.assertIn("unread", s)


class TestSaveLoad(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.orig_data_file = DATA_FILE
        import app
        app.DATA_FILE = os.path.join(self.tmpdir, "books.json")

    def tearDown(self):
        import app
        app.DATA_FILE = self.orig_data_file

    def test_save_and_load_empty(self):
        save_books([])
        loaded = load_books()
        self.assertEqual(loaded, [])

    def test_save_and_load_books(self):
        books = [Book(title="A"), Book(title="B", author="X", year=2000, genre="G", rating=3, status="read")]
        save_books(books)
        loaded = load_books()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].title, "A")
        self.assertEqual(loaded[1].title, "B")
        self.assertEqual(loaded[1].author, "X")
        self.assertEqual(loaded[1].year, 2000)
        self.assertEqual(loaded[1].genre, "G")
        self.assertEqual(loaded[1].rating, 3)
        self.assertEqual(loaded[1].status, "read")

    def test_load_missing_file(self):
        loaded = load_books()
        self.assertEqual(loaded, [])

    def test_load_corrupted_json(self):
        with open(os.path.join(self.tmpdir, "books.json"), "w") as f:
            f.write("invalid json")
        loaded = load_books()
        self.assertEqual(loaded, [])

    def test_id_preserved_across_save_load(self):
        b = Book(title="Test")
        original_id = b.id
        save_books([b])
        loaded = load_books()
        self.assertEqual(loaded[0].id, original_id)


class TestDisplayBooks(unittest.TestCase):
    def test_empty_list(self):
        out = StringIO()
        with patch("sys.stdout", out):
            display_books([])
        self.assertIn("No books", out.getvalue())

    def test_with_books(self):
        books = [Book(title="A", rating=4), Book(title="B", status="read")]
        out = StringIO()
        with patch("sys.stdout", out):
            display_books(books)
        val = out.getvalue()
        self.assertIn("A", val)
        self.assertIn("B", val)
        self.assertIn("Total:", val)

    def test_custom_header(self):
        out = StringIO()
        with patch("sys.stdout", out):
            display_books([Book(title="X")], header="Custom:")
        self.assertIn("Custom:", out.getvalue())


class TestSelectBook(unittest.TestCase):
    def test_empty_list_returns_none(self):
        out = StringIO()
        with patch("sys.stdout", out):
            result = select_book([], "test")
        self.assertIsNone(result)
        self.assertIn("No books", out.getvalue())

    def test_valid_selection(self):
        books = [Book(title="First"), Book(title="Second")]
        with patch("builtins.input", return_value="2"):
            result = select_book(books, "test")
        self.assertIs(result, books[1])

    def test_invalid_then_valid(self):
        books = [Book(title="First"), Book(title="Second")]
        with patch("builtins.input", side_effect=["0", "abc", "2"]):
            result = select_book(books, "test")
        self.assertIs(result, books[1])


class TestAddBook(unittest.TestCase):
    def test_add_valid_title(self):
        books = []
        with patch("builtins.input", side_effect=["My Book", "", "", ""]):
            add_book(books)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "My Book")

    def test_empty_title_rejected(self):
        books = []
        with patch("builtins.input", return_value="  "):
            add_book(books)
        self.assertEqual(len(books), 0)

    def test_add_with_metadata(self):
        books = []
        with patch("builtins.input", side_effect=["Full Book", "Author Name", "2020", "Fiction"]):
            add_book(books)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].author, "Author Name")
        self.assertEqual(books[0].year, 2020)
        self.assertEqual(books[0].genre, "Fiction")

    def test_invalid_year_ignored(self):
        books = []
        with patch("builtins.input", side_effect=["Book", "", "abc", ""]):
            add_book(books)
        self.assertIsNone(books[0].year)


class TestDeleteBook(unittest.TestCase):
    def test_delete_existing(self):
        books = [Book(title="First"), Book(title="Second")]
        with patch("builtins.input", return_value="1"):
            delete_book(books)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Second")


class TestRateBook(unittest.TestCase):
    def test_rate_valid(self):
        books = [Book(title="RateMe")]
        with patch("builtins.input", side_effect=["1", "4"]):
            rate_book(books)
        self.assertEqual(books[0].rating, 4)

    def test_rate_invalid_then_valid(self):
        books = [Book(title="RateMe")]
        with patch("builtins.input", side_effect=["1", "0", "6", "3"]):
            rate_book(books)
        self.assertEqual(books[0].rating, 3)


class TestToggleRead(unittest.TestCase):
    def test_toggle_unread_to_read(self):
        books = [Book(title="ToggleMe")]
        self.assertEqual(books[0].status, "unread")
        with patch("builtins.input", return_value="1"):
            toggle_read(books)
        self.assertEqual(books[0].status, "read")

    def test_toggle_read_to_unread(self):
        books = [Book(title="ToggleMe", status="read")]
        with patch("builtins.input", return_value="1"):
            toggle_read(books)
        self.assertEqual(books[0].status, "unread")


class TestEditBook(unittest.TestCase):
    def test_edit_title(self):
        books = [Book(title="OldTitle")]
        with patch("builtins.input", side_effect=["1", "1", "NewTitle", "5"]):
            edit_book(books)
        self.assertEqual(books[0].title, "NewTitle")

    def test_edit_author(self):
        books = [Book(title="EditMe")]
        with patch("builtins.input", side_effect=["1", "2", "NewAuthor", "5"]):
            edit_book(books)
        self.assertEqual(books[0].author, "NewAuthor")

    def test_edit_year(self):
        books = [Book(title="EditMe")]
        with patch("builtins.input", side_effect=["1", "3", "1999", "5"]):
            edit_book(books)
        self.assertEqual(books[0].year, 1999)

    def test_edit_genre(self):
        books = [Book(title="EditMe")]
        with patch("builtins.input", side_effect=["1", "4", "Science", "5"]):
            edit_book(books)
        self.assertEqual(books[0].genre, "Science")

    def test_done_without_changes(self):
        books = [Book(title="EditMe")]
        with patch("builtins.input", side_effect=["1", "5"]):
            edit_book(books)
        self.assertEqual(books[0].title, "EditMe")


class TestSearchBook(unittest.TestCase):
    def test_search_by_title_contains(self):
        books = [Book(title="The Great Gatsby"), Book(title="1984"), Book(title="Great Expectations")]
        with patch("builtins.input", side_effect=["1", "great", "1"]):
            out = StringIO()
            with patch("sys.stdout", out):
                search_book(books)
        self.assertIn("Great Gatsby", out.getvalue())
        self.assertIn("Great Expectations", out.getvalue())
        self.assertNotIn("1984", out.getvalue())

    def test_search_by_exact_match(self):
        books = [Book(title="The Great Gatsby"), Book(title="1984")]
        with patch("builtins.input", side_effect=["1", "1984", "3"]):
            out = StringIO()
            with patch("sys.stdout", out):
                search_book(books)
        self.assertIn("1984", out.getvalue())

    def test_search_by_author(self):
        books = [Book(title="Book A", author="Orwell"), Book(title="Book B", author="Huxley")]
        with patch("builtins.input", side_effect=["2", "orwell", "1"]):
            out = StringIO()
            with patch("sys.stdout", out):
                search_book(books)
        val = out.getvalue()
        self.assertIn("Book A", val)
        self.assertNotIn("Book B", val)

    def test_search_by_genre(self):
        books = [Book(title="Book A", genre="Dystopian"), Book(title="Book B", genre="Fantasy")]
        with patch("builtins.input", side_effect=["3", "fantasy", "3"]):
            out = StringIO()
            with patch("sys.stdout", out):
                search_book(books)
        val = out.getvalue()
        self.assertIn("Book B", val)
        self.assertNotIn("Book A", val)

    def test_no_match(self):
        books = [Book(title="The Great Gatsby")]
        with patch("builtins.input", side_effect=["1", "nonexistent", "1"]):
            out = StringIO()
            with patch("sys.stdout", out):
                search_book(books)
        self.assertIn("No matching book", out.getvalue())

    def test_empty_query(self):
        books = [Book(title="A")]
        with patch("builtins.input", side_effect=["1", ""]):
            out = StringIO()
            with patch("sys.stdout", out):
                search_book(books)
        self.assertIn("cannot be empty", out.getvalue())


class TestViewByRating(unittest.TestCase):
    def test_no_rated_books(self):
        books = [Book(title="A"), Book(title="B")]
        out = StringIO()
        with patch("sys.stdout", out):
            with patch("builtins.input", return_value="n"):
                view_by_rating(books)
        self.assertIn("No rated books", out.getvalue())

    def test_sorted_highest_first(self):
        books = [Book(title="Alpha", rating=2), Book(title="Bravo", rating=5), Book(title="Charlie", rating=3)]
        out = StringIO()
        with patch("sys.stdout", out):
            with patch("builtins.input", side_effect=["1", "n"]):
                view_by_rating(books)
        val = out.getvalue()
        pos_bravo = val.index("Bravo")
        pos_charlie = val.index("Charlie")
        pos_alpha = val.index("Alpha")
        self.assertLess(pos_bravo, pos_charlie)
        self.assertLess(pos_charlie, pos_alpha)

    def test_sorted_lowest_first(self):
        books = [Book(title="Alpha", rating=2), Book(title="Bravo", rating=5), Book(title="Charlie", rating=3)]
        out = StringIO()
        with patch("sys.stdout", out):
            with patch("builtins.input", side_effect=["2", "n"]):
                view_by_rating(books)
        val = out.getvalue()
        pos_alpha = val.index("Alpha")
        pos_charlie = val.index("Charlie")
        pos_bravo = val.index("Bravo")
        self.assertLess(pos_alpha, pos_charlie)
        self.assertLess(pos_charlie, pos_bravo)


class TestAddMultipleBooks(unittest.TestCase):
    def test_add_multiple(self):
        books = []
        with patch("builtins.input", return_value="A, B, C"):
            add_book_func = __import__("app").add_multiple_books
            add_book_func(books)
        self.assertEqual(len(books), 3)
        self.assertEqual(books[0].title, "A")
        self.assertEqual(books[1].title, "B")
        self.assertEqual(books[2].title, "C")

    def test_empty_input(self):
        books = [Book(title="Existing")]
        with patch("builtins.input", return_value=""):
            add_book_func = __import__("app").add_multiple_books
            add_book_func(books)
        self.assertEqual(len(books), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
