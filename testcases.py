import unittest
from library_system import LibrarySystem
from unittest.mock import patch
import io

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.library_system = LibrarySystem()
        self.library_system.register_member("user1", "1")
        self.library_system.login_member("1")
        self.library_system.add_book("Book One", "Author A", "ISBN001")
        self.library_system.add_book("Book Two", "Author B", "ISBN002")

    def test_register_member(self):
        result = self.library_system.register_member("user2", "2")
        self.assertTrue(result)
        result = self.library_system.register_member("user1", "1")
        self.assertFalse(result)

    def test_login_member(self):
        self.library_system.logout_member()
        result = self.library_system.login_member("1")
        self.assertTrue(result)
        result = self.library_system.login_member("unknown")
        self.assertFalse(result)

    def test_borrow_and_return_book(self):
        result = self.library_system.borrow_book("ISBN001")
        self.assertTrue(result)
        borrowed_books = self.library_system.view_borrowed_books()
        self.assertEqual(len(borrowed_books), 1)
        self.assertEqual(borrowed_books[0].title, "Book One")

        result = self.library_system.return_book("ISBN001")
        self.assertTrue(result)
        borrowed_books = self.library_system.view_borrowed_books()
        self.assertEqual(len(borrowed_books), 0)

    def test_view_available_books(self):
        self.library_system.borrow_book("ISBN001")
        available_books = self.library_system.view_available_books()
        self.assertEqual(len(available_books), 1)
        self.assertEqual(available_books[0].title, "Book Two")

    def test_search_books_by_title(self):
        results = self.library_system.search_books_by_title("One")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Book One")

    def test_view_statistics(self):
        total_books, borrowed_books = self.library_system.view_statistics()
        self.assertEqual(total_books, 2)
        self.assertEqual(borrowed_books, 0)
        self.library_system.borrow_book("ISBN001")
        total_books, borrowed_books = self.library_system.view_statistics()
        self.assertEqual(borrowed_books, 1)

if __name__ == "__main__":
    unittest.main()