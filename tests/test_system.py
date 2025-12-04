"""
Unit Tests untuk Sistem Perpustakaan Digital
Test untuk semua struktur data dan fitur utama
"""

import unittest
import sys
import os
from datetime import datetime, timedelta

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_structures import (
    BinarySearchTree, HashTable, Queue, Stack, Graph,
    LinkedList, MinHeap
)
from src.models import Book, User, Transaction, UserRole, BookStatus
from src.auth import AuthenticationManager
from src.library_manager import LibraryManager
from src.persistence import DataPersistence


class TestDataStructures(unittest.TestCase):
    """Test semua data structures"""

    def test_binary_search_tree(self):
        """Test BST operations"""
        bst = BinarySearchTree()
        
        # Test insert
        bst.insert("book1", "Title 1")
        bst.insert("book2", "Title 2")
        bst.insert("book3", "Title 3")
        self.assertEqual(bst.size, 3)
        
        # Test search
        self.assertEqual(bst.search("book1"), "Title 1")
        self.assertIsNone(bst.search("book999"))
        
        # Test delete
        self.assertTrue(bst.delete("book1"))
        self.assertEqual(bst.size, 2)
        self.assertIsNone(bst.search("book1"))

    def test_hash_table(self):
        """Test Hash Table operations"""
        ht = HashTable(capacity=50)
        
        # Test insert
        ht.insert("key1", "value1")
        ht.insert("key2", "value2")
        self.assertEqual(ht.size, 2)
        
        # Test search
        self.assertEqual(ht.search("key1"), "value1")
        self.assertIsNone(ht.search("key999"))
        
        # Test delete
        self.assertTrue(ht.delete("key1"))
        self.assertEqual(ht.size, 1)

    def test_queue(self):
        """Test Queue operations"""
        queue = Queue()
        
        # Test enqueue
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        self.assertEqual(queue.size(), 3)
        
        # Test dequeue (FIFO)
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual(queue.size(), 1)

    def test_stack(self):
        """Test Stack operations"""
        stack = Stack()
        
        # Test push
        stack.push(1)
        stack.push(2)
        stack.push(3)
        self.assertEqual(stack.size(), 3)
        
        # Test pop (LIFO)
        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.size(), 1)

    def test_linked_list(self):
        """Test Linked List operations"""
        ll = LinkedList()
        
        # Test append
        ll.append(10)
        ll.append(20)
        ll.append(30)
        self.assertEqual(ll.size, 3)
        
        # Test get
        self.assertEqual(ll.get(0), 10)
        self.assertEqual(ll.get(2), 30)
        
        # Test insert at
        ll.insert_at(1, 15)
        self.assertEqual(ll.get(1), 15)
        self.assertEqual(ll.size, 4)

    def test_min_heap(self):
        """Test Min Heap operations"""
        heap = MinHeap()
        
        # Test insert
        heap.insert((5, "data5"))
        heap.insert((3, "data3"))
        heap.insert((7, "data7"))
        heap.insert((1, "data1"))
        
        # Test extract min
        min_item = heap.extract_min()
        self.assertEqual(min_item[0], 1)
        
        self.assertEqual(heap.extract_min()[0], 3)
        self.assertEqual(heap.size(), 2)

    def test_graph(self):
        """Test Graph operations"""
        graph = Graph()
        
        # Test add nodes
        graph.add_node("book1", "Title 1")
        graph.add_node("book2", "Title 2")
        graph.add_node("book3", "Title 3")
        
        # Test add edges
        graph.add_edge("book1", "book2", 0.8)
        graph.add_edge("book1", "book3", 0.5)
        
        # Test recommendations
        recs = graph.get_recommendations("book1", depth=1)
        self.assertEqual(len(recs), 2)
        self.assertEqual(recs[0][0], "book2")  # Highest weight first


