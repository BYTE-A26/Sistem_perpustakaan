"""
Sample Data Generator untuk Testing Sistem Perpustakaan Digital
Script ini menghasilkan sample data untuk demonstration
"""

import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.library_manager import LibraryManager
from src.auth import AuthenticationManager
from src.persistence import DataPersistence
from src.models import Book, UserRole


def generate_sample_data():
    """Generate sample data untuk testing"""
    
    print("Generating sample data for Digital Library System...")
    
    # Initialize managers
    library = LibraryManager()
    auth = AuthenticationManager()
    persistence = DataPersistence()
    
    # ==================== CREATE SAMPLE USERS ====================
    print("\n[1] Creating sample users...")
    
    users = [
        ("admin", "admin123456", "Administrator", "admin@library.com", 
         "0812-0000-0001", "Perpustakaan Main", UserRole.ADMIN.value),
        ("librarian", "librarian123", "Pustakawan Utama", "librarian@library.com",
         "0812-0000-0002", "Perpustakaan Main", UserRole.LIBRARIAN.value),
        ("budi", "budi123456", "Budi Santoso", "budi@example.com",
         "0812-3456-7890", "Jl. Ahmad Yani No. 10, Jakarta", UserRole.MEMBER.value),
        ("ani", "ani1234567", "Ani Wijaya", "ani@example.com",
         "0812-8765-4321", "Jl. Diponegoro No. 5, Bandung", UserRole.MEMBER.value),
        ("randi", "randi12345", "Randi Pratama", "randi@example.com",
         "0812-5555-5555", "Jl. Gatot Subroto No. 25, Surabaya", UserRole.MEMBER.value),
    ]
    
    for username, password, name, email, phone, address, role in users:
        user_id = str(uuid.uuid4())[:8]
        success, msg = auth.register_user(
            username, password, name, email, phone, address, user_id, role
        )
        if success:
            print(f"  ✓ User '{username}' ({role}) created")
        else:
            print(f"  ✗ Failed: {msg}")
    
    # ==================== CREATE SAMPLE BOOKS ====================
    print("\n[2] Creating sample books...")
    
    books_data = [
        ("Python Programming", "Mark Lutz", "O'Reilly Media", "978-1491957608", 2013, "Programming", 5, "Rak A1"),
        ("Clean Code", "Robert C. Martin", "Prentice Hall", "978-0132350884", 2008, "Programming", 4, "Rak A2"),
        ("The Pragmatic Programmer", "Andrew Hunt", "Addison-Wesley", "978-0201616224", 1999, "Programming", 3, "Rak A3"),
        ("Design Patterns", "Erich Gamma", "Addison-Wesley", "978-0201633610", 1994, "Programming", 2, "Rak A4"),
        ("Algorithms", "Robert Sedgewick", "Addison-Wesley", "978-0321573513", 2011, "Computer Science", 6, "Rak B1"),
        ("Introduction to Algorithms", "Thomas Cormen", "MIT Press", "978-0262033848", 2009, "Computer Science", 5, "Rak B2"),
        ("The C Programming Language", "Brian Kernighan", "Prentice Hall", "978-0131103627", 1988, "Programming", 4, "Rak B3"),
        ("Java: The Complete Reference", "Herbert Schildt", "McGraw-Hill", "978-0071808552", 2014, "Programming", 3, "Rak B4"),
        ("Sapiens", "Yuval Noah Harari", "Harper", "978-0062316097", 2014, "History", 7, "Rak C1"),
        ("Educated", "Tara Westover", "Random House", "978-0399590528", 2018, "Biography", 6, "Rak C2"),
        ("Thinking, Fast and Slow", "Daniel Kahneman", "Farrar, Straus and Giroux", "978-0374275631", 2011, "Psychology", 5, "Rak C3"),
        ("The Selfish Gene", "Richard Dawkins", "Oxford University Press", "978-0192860926", 1976, "Science", 4, "Rak C4"),
        ("1984", "George Orwell", "Secker & Warburg", "978-0451524935", 1949, "Fiction", 8, "Rak D1"),
        ("To Kill a Mockingbird", "Harper Lee", "J. B. Lippincott", "978-0061120084", 1960, "Fiction", 7, "Rak D2"),
        ("The Great Gatsby", "F. Scott Fitzgerald", "Scribner", "978-0743273565", 1925, "Fiction", 6, "Rak D3"),
        ("Pride and Prejudice", "Jane Austen", "T. Egerton", "978-0141439518", 1813, "Fiction", 5, "Rak D4"),
    ]
    
    for title, author, publisher, isbn, year, category, copies, location in books_data:
        book_id = str(uuid.uuid4())[:8]
        book = Book(
            book_id=book_id,
            title=title,
            author=author,
            publisher=publisher,
            isbn=isbn,
            publication_year=year,
            category=category,
            total_copies=copies,
            available_copies=copies,
            location=location,
            description=f"A great {category.lower()} book: {title}",
            pages=300 + (len(title) % 200),
            language="Indonesian" if "Python" in title else "English"
        )
        
        success, msg = library.add_book(book)
        if success:
            print(f"  ✓ Book '{title}' added")
        else:
            print(f"  ✗ Failed: {msg}")
    
    # ==================== CREATE BOOK RELATIONSHIPS ====================
    print("\n[3] Creating book relationships for recommendations...")
    
    all_books = [b for _, b in library.books_bst.get_all()]
    
    # Connect programming books
    programming_books = [b for b in all_books if b.category == "Programming"]
    for i in range(len(programming_books)):
        for j in range(i+1, len(programming_books)):
            similarity = 0.9 - (0.1 * (j - i))
            library.add_book_relationship(
                programming_books[i].book_id,
                programming_books[j].book_id,
                similarity
            )
    
    # Connect fiction books
    fiction_books = [b for b in all_books if b.category == "Fiction"]
    for i in range(len(fiction_books)):
        for j in range(i+1, len(fiction_books)):
            similarity = 0.85 - (0.1 * (j - i))
            library.add_book_relationship(
                fiction_books[i].book_id,
                fiction_books[j].book_id,
                similarity
            )
    
    print(f"  ✓ Book relationships created")
    
    # ==================== SAVE ALL DATA ====================
    print("\n[4] Saving all data to files...")
    
    success, msg = persistence.save_all(library, auth)
    print(f"  ✓ {msg}")
    
    # ==================== PRINT SUMMARY ====================
    print("\n" + "="*50)
    print("SAMPLE DATA GENERATION COMPLETED!")
    print("="*50)
    
    stats = library.generate_statistics()
    print(f"\nSystem Statistics:")
    print(f"  Total Books: {stats.total_books}")
    print(f"  Total Users: {auth.users.size}")
    print(f"  Available Books: {stats.available_books}")
    print(f"  Average Rating: {stats.average_rating:.1f}★")
    
    print("\n" + "="*50)
    print("SAMPLE USERS FOR TESTING:")
    print("="*50)
    print("\nAdmin Account:")
    print("  Username: admin")
    print("  Password: admin123456")
    
    print("\nLibrarian Account:")
    print("  Username: librarian")
    print("  Password: librarian123")
    
    print("\nMember Accounts:")
    print("  Username: budi | Password: budi123456")
    print("  Username: ani | Password: ani1234567")
    print("  Username: randi | Password: randi12345")
    
    print("\n" + "="*50)
    print("Data saved in 'data/' directory")
    print("Ready to start the application!")
    print("="*50 + "\n")


if __name__ == "__main__":
    generate_sample_data()
