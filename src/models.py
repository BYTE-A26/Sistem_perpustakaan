"""
Module Models untuk Sistem Perpustakaan Digital
Mendefinisikan struktur data untuk Buku, User, Transaksi, dll
"""

from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum
import json


class BookStatus(Enum):
    """Status ketersediaan buku"""
    AVAILABLE = "Tersedia"
    BORROWED = "Dipinjam"
    RESERVED = "Dipesan"
    MAINTENANCE = "Maintenance"


class TransactionType(Enum):
    """Tipe transaksi perpustakaan"""
    BORROW = "Peminjaman"
    RETURN = "Pengembalian"
    RESERVATION = "Pemesanan"
    CANCEL_RESERVATION = "Batal Pesan"


class UserRole(Enum):
    """Role user dalam sistem"""
    ADMIN = "Admin"
    LIBRARIAN = "Librarian"
    MEMBER = "Member"


@dataclass
class Book:
    """Model untuk Data Buku"""
    book_id: str
    title: str
    author: str
    publisher: str
    isbn: str
    publication_year: int
    category: str
    total_copies: int
    available_copies: int
    location: str
    description: str = ""
    pages: int = 0
    language: str = "Indonesian"
    status: str = BookStatus.AVAILABLE.value
    rating: float = 0.0
    views: int = 0
    borrow_count: int = 0

    def to_dict(self) -> dict:
        """Convert ke dictionary"""
        data = asdict(self)
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Create instance dari dictionary"""
        return cls(**data)

    def is_available(self) -> bool:
        """Check apakah buku tersedia untuk dipinjam"""
        return self.available_copies > 0 and self.status == BookStatus.AVAILABLE.value


@dataclass
class User:
    """Model untuk Data User"""
    user_id: str
    username: str
    password_hash: str
    full_name: str
    email: str
    phone: str
    address: str
    role: str = UserRole.MEMBER.value
    registration_date: str = field(default_factory=lambda: datetime.now().isoformat())
    is_active: bool = True
    borrow_count: int = 0
    late_return_count: int = 0
    fine_amount: float = 0.0

    def to_dict(self) -> dict:
        """Convert ke dictionary (exclude password)"""
        data = asdict(self)
        # Don't include password hash
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create instance dari dictionary"""
        return cls(**data)


@dataclass
class Transaction:
    """Model untuk Data Transaksi"""
    transaction_id: str
    user_id: str
    book_id: str
    transaction_type: str  # BORROW, RETURN, RESERVATION
    transaction_date: str = field(default_factory=lambda: datetime.now().isoformat())
    due_date: Optional[str] = None
    return_date: Optional[str] = None
    fine_amount: float = 0.0
    status: str = "Aktif"
    notes: str = ""

    def to_dict(self) -> dict:
        """Convert ke dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        """Create instance dari dictionary"""
        return cls(**data)

    def is_overdue(self) -> bool:
        """Check apakah transaksi overdue"""
        if self.due_date and self.return_date is None:
            due = datetime.fromisoformat(self.due_date)
            return datetime.now() > due
        return False

    def calculate_fine(self, fine_per_day: float = 5000) -> float:
        """Calculate denda keterlambatan"""
        if not self.due_date or self.return_date is None:
            return 0.0
        
        due = datetime.fromisoformat(self.due_date)
        returned = datetime.fromisoformat(self.return_date)
        
        if returned > due:
            days_late = (returned - due).days
            self.fine_amount = days_late * fine_per_day
        
        return self.fine_amount


@dataclass
class Review:
    """Model untuk Review/Rating Buku"""
    review_id: str
    book_id: str
    user_id: str
    rating: int  # 1-5
    review_text: str
    review_date: str = field(default_factory=lambda: datetime.now().isoformat())
    helpful_count: int = 0

    def to_dict(self) -> dict:
        """Convert ke dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Review':
        """Create instance dari dictionary"""
        return cls(**data)


@dataclass
class Reservation:
    """Model untuk Reservasi Buku"""
    reservation_id: str
    user_id: str
    book_id: str
    reservation_date: str = field(default_factory=lambda: datetime.now().isoformat())
    priority: int = 0  # Untuk queue berdasarkan waktu
    status: str = "Aktif"  # Aktif, Siap, Dibatalkan
    expiry_date: str = field(default_factory=lambda: (datetime.now() + timedelta(days=7)).isoformat())

    def to_dict(self) -> dict:
        """Convert ke dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Reservation':
        """Create instance dari dictionary"""
        return cls(**data)

    def is_expired(self) -> bool:
        """Check apakah reservasi sudah expired"""
        expiry = datetime.fromisoformat(self.expiry_date)
        return datetime.now() > expiry


@dataclass
class SearchHistory:
    """Model untuk Riwayat Pencarian"""
    search_id: str
    user_id: str
    query: str
    search_date: str = field(default_factory=lambda: datetime.now().isoformat())
    results_count: int = 0

    def to_dict(self) -> dict:
        """Convert ke dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'SearchHistory':
        """Create instance dari dictionary"""
        return cls(**data)


@dataclass
class LibraryStatistics:
    """Model untuk Statistik Perpustakaan"""
    total_books: int = 0
    available_books: int = 0
    borrowed_books: int = 0
    total_members: int = 0
    active_members: int = 0
    total_transactions: int = 0
    total_fines: float = 0.0
    average_rating: float = 0.0
    most_borrowed_category: str = ""
    most_borrowed_book: str = ""
    generated_date: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert ke dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'LibraryStatistics':
        """Create instance dari dictionary"""
        return cls(**data)
