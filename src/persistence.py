"""
Module Persistensi Data untuk Sistem Perpustakaan Digital
Menangani penyimpanan dan loading data dari file JSON
"""

import json
import os
from typing import Tuple
from src.models import Book, User, Transaction, Reservation, Review, SearchHistory
from src.library_manager import LibraryManager
from src.auth import AuthenticationManager


class DataPersistence:
    """Manager untuk menyimpan dan memuat data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.books_file = os.path.join(data_dir, "books.json")
        self.users_file = os.path.join(data_dir, "users.json")
        self.transactions_file = os.path.join(data_dir, "transactions.json")
        self.reservations_file = os.path.join(data_dir, "reservations.json")
        self.reviews_file = os.path.join(data_dir, "reviews.json")
        self.search_history_file = os.path.join(data_dir, "search_history.json")
        
        # Create data directory if not exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    # ==================== SAVE METHODS ====================
    
    def save_books(self, library_manager: LibraryManager) -> Tuple[bool, str]:
        """Save semua buku ke file"""
        try:
            books_data = []
            for book_id, book in library_manager.books_bst.get_all():
                books_data.append(book.to_dict())
            
            with open(self.books_file, 'w', encoding='utf-8') as f:
                json.dump(books_data, f, indent=2, ensure_ascii=False)
            
            return True, f"Berhasil menyimpan {len(books_data)} buku"
        except Exception as e:
            return False, f"Error menyimpan buku: {str(e)}"

    def save_users(self, auth_manager: AuthenticationManager) -> Tuple[bool, str]:
        """Save semua user ke file"""
        try:
            users_data = []
            all_users = auth_manager.users.get_all()
            for username, user in all_users.items():
                users_data.append(user.to_dict())
            
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, indent=2, ensure_ascii=False)
            
            return True, f"Berhasil menyimpan {len(users_data)} user"
        except Exception as e:
            return False, f"Error menyimpan user: {str(e)}"

    def save_transactions(self, library_manager: LibraryManager) -> Tuple[bool, str]:
        """Save semua transaksi ke file"""
        try:
            trans_data = []
            all_trans = library_manager.transactions.get_all()
            for trans in all_trans:
                trans_data.append(trans.to_dict())
            
            with open(self.transactions_file, 'w', encoding='utf-8') as f:
                json.dump(trans_data, f, indent=2, ensure_ascii=False)
            
            return True, f"Berhasil menyimpan {len(trans_data)} transaksi"
        except Exception as e:
            return False, f"Error menyimpan transaksi: {str(e)}"

    def save_reservations(self, library_manager: LibraryManager) -> Tuple[bool, str]:
        """Save semua reservasi ke file"""
        try:
            res_data = []
            all_res = library_manager.reservation_list.get_all()
            for res in all_res:
                res_data.append(res.to_dict())
            
            with open(self.reservations_file, 'w', encoding='utf-8') as f:
                json.dump(res_data, f, indent=2, ensure_ascii=False)
            
            return True, f"Berhasil menyimpan {len(res_data)} reservasi"
        except Exception as e:
            return False, f"Error menyimpan reservasi: {str(e)}"

    def save_reviews(self, library_manager: LibraryManager) -> Tuple[bool, str]:
        """Save semua review ke file"""
        try:
            rev_data = []
            all_rev = library_manager.reviews.get_all()
            for rev in all_rev:
                rev_data.append(rev.to_dict())
            
            with open(self.reviews_file, 'w', encoding='utf-8') as f:
                json.dump(rev_data, f, indent=2, ensure_ascii=False)
            
            return True, f"Berhasil menyimpan {len(rev_data)} review"
        except Exception as e:
            return False, f"Error menyimpan review: {str(e)}"

    def save_search_history(self, library_manager: LibraryManager) -> Tuple[bool, str]:
        """Save riwayat pencarian ke file"""
        try:
            hist_data = []
            all_hist = library_manager.search_history.get_all()
            for hist in all_hist:
                hist_data.append(hist.to_dict())
            
            with open(self.search_history_file, 'w', encoding='utf-8') as f:
                json.dump(hist_data, f, indent=2, ensure_ascii=False)
            
            return True, f"Berhasil menyimpan {len(hist_data)} riwayat pencarian"
        except Exception as e:
            return False, f"Error menyimpan riwayat pencarian: {str(e)}"

    def save_all(self, library_manager: LibraryManager, auth_manager: AuthenticationManager) -> Tuple[bool, str]:
        """Save semua data"""
        results = []
        
        results.append(self.save_books(library_manager))
        results.append(self.save_users(auth_manager))
        results.append(self.save_transactions(library_manager))
        results.append(self.save_reservations(library_manager))
        results.append(self.save_reviews(library_manager))
        results.append(self.save_search_history(library_manager))
        
        success_count = sum(1 for success, _ in results if success)
        all_success = all(success for success, _ in results)
        
        if all_success:
            return True, f"Semua data berhasil disimpan ({success_count}/6)"
        else:
            messages = "\n".join([msg for _, msg in results])
            return False, f"Error menyimpan data:\n{messages}"

    # ==================== LOAD METHODS ====================
    
    def load_books(self, library_manager: LibraryManager) -> Tuple[bool, str]:
        """Load buku dari file"""
        try:
            if not os.path.exists(self.books_file):
                return True, "File buku tidak ada (baru)"
            
            with open(self.books_file, 'r', encoding='utf-8') as f:
                books_data = json.load(f)
            
            for book_dict in books_data:
                book = Book.from_dict(book_dict)
                library_manager.add_book(book)
            
            return True, f"Berhasil memuat {len(books_data)} buku"
        except Exception as e:
            return False, f"Error memuat buku: {str(e)}"

    def load_users(self, auth_manager: AuthenticationManager) -> Tuple[bool, str]:
        """Load user dari file"""
        try:
            if not os.path.exists(self.users_file):
                return True, "File user tidak ada (baru)"
            
            with open(self.users_file, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            for user_dict in users_data:
                user = User.from_dict(user_dict)
                auth_manager.users.insert(user.username, user)
            
            return True, f"Berhasil memuat {len(users_data)} user"
        except Exception as e:
            return False, f"Error memuat user: {str(e)}"

    def load_transactions(self, library_manager: LibraryManager) -> Tuple[bool, str]:
        """Load transaksi dari file"""
        try:
            if not os.path.exists(self.transactions_file):
                return True, "File transaksi tidak ada (baru)"
            
            with open(self.transactions_file, 'r', encoding='utf-8') as f:
                trans_data = json.load(f)
            
            for trans_dict in trans_data:
                trans = Transaction.from_dict(trans_dict)
                library_manager.transactions.append(trans)
            
            return True, f"Berhasil memuat {len(trans_data)} transaksi"
        except Exception as e:
            return False, f"Error memuat transaksi: {str(e)}"

    def load_reservations(self, library_manager: LibraryManager) -> Tuple[bool, str]:
        """Load reservasi dari file"""
        try:
            if not os.path.exists(self.reservations_file):
                return True, "File reservasi tidak ada (baru)"
            
            with open(self.reservations_file, 'r', encoding='utf-8') as f:
                res_data = json.load(f)
            
            for res_dict in res_data:
                res = Reservation.from_dict(res_dict)
                library_manager.reservation_list.append(res)
            
            return True, f"Berhasil memuat {len(res_data)} reservasi"
        except Exception as e:
            return False, f"Error memuat reservasi: {str(e)}"

    def load_reviews(self, library_manager: LibraryManager) -> Tuple[bool, str]:
        """Load review dari file"""
        try:
            if not os.path.exists(self.reviews_file):
                return True, "File review tidak ada (baru)"
            
            with open(self.reviews_file, 'r', encoding='utf-8') as f:
                rev_data = json.load(f)
            
            for rev_dict in rev_data:
                rev = Review.from_dict(rev_dict)
                library_manager.reviews.append(rev)
            
            return True, f"Berhasil memuat {len(rev_data)} review"
        except Exception as e:
            return False, f"Error memuat review: {str(e)}"

    def load_search_history(self, library_manager: LibraryManager) -> Tuple[bool, str]:
        """Load riwayat pencarian dari file"""
        try:
            if not os.path.exists(self.search_history_file):
                return True, "File riwayat pencarian tidak ada (baru)"
            
            with open(self.search_history_file, 'r', encoding='utf-8') as f:
                hist_data = json.load(f)
            
            for hist_dict in hist_data:
                hist = SearchHistory.from_dict(hist_dict)
                library_manager.search_history.append(hist)
            
            return True, f"Berhasil memuat {len(hist_data)} riwayat pencarian"
        except Exception as e:
            return False, f"Error memuat riwayat pencarian: {str(e)}"

    def load_all(self, library_manager: LibraryManager, auth_manager: AuthenticationManager) -> Tuple[bool, str]:
        """Load semua data"""
        results = []
        
        results.append(self.load_books(library_manager))
        results.append(self.load_users(auth_manager))
        results.append(self.load_transactions(library_manager))
        results.append(self.load_reservations(library_manager))
        results.append(self.load_reviews(library_manager))
        results.append(self.load_search_history(library_manager))
        
        success_count = sum(1 for success, _ in results if success)
        all_success = all(success for success, _ in results if success)
        
        if all_success:
            return True, f"Semua data berhasil dimuat ({success_count}/6)"
        else:
            messages = "\n".join([msg for _, msg in results])
            return False, f"Error memuat data:\n{messages}"
