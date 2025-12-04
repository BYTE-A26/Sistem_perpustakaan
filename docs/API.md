# API Documentation

## Data Structures Module (`src/data_structures.py`)

### BinarySearchTree

```python
bst = BinarySearchTree()
bst.insert(key, value)          # Insert key-value pair
result = bst.search(key)        # Search by key
bst.delete(key)                 # Delete by key
items = bst.inorder_traversal() # Get sorted items
```

### HashTable

```python
ht = HashTable(capacity=100)
ht.insert(key, value)           # Insert/update
value = ht.search(key)          # Search
ht.delete(key)                  # Delete
all_data = ht.get_all()         # Get all as dict
```

### Queue

```python
queue = Queue()
queue.enqueue(item)             # Add to back
item = queue.dequeue()          # Remove from front
item = queue.peek()             # View front
is_empty = queue.is_empty()     # Check if empty
size = queue.size()             # Get size
```

### Stack

```python
stack = Stack()
stack.push(item)                # Add to top
item = stack.pop()              # Remove from top
item = stack.peek()             # View top
is_empty = stack.is_empty()     # Check if empty
size = stack.size()             # Get size
```

### Graph

```python
graph = Graph()
graph.add_node(book_id, title)  # Add node
graph.add_edge(id1, id2, weight) # Add edge
recs = graph.get_recommendations(book_id, depth) # Get recommendations
```

### LinkedList

```python
ll = LinkedList()
ll.append(data)                 # Add to end
ll.insert_at(index, data)       # Insert at position
data = ll.remove_at(index)      # Remove at position
data = ll.get(index)            # Get at position
all_data = ll.get_all()         # Get all as list
```

### MinHeap

```python
heap = MinHeap()
heap.insert((priority, data))   # Insert with priority
item = heap.extract_min()       # Extract min priority
item = heap.peek()              # View min
size = heap.size()              # Get size
```

---

## Authentication Module (`src/auth.py`)

### AuthenticationManager

#### register_user()
```python
success, message = auth_manager.register_user(
    username="john_doe",
    password="secure_password",
    full_name="John Doe",
    email="john@example.com",
    phone="08123456789",
    address="123 Main St",
    user_id="user001",
    role="Member"  # Optional, default: Member
)
```

#### login()
```python
success, message, session_id = auth_manager.login(
    username="john_doe",
    password="secure_password",
    session_duration=3600  # Optional, in seconds
)
```

#### validate_session()
```python
is_valid, user_id = auth_manager.validate_session(session_id)
```

#### change_password()
```python
success, message = auth_manager.change_password(
    username="john_doe",
    old_password="old_pass",
    new_password="new_pass"
)
```

#### logout()
```python
success = auth_manager.logout(session_id)
```

---

## Library Manager Module (`src/library_manager.py`)

### LibraryManager

#### Book Operations

```python
# Add book
success, message = library.add_book(book)

# Get book
book = library.get_book(book_id)

# Search by criteria
books = library.search_books_multi_criteria(
    title="Python",      # Optional
    author="John",       # Optional
    category="Fiction",  # Optional
    year=2023           # Optional
)

# Get all books
all_books = library.get_all_books()  # Returns list of (id, book) tuples

# Update book
success, message = library.update_book(book_id, title="New Title", available_copies=8)

# Delete book
success, message = library.delete_book(book_id)
```

#### Transaction Operations

```python
# Borrow book
success, message, trans_id = library.borrow_book(
    user_id="user001",
    book_id="book001",
    duration_days=7  # Optional, default: 7
)

# Return book
success, message, fine_amount = library.return_book(transaction_id)

# Get user transactions
transactions = library.get_user_transactions(user_id)

# Get all transactions
all_transactions = library.get_all_transactions()

# Get pending (not returned) books
pending = library.get_pending_transactions()

# Get overdue books
overdue = library.get_overdue_books()
```

#### Reservation Operations

```python
# Reserve book
success, message, res_id = library.reserve_book(
    user_id="user001",
    book_id="book001"
)

# Cancel reservation
success, message = library.cancel_reservation(reservation_id)

# Get user reservations
reservations = library.get_user_reservations(user_id)

# Get next reservation in queue
next_res = library.get_next_reservation(book_id)
```

#### Review Operations

```python
# Add review
success, message = library.add_review(
    user_id="user001",
    book_id="book001",
    rating=5,  # 1-5
    review_text="Great book!"
)

# Get book reviews
reviews = library.get_book_reviews(book_id)
```

#### Recommendation Operations

```python
# Add book relationship
library.add_book_relationship(book_id1, book_id2, similarity=0.8)

# Get recommendations
recommendations = library.get_recommendations(
    book_id="book001",
    depth=2
)
```

#### Statistics