class TestAuthentication(unittest.TestCase):
    """Test authentication system"""

    def setUp(self):
        self.auth = AuthenticationManager()

    def test_register_user(self):
        """Test user registration"""
        success, msg = self.auth.register_user(
            "testuser", "password123", "Test User",
            "test@email.com", "08123456789", "Jl. Test",
            "user001"
        )
        self.assertTrue(success)

    def test_login(self):
        """Test user login"""
        self.auth.register_user(
            "testuser", "password123", "Test User",
            "test@email.com", "08123456789", "Jl. Test",
            "user001"
        )
        
        success, msg, session_id = self.auth.login("testuser", "password123")
        self.assertTrue(success)
        self.assertIsNotNone(session_id)

    def test_invalid_login(self):
        """Test invalid login"""
        success, msg, session_id = self.auth.login("nonexistent", "password")
        self.assertFalse(success)
        self.assertIsNone(session_id)

    def test_session_validation(self):
        """Test session validation"""
        self.auth.register_user(
            "testuser", "password123", "Test User",
            "test@email.com", "08123456789", "Jl. Test",
            "user001"
        )
        
        _, _, session_id = self.auth.login("testuser", "password123")
        
        is_valid, user_id = self.auth.validate_session(session_id)
        self.assertTrue(is_valid)
        self.assertIsNotNone(user_id)

    def test_change_password(self):
        """Test change password"""
        self.auth.register_user(
            "testuser", "password123", "Test User",
            "test@email.com", "08123456789", "Jl. Test",
            "user001"
        )
        
        success, msg = self.auth.change_password("testuser", "password123", "newpassword456")
        self.assertTrue(success)
        
        # Test login with new password
        success, _, _ = self.auth.login("testuser", "newpassword456")
        self.assertTrue(success)


class TestLibraryManager(unittest.TestCase):
    """Test library manager operations"""

    def setUp(self):
        self.library = LibraryManager()
        self.auth = AuthenticationManager()
        
        # Create test data
        self.book = Book(
            book_id="book001",
            title="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            isbn="123456789",
            publication_year=2023,
            category="Fiction",
            total_copies=5,
            available_copies=5,
            location="Rak A1"
        )
        
        self.auth.register_user(
            "testuser", "password123", "Test User",
            "test@email.com", "08123456789", "Jl. Test",
            "user001"
        )
        self.user = self.auth.get_user("testuser")

    def test_add_book(self):
        """Test add book"""
        success, msg = self.library.add_book(self.book)
        self.assertTrue(success)
        self.assertEqual(self.library.books_bst.size, 1)

    def test_search_book(self):
        """Test search book"""
        self.library.add_book(self.book)
        
        result = self.library.get_book("book001")
        self.assertIsNotNone(result)
        self.assertEqual(result.title, "Test Book")

    def test_borrow_book(self):
        """Test borrow book"""
        self.library.add_book(self.book)
        
        success, msg, trans_id = self.library.borrow_book(self.user.user_id, "book001")
        self.assertTrue(success)
        self.assertIsNotNone(trans_id)
        
        # Check available copies decreased
        book = self.library.get_book("book001")
        self.assertEqual(book.available_copies, 4)

    def test_return_book(self):
        """Test return book"""
        self.library.add_book(self.book)
        
        _, _, trans_id = self.library.borrow_book(self.user.user_id, "book001")
        success, msg, fine = self.library.return_book(trans_id)
        
        self.assertTrue(success)
        self.assertEqual(fine, 0.0)  # No fine if returned on time
        
        # Check available copies increased
        book = self.library.get_book("book001")
        self.assertEqual(book.available_copies, 5)

    def test_reserve_book(self):
        """Test book reservation"""
        self.library.add_book(self.book)
        
        # Borrow all copies
        for i in range(5):
            user_id = f"user{i:03d}"
            self.library.borrow_book(user_id, "book001")
        
        # Now reserve
        success, msg, res_id = self.library.reserve_book(self.user.user_id, "book001")
        self.assertTrue(success)
        self.assertIsNotNone(res_id)

    def test_search_multi_criteria(self):
        """Test multi-criteria search"""
        self.library.add_book(self.book)
        
        results = self.library.search_books_multi_criteria(
            title="Test", author="Test Author"
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].book_id, "book001")

    def test_statistics(self):
        """Test generate statistics"""
        self.library.add_book(self.book)
        
        stats = self.library.generate_statistics()
        self.assertEqual(stats.total_books, 1)
        self.assertEqual(stats.available_books, 1)


class TestPersistence(unittest.TestCase):
    """Test data persistence"""

    def setUp(self):
        self.data_dir = "test_data"
        self.persistence = DataPersistence(self.data_dir)
        self.library = LibraryManager()
        self.auth = AuthenticationManager()

    def tearDown(self):
        # Clean up test data
        import shutil
        if os.path.exists(self.data_dir):
            shutil.rmtree(self.data_dir)

    def test_save_and_load_books(self):
        """Test save and load books"""
        book = Book(
            book_id="book001",
            title="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            isbn="123456789",
            publication_year=2023,
            category="Fiction",
            total_copies=5,
            available_copies=5,
            location="Rak A1"
        )
        
        self.library.add_book(book)
        
        # Save
        success, msg = self.persistence.save_books(self.library)
        self.assertTrue(success)
        
        # Load into new manager
        library2 = LibraryManager()
        success, msg = self.persistence.load_books(library2)
        self.assertTrue(success)
        self.assertEqual(library2.books_bst.size, 1)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == "__main__":
    run_tests()
