"""
Module LibraryManager untuk Sistem Perpustakaan Digital
Core business logic untuk manajemen buku, transaksi, dan rekomendasi
"""

import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from src.data_structures import (
    BinarySearchTree, HashTable, Queue, Stack, Graph, 
    LinkedList, MinHeap
)
from src.models import (
    Book, Transaction, Reservation, Review, SearchHistory, 
    TransactionType, BookStatus, LibraryStatistics
)


class LibraryManager:
    """
    Core manager untuk operasi perpustakaan
    Mengintegrasikan berbagai struktur data
    """
    
    def __init__(self):
        # Data structures untuk berbagai keperluan
        self.books_bst: BinarySearchTree = BinarySearchTree()  # Books by ID
        self.books_hash: HashTable = HashTable(capacity=500)  # Books by title
        self.books_by_category: dict = {}  # Category -> books list
        self.books_by_author: HashTable = HashTable(capacity=500)  # Books by author
        
        self.transactions: LinkedList = LinkedList()  # Riwayat transaksi
        self.transaction_queue: Queue = Queue()  # Queue transaksi yang diproses
        self.transaction_history: Stack = Stack()  # Stack untuk undo/redo
        
        self.reservations: MinHeap = MinHeap()  # Priority queue untuk reservasi
        self.reservation_list: LinkedList = LinkedList()  # Daftar reservasi
        
        self.reviews: LinkedList = LinkedList()  # Daftar review
        self.search_history: LinkedList = LinkedList()  # Riwayat pencarian
        
        self.recommendation_graph: Graph = Graph()  # Graph untuk rekomendasi
        
        self.borrow_count: int = 0
        self.return_count: int = 0

    # ==================== MANAJEMEN BUKU ====================
    
    def add_book(self, book: Book) -> Tuple[bool, str]:
        """Tambah buku baru ke sistem"""
        if self.books_bst.search(book.book_id) is not None:
            return False, "Book ID sudah terdaftar"
        
        # Insert ke berbagai struktur
        self.books_bst.insert(book.book_id, book)
        self.books_hash.insert(book.title.lower(), book)
        self.books_by_author.insert(book.author.lower(), book)
        
        # Add ke category index
        if book.category not in self.books_by_category:
            self.books_by_category[book.category] = LinkedList()
        self.books_by_category[book.category].append(book)
        
        # Add ke graph untuk rekomendasi
        self.recommendation_graph.add_node(book.book_id, book.title)
        
        return True, f"Buku '{book.title}' berhasil ditambahkan"

    def get_book(self, book_id: str) -> Optional[Book]:
        """Get buku berdasarkan ID"""
        return self.books_bst.search(book_id)

    def search_book_by_title(self, title: str) -> Optional[Book]:
        """Search buku berdasarkan title"""
        return self.books_hash.search(title.lower())

    def search_book_by_author(self, author: str) -> Optional[Book]:
        """Search buku berdasarkan author"""
        return self.books_by_author.search(author.lower())

    def search_books_by_category(self, category: str) -> List[Book]:
        """Get semua buku dalam kategori tertentu"""
        if category in self.books_by_category:
            return self.books_by_category[category].get_all()
        return []

    def search_books_multi_criteria(self, title: str = "", author: str = "", 
                                   category: str = "", year: int = 0) -> List[Book]:
        """
        Pencarian multi-kriteria
        Menggunakan kombinasi BST traversal, Hash Table, dan Array Operations
        """
        results = []
        all_books = self.books_bst.get_all()
        
        for book_id, book in all_books:
            # Filter berdasarkan kriteria
            title_match = not title or title.lower() in book.title.lower()
            author_match = not author or author.lower() in book.author.lower()
            category_match = not category or category == book.category
            year_match = not year or book.publication_year == year
            
            if title_match and author_match and category_match and year_match:
                results.append(book)
        
        return results

    def get_all_books(self) -> List[Tuple[str, Book]]:
        """Get semua buku (sorted by ID)"""
        return self.books_bst.get_all()

    def update_book(self, book_id: str, **kwargs) -> Tuple[bool, str]:
        """Update informasi buku"""
        book = self.get_book(book_id)
        if book is None:
            return False, "Buku tidak ditemukan"
        
        # Update fields
        for key, value in kwargs.items():
            if hasattr(book, key):
                setattr(book, key, value)
        
        # Update di semua struktur
        self.books_bst.insert(book.book_id, book)
        self.books_hash.insert(book.title.lower(), book)
        self.books_by_author.insert(book.author.lower(), book)
        
        return True, "Buku berhasil diupdate"

    def delete_book(self, book_id: str) -> Tuple[bool, str]:
        """Hapus buku dari sistem"""
        book = self.get_book(book_id)
        if book is None:
            return False, "Buku tidak ditemukan"
        
        # Hapus dari berbagai struktur
        self.books_bst.delete(book_id)
        self.books_hash.delete(book.title.lower())
        self.books_by_author.delete(book.author.lower())
        
        return True, "Buku berhasil dihapus"

    # ==================== SISTEM TRANSAKSI ====================
    
    def borrow_book(self, user_id: str, book_id: str, duration_days: int = 7) -> Tuple[bool, str, Optional[str]]:
        """Proses peminjaman buku"""
        book = self.get_book(book_id)
        if book is None:
            return False, "Buku tidak ditemukan", None
        
        if book.available_copies <= 0:
            return False, "Buku tidak tersedia", None
        
        # Create transaction
        transaction_id = str(uuid.uuid4())[:8]
        due_date = (datetime.now() + timedelta(days=duration_days)).isoformat()
        
        transaction = Transaction(
            transaction_id=transaction_id,
            user_id=user_id,
            book_id=book_id,
            transaction_type=TransactionType.BORROW.value,
            due_date=due_date,
            status="Aktif"
        )
        
        # Add ke queue untuk diproses
        self.transaction_queue.enqueue(transaction)
        
        # Update buku
        book.available_copies -= 1
        book.borrow_count += 1
        if book.available_copies == 0:
            book.status = BookStatus.BORROWED.value
        self.update_book(book_id, 
                        available_copies=book.available_copies,
                        borrow_count=book.borrow_count,
                        status=book.status)
        
        # Tambah ke history
        self.transactions.append(transaction)
        self.transaction_history.push({
            'action': 'borrow',
            'transaction': transaction,
            'book_before': book
        })
        
        self.borrow_count += 1
        
        return True, f"Peminjaman berhasil. Batas pengembalian: {due_date}", transaction_id

    def return_book(self, transaction_id: str) -> Tuple[bool, str, float]:
        """Proses pengembalian buku"""
        # Cari transaksi
        transactions = self.transactions.get_all()
        transaction = None
        for trans in transactions:
            if trans.transaction_id == transaction_id:
                transaction = trans
                break
        
        if transaction is None:
            return False, "Transaksi tidak ditemukan", 0.0
        
        if transaction.transaction_type != TransactionType.BORROW.value:
            return False, "Transaksi bukan peminjaman", 0.0
        
        if transaction.status != "Aktif":
            return False, "Transaksi sudah ditutup", 0.0
        
        # Get buku
        book = self.get_book(transaction.book_id)
        if book is None:
            return False, "Buku tidak ditemukan", 0.0
        
        # Create return transaction
        transaction.return_date = datetime.now().isoformat()
        transaction.status = "Selesai"
        fine_amount = transaction.calculate_fine()
        
        # Update buku
        book.available_copies += 1
        if book.available_copies == book.total_copies:
            book.status = BookStatus.AVAILABLE.value
        self.update_book(transaction.book_id,
                        available_copies=book.available_copies,
                        status=book.status)
        
        # Tambah ke history
        self.transaction_history.push({
            'action': 'return',
            'transaction': transaction,
            'fine_amount': fine_amount
        })
        
        self.return_count += 1
        
        return True, "Pengembalian berhasil", fine_amount

    def get_user_transactions(self, user_id: str) -> List[Transaction]:
        """Get transaksi user"""
        all_trans = self.transactions.get_all()
        return [t for t in all_trans if t.user_id == user_id]

    def get_all_transactions(self) -> List[Transaction]:
        """Get semua transaksi"""
        return self.transactions.get_all()

    def get_pending_transactions(self) -> List[Transaction]:
        """Get transaksi yang masih pending (belum di-return)"""
        all_trans = self.transactions.get_all()
        return [t for t in all_trans if t.status == "Aktif" and t.transaction_type == TransactionType.BORROW.value]

    def get_overdue_books(self) -> List[Transaction]:
        """Get buku yang overdue"""
        pending = self.get_pending_transactions()
        overdue = []
        for trans in pending:
            if trans.is_overdue():
                overdue.append(trans)
        return overdue

    # ==================== SISTEM RESERVASI ====================
    
    def reserve_book(self, user_id: str, book_id: str) -> Tuple[bool, str, Optional[str]]:
        """Reservasi buku"""
        book = self.get_book(book_id)
        if book is None:
            return False, "Buku tidak ditemukan", None
        
        if book.available_copies > 0:
            return False, "Buku masih tersedia, tidak perlu reservasi", None
        
        # Create reservation
        reservation_id = str(uuid.uuid4())[:8]
        current_priority = self.reservations.size()
        
        reservation = Reservation(
            reservation_id=reservation_id,
            user_id=user_id,
            book_id=book_id
        )
        
        # Add ke priority queue
        self.reservations.insert((current_priority, reservation))
        self.reservation_list.append(reservation)
        
        return True, f"Reservasi berhasil. Posisi: {current_priority + 1}", reservation_id

    def cancel_reservation(self, reservation_id: str) -> Tuple[bool, str]:
        """Cancel reservasi"""
        reservations = self.reservation_list.get_all()
        for i, res in enumerate(reservations):
            if res.reservation_id == reservation_id:
                res.status = "Dibatalkan"
                self.reservation_list.insert_at(i, res)
                return True, "Reservasi berhasil dibatalkan"
        
        return False, "Reservasi tidak ditemukan"

    def get_user_reservations(self, user_id: str) -> List[Reservation]:
        """Get reservasi user"""
        reservations = self.reservation_list.get_all()
        return [r for r in reservations if r.user_id == user_id and r.status == "Aktif"]

    def get_next_reservation(self, book_id: str) -> Optional[Reservation]:
        """Get reservasi berikutnya untuk buku"""
        heap_items = self.reservations.get_all()
        
        for priority, res in sorted(heap_items, key=lambda x: x[0]):
            if res.book_id == book_id and res.status == "Aktif":
                return res
        
        return None

    # ==================== SISTEM RATING/REVIEW ====================
    
    def add_review(self, user_id: str, book_id: str, rating: int, review_text: str) -> Tuple[bool, str]:
        """Add review/rating untuk buku"""
        if rating < 1 or rating > 5:
            return False, "Rating harus antara 1-5"
        
        book = self.get_book(book_id)
        if book is None:
            return False, "Buku tidak ditemukan"
        
        review_id = str(uuid.uuid4())[:8]
        review = Review(
            review_id=review_id,
            book_id=book_id,
            user_id=user_id,
            rating=rating,
            review_text=review_text
        )
        
        self.reviews.append(review)
        
        # Update book rating (simple average)
        all_reviews = self.reviews.get_all()
        book_reviews = [r for r in all_reviews if r.book_id == book_id]
        avg_rating = sum(r.rating for r in book_reviews) / len(book_reviews) if book_reviews else 0
        self.update_book(book_id, rating=avg_rating)
        
        return True, "Review berhasil ditambahkan"

    def get_book_reviews(self, book_id: str) -> List[Review]:
        """Get semua review untuk buku"""
        all_reviews = self.reviews.get_all()
        return [r for r in all_reviews if r.book_id == book_id]

    # ==================== SISTEM REKOMENDASI ====================
    
    def add_book_relationship(self, book_id1: str, book_id2: str, similarity: float = 1.0) -> None:
        """Add hubungan antar buku (untuk rekomendasi)"""
        self.recommendation_graph.add_edge(book_id1, book_id2, similarity)

    def get_recommendations(self, book_id: str, depth: int = 2) -> List[Tuple[str, float]]:
        """Get rekomendasi buku berdasarkan similarity"""
        recommendations = self.recommendation_graph.get_recommendations(book_id, depth)
        
        # Enrich dengan data buku
        result = []
        for rec_id, weight in recommendations:
            book = self.get_book(rec_id)
            if book:
                result.append((book.title, weight))
        
        return result

    # ==================== RIWAYAT PENCARIAN ====================
    
    def add_search_history(self, user_id: str, query: str, results_count: int) -> None:
        """Tambah ke riwayat pencarian"""
        search_id = str(uuid.uuid4())[:8]
        search = SearchHistory(
            search_id=search_id,
            user_id=user_id,
            query=query,
            results_count=results_count
        )
        self.search_history.append(search)

    def get_user_search_history(self, user_id: str) -> List[SearchHistory]:
        """Get riwayat pencarian user"""
        all_history = self.search_history.get_all()
        return [s for s in all_history if s.user_id == user_id]

    # ==================== STATISTIK & ANALYTICS ====================
    
    def generate_statistics(self) -> LibraryStatistics:
        """Generate statistik perpustakaan"""
        all_books = [b for _, b in self.books_bst.get_all()]
        
        total_books = len(all_books)
        available_books = sum(1 for b in all_books if b.available_copies > 0)
        borrowed_books = total_books - available_books
        
        all_trans = self.transactions.get_all()
        total_transactions = len(all_trans)
        total_fines = sum(t.fine_amount for t in all_trans)
        
        # Calculate average rating
        all_reviews = self.reviews.get_all()
        avg_rating = (sum(r.rating for r in all_reviews) / len(all_reviews)) if all_reviews else 0
        
        # Most borrowed
        borrow_count = {}
        category_count = {}
        for book in all_books:
            borrow_count[book.book_id] = book.borrow_count
            category_count[book.category] = category_count.get(book.category, 0) + book.borrow_count
        
        most_borrowed_id = max(borrow_count, key=borrow_count.get) if borrow_count else ""
        most_borrowed_book = self.get_book(most_borrowed_id).title if most_borrowed_id else ""
        most_borrowed_category = max(category_count, key=category_count.get) if category_count else ""
        
        stats = LibraryStatistics(
            total_books=total_books,
            available_books=available_books,
            borrowed_books=borrowed_books,
            total_transactions=total_transactions,
            total_fines=total_fines,
            average_rating=avg_rating,
            most_borrowed_category=most_borrowed_category,
            most_borrowed_book=most_borrowed_book
        )
        
        return stats

    def get_popular_books(self, limit: int = 10) -> List[Book]:
        """Get buku paling populer berdasarkan borrow count"""
        all_books = [b for _, b in self.books_bst.get_all()]
        sorted_books = sorted(all_books, key=lambda b: b.borrow_count, reverse=True)
        return sorted_books[:limit]

    def get_highest_rated_books(self, limit: int = 10) -> List[Book]:
        """Get buku dengan rating tertinggi"""
        all_books = [b for _, b in self.books_bst.get_all()]
        sorted_books = sorted(all_books, key=lambda b: b.rating, reverse=True)
        return sorted_books[:limit]

    def process_transaction_queue(self) -> int:
        """Process semua transaksi dalam queue"""
        processed = 0
        while not self.transaction_queue.is_empty():
            trans = self.transaction_queue.dequeue()
            if trans:
                processed += 1
        return processed
