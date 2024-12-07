import unittest
from library_system import LibrarySystem
from unittest.mock import patch
import io

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.library_system = LibrarySystem()
        self.library_system.register_member("user1", "1")
        self.library_system.login_member("1")
        # Add books with the new 'category' argument
        self.library_system.add_book("Book One", "Author A", "ISBN001", "Fiction")
        self.library_system.add_book("Book Two", "Author B", "ISBN002", "Science")

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

    def test_logout_member(self):
        self.library_system.logout_member()
        self.assertIsNone(self.library_system.logged_in_member)
    
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

    def test_borrow_unavailable_book(self):
        self.library_system.borrow_book("ISBN001")
        result = self.library_system.borrow_book("ISBN001")
        self.assertFalse(result)

    def test_return_non_borrowed_book(self):
        result = self.library_system.return_book("ISBN002")
        self.assertFalse(result)

    def test_view_available_books(self):
        self.library_system.borrow_book("ISBN001")
        available_books = self.library_system.view_available_books()
        self.assertEqual(len(available_books), 1)
        self.assertEqual(available_books[0].title, "Book Two")

    def test_search_books_by_title(self):
        results = self.library_system.search_books_by_title("One")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Book One")

        # Test with no results expected
        results = self.library_system.search_books_by_title("Nonexistent")
        self.assertEqual(len(results), 0)

    def test_view_statistics(self):
        total_books, borrowed_books = self.library_system.view_statistics()
        self.assertEqual(total_books, 2)
        self.assertEqual(borrowed_books, 0)
        
        self.library_system.borrow_book("ISBN001")
        total_books, borrowed_books = self.library_system.view_statistics()
        self.assertEqual(borrowed_books, 1)

    def test_view_all_members(self):
        self.library_system.register_member("user3", "3")
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            self.library_system.view_all_members()
            output = mock_stdout.getvalue()
            self.assertIn("user1", output)
            self.assertIn("user3", output)

    def test_double_registration_attempt(self):
        result = self.library_system.register_member("user2", "1")
        self.assertFalse(result)

    def test_search_with_special_characters(self):
        self.library_system.add_book("C++ Primer", "Author C", "ISBN003", "Technology")
        results = self.library_system.search_books_by_title("C++")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "C++ Primer")

    def test_add_and_search_books(self):
        self.library_system.add_book("Advanced Python", "Author D", "ISBN004", "Technology")
        found_books = self.library_system.search_books_by_title("Python")
        self.assertTrue(any(book.title == "Advanced Python" for book in found_books))

    def test_borrow_nonexistent_book(self):
        result = self.library_system.borrow_book("NONEXISTENTISBN")
        self.assertFalse(result)

    def test_return_nonexistent_book(self):
        self.library_system.login_member("1")
        result = self.library_system.return_book("NONEXISTENTISBN")
        self.assertFalse(result)

    def test_borrow_book_when_no_member_logged_in(self):
        self.library_system.logout_member()
        result = self.library_system.borrow_book("ISBN001")
        self.assertFalse(result)

    def test_return_book_when_no_member_logged_in(self):
        self.library_system.logout_member()
        result = self.library_system.return_book("ISBN001")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()