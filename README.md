# 📚 Book Manager CLI

> 🖥️ A terminal app to manage your personal book collection — add, search, rate, and track reading status. Zero external dependencies.

---

## 📖 Manage
**Full control over your library from the terminal.** Add books with a required title and optional author, year, and genre. Add multiple books at once by comma-separated titles. Edit any field later, or delete what you don't need.

## 🔍 Search
**Find any book in seconds.** Search by title, author, or genre — with 3 modes: contains, starts with, or exact match.

## ⭐ Rate
**Remember your opinion on every book.** Rate from 1 to 5, sort highest or lowest, and see which books you haven't rated yet. Toggle reading status between "read" and "unread" with one click.

## 🎨 Display
**Your library, beautifully presented.** A color-coded table — green for read, yellow for unread — with quick stats: how many books you've read and how many remain.

## 💾 Save
**Automatic safety.** Everything is saved to a JSON file after every action — and loaded automatically when you start the app. No manual "Save" button needed.

---

## 🚀 Get started

```bash
git clone https://github.com/redajabar-404/Book-manager.git
cd Book-manager
python app.py
```

**📌 Requirements:** Python 3.10+ only — no `pip install` needed.

### Menu

```
1. Add a book          6. Rate a book
2. View all books      7. Toggle read/unread
3. Search books        8. View by rating
4. Edit a book         9. Add multiple books
5. Delete a book       10. Exit
```

## ✅ Run tests

```bash
python -m unittest test_app.py -v
```

40 tests covering every function in the app — all passing.

## 🧰 Tech stack

`dataclasses` · `json` · `uuid` · `typing` · `unittest` — all from the Python standard library, zero external dependencies.

## 📜 License

[MIT](LICENSE) — use, modify, and distribute freely.

---

⭐ **If you like this project, don't forget to star it — it keeps us motivated to add more features!**
