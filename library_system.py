import datetime

# Models
class Member:
    def __init__(self, username, member_id):
        self.username = username
        self.member_id = member_id
        self.borrowed_books = []
        
        # Register the date when the member joined
        self.date_joined = datetime.datetime.now()

    def __repr__(self):
        return f"Member(username={self.username}, member_id={self.member_id})"
        
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.borrower = None
        self.date_borrowed = None

    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, isbn={self.isbn})"

# Library System
class LibrarySystem:
    def __init__(self):
        self.members = {}
        self.books = []
        self.logged_in_member = None

    # Register a new library member
    def register_member(self, username, member_id):
        if member_id in self.members:
            print(f"Member ID {member_id} already exists.")
            return False
        self.members[member_id] = Member(username, member_id)
        print(f"Member {username} registered successfully.")
        return True

    # Login an existing library member
    def login_member(self, member_id):
        if member_id not in self.members:
            print(f"Member ID {member_id} does not exist.")
            return False
        self.logged_in_member = self.members[member_id]
        print(f"Member {self.logged_in_member.username} logged in successfully.")
        return True

    # Logout the current library member
    def logout_member(self):
        if self.logged_in_member:
            print(f"Member {self.logged_in_member.username} logged out.")
            self.logged_in_member = None

    # Add a new book to the library
    def add_book(self, title, author, isbn):
        book = Book(title, author, isbn)
        self.books.append(book)
        print(f"Book '{title}' added successfully.")

    # Borrow a book from the library
    def borrow_book(self, isbn):
        if not self.logged_in_member:
            print("No member is currently logged in.")
            return False
        for book in self.books:
            if book.isbn == isbn and not book.borrower:
                book.borrower = self.logged_in_member
                book.date_borrowed = datetime.datetime.now()
                self.logged_in_member.borrowed_books.append(book)
                print(f"Book '{book.title}' borrowed successfully.")
                return True
        print("Book is not available for borrowing.")
        return False

    # Return a borrowed book
    def return_book(self, isbn):
        if not self.logged_in_member:
            print("No member is currently logged in.")
            return False
        for book in self.logged_in_member.borrowed_books:
            if book.isbn == isbn:
                book.borrower = None
                book.date_borrowed = None
                self.logged_in_member.borrowed_books.remove(book)
                print(f"Book '{book.title}' returned successfully.")
                return True
        print("This book is not borrowed by the current member.")
        return False

    # View all available books in the library
    def view_available_books(self):
        available_books = [book for book in self.books if not book.borrower]
        print("Available books:")
        for book in available_books:
            print(f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}")
        return available_books

    # View all borrowed books by the current member
    def view_borrowed_books(self):
        if not self.logged_in_member:
            print("No member is currently logged in.")
            return []
        print("Borrowed books:")
        for book in self.logged_in_member.borrowed_books:
            print(f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}, Date Borrowed: {book.date_borrowed}")
        return self.logged_in_member.borrowed_books

    # Search books by title
    def search_books_by_title(self, keyword):
        found_books = [book for book in self.books if keyword.lower() in book.title.lower()]
        print(f"Books found for keyword '{keyword}':")
        for book in found_books:
            print(f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}")
        return found_books

    # View library statistics
    def view_statistics(self):
        total_books = len(self.books)
        borrowed_books = sum(1 for book in self.books if book.borrower)
        print(f"Total Books: {total_books}, Borrowed Books: {borrowed_books}")
        return total_books, borrowed_books

    # View all members
    def view_all_members(self):
        print("Library Members:")
        for member_id, member in self.members.items():
            print(f"Username: {member.username}, ID: {member_id}, Date Joined: {member.date_joined}")

# Main program flow
def main():
    library_system = LibrarySystem()

    while True:
        print("\n=== Library System ===")
        print("1. Register Member")
        print("2. Login Member")
        print("3. Add Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. View Available Books")
        print("7. View Borrowed Books")
        print("8. Search Books by Title")
        print("9. View Statistics")
        print("10. View All Members")
        print("11. Logout")
        print("12. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            member_id = input("Enter member ID: ")
            library_system.register_member(username, member_id)

        elif choice == "2":
            member_id = input("Enter member ID: ")
            library_system.login_member(member_id)

        elif choice == "3":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            library_system.add_book(title, author, isbn)

        elif choice == "4":
            isbn = input("Enter book ISBN: ")
            library_system.borrow_book(isbn)

        elif choice == "5":
            isbn = input("Enter book ISBN: ")
            library_system.return_book(isbn)

        elif choice == "6":
            library_system.view_available_books()

        elif choice == "7":
            library_system.view_borrowed_books()

        elif choice == "8":
            keyword = input("Enter title keyword: ")
            library_system.search_books_by_title(keyword)

        elif choice == "9":
            library_system.view_statistics()

        elif choice == "10":
            library_system.view_all_members()

        elif choice == "11":
            library_system.logout_member()

        elif choice == "12":
            break

if __name__ == "__main__":
    main()