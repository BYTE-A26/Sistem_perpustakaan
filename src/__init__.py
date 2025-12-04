"""
Sistem Perpustakaan Digital
Integrated Library Management System dengan GUI, Authentication, dan Analytics

Version: 1.0.0
Author: Student
Date: December 2024
"""

from src.data_structures import (
    BinarySearchTree,
    HashTable,
    Queue,
    Stack,
    Graph,
    LinkedList,
    MinHeap
)

from src.models import (
    Book,
    User,
    Transaction,
    Reservation,
    Review,
    SearchHistory,
    BookStatus,
    TransactionType,
    UserRole
)

from src.auth import AuthenticationManager
from src.library_manager import LibraryManager
from src.persistence import DataPersistence

__version__ = "1.0.0"
__all__ = [
    "BinarySearchTree",
    "HashTable", 
    "Queue",
    "Stack",
    "Graph",
    "LinkedList",
    "MinHeap",
    "Book",
    "User",
    "Transaction",
    "Reservation",
    "Review",
    "SearchHistory",
    "BookStatus",
    "TransactionType",
    "UserRole",
    "AuthenticationManager",
    "LibraryManager",
    "DataPersistence"
]