```python
# Generate statistics
stats = library.generate_statistics()
# Returns LibraryStatistics with:
# - total_books, available_books, borrowed_books
# - total_members, active_members
# - total_transactions, total_fines
# - average_rating, most_borrowed_book, most_borrowed_category

# Get popular books
popular = library.get_popular_books(limit=10)

# Get highest rated books
top_rated = library.get_highest_rated_books(limit=10)
```

---

## Persistence Module (`src/persistence.py`)

### DataPersistence

```python
persistence = DataPersistence(data_dir="data")

# Save all data
success, message = persistence.save_all(library_manager, auth_manager)

# Load all data
success, message = persistence.load_all(library_manager, auth_manager)

# Save specific
success, message = persistence.save_books(library_manager)
success, message = persistence.save_users(auth_manager)
success, message = persistence.save_transactions(library_manager)
success, message = persistence.save_reservations(library_manager)
success, message = persistence.save_reviews(library_manager)
success, message = persistence.save_search_history(library_manager)

# Load specific
success, message = persistence.load_books(library_manager)
success, message = persistence.load_users(auth_manager)
success, message = persistence.load_transactions(library_manager)
success, message = persistence.load_reservations(library_manager)
success, message = persistence.load_reviews(library_manager)
success, message = persistence.load_search_history(library_manager)
```

---

## Models Module (`src/models.py`)

### Data Models

#### Book
```python
book = Book(
    book_id="book001",
    title="Python Programming",
    author="John Doe",
    publisher="Tech Press",
    isbn="123456789",
    publication_year=2023,
    category="Programming",
    total_copies=10,
    available_copies=10,
    location="Rak B2",
    description="Learn Python",  # Optional
    pages=500,  # Optional
    language="Indonesian",  # Optional
    status="Tersedia",  # Optional
    rating=4.5,  # Optional
    views=100,  # Optional
    borrow_count=15  # Optional
)

book.is_available()  # Check if book can be borrowed
```

#### User
```python
user = User(
    user_id="user001",
    username="john_doe",
    password_hash="hash$salt",
    full_name="John Doe",
    email="john@example.com",
    phone="08123456789",
    address="123 Main St",
    role="Member",  # Optional
    registration_date="2024-12-04T10:30:00",  # Optional
    is_active=True,  # Optional
    borrow_count=5,  # Optional
    late_return_count=0,  # Optional
    fine_amount=0.0  # Optional
)
```

#### Transaction
```python
transaction = Transaction(
    transaction_id="trans001",
    user_id="user001",
    book_id="book001",
    transaction_type="Peminjaman",
    transaction_date="2024-12-04T10:30:00",  # Optional
    due_date="2024-12-11T10:30:00",  # Optional
    return_date=None,  # Optional
    fine_amount=0.0,  # Optional
    status="Aktif",  # Optional
    notes=""  # Optional
)

transaction.is_overdue()  # Check if overdue
transaction.calculate_fine(fine_per_day=5000)  # Calculate fine
```

#### Reservation
```python
reservation = Reservation(
    reservation_id="res001",
    user_id="user001",
    book_id="book001",
    reservation_date="2024-12-04T10:30:00",  # Optional
    priority=0,  # Optional
    status="Aktif",  # Optional
    expiry_date="2024-12-11T10:30:00"  # Optional
)

reservation.is_expired()  # Check if expired
```

#### Review
```python
review = Review(
    review_id="rev001",
    book_id="book001",
    user_id="user001",
    rating=5,  # 1-5
    review_text="Excellent book!",
    review_date="2024-12-04T10:30:00",  # Optional
    helpful_count=10  # Optional
)
```

---

## Error Handling

All methods return `(success: bool, message: str)` or `(success: bool, message: str, data: Any)`

```python
success, message = library.add_book(book)
if not success:
    print(f"Error: {message}")
else:
    print("Operation successful")
```

Common error messages:
- "Book ID sudah terdaftar"
- "Buku tidak ditemukan"
- "Buku tidak tersedia"
- "User tidak ditemukan"
- "Username atau password salah"
- "Password minimal 8 karakter"
- "Transaksi tidak ditemukan"
- "Rating harus antara 1-5"

---

## Constants

### BookStatus
- `AVAILABLE = "Tersedia"`
- `BORROWED = "Dipinjam"`
- `RESERVED = "Dipesan"`
- `MAINTENANCE = "Maintenance"`

### TransactionType
- `BORROW = "Peminjaman"`
- `RETURN = "Pengembalian"`
- `RESERVATION = "Pemesanan"`
- `CANCEL_RESERVATION = "Batal Pesan"`

### UserRole
- `ADMIN = "Admin"`
- `LIBRARIAN = "Librarian"`
- `MEMBER = "Member"`
