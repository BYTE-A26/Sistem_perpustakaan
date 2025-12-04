# QUICK START GUIDE

## 🚀 Mulai Aplikasi dalam 3 Langkah

### 1️⃣ Install Dependencies
```bash
cd c:\Users\ASUS\Documents\TUGAS\Proyek\Proyek
pip install -r requirements.txt
```

### 2️⃣ Generate Sample Data (Opsional tapi Recommended)
```bash
python generate_sample_data.py
```

### 3️⃣ Run Aplikasi
```bash
python main.py
```

---

## 👤 Default Login Credentials (Jika Sample Data Digunakan)

### Admin Account
- **Username**: `admin`
- **Password**: `admin123456`

### Librarian Account
- **Username**: `librarian`
- **Password**: `librarian123`

### Member Accounts
- **Username**: `budi` | **Password**: `budi123456`
- **Username**: `ani` | **Password**: `ani1234567`
- **Username**: `randi` | **Password**: `randi12345`

---

## 📁 File Structure

```
Proyek/
├── main.py                    # Entry point aplikasi
├── generate_sample_data.py    # Generator data sample
├── requirements.txt           # Python dependencies
│
├── src/                       # Source code
│   ├── __init__.py
│   ├── data_structures.py    # 7 struktur data utama
│   ├── models.py             # Data models
│   ├── auth.py              # Authentication
│   ├── library_manager.py   # Core business logic
│   ├── persistence.py       # Data persistence
│   └── gui.py               # GUI Tkinter
│
├── data/                      # Data storage (auto-created)
│   ├── books.json
│   ├── users.json
│   ├── transactions.json
│   ├── reservations.json
│   ├── reviews.json
│   └── search_history.json
│
├── tests/
│   └── test_system.py        # Unit tests
│
└── docs/                      # Documentation
    ├── README.md             # Full documentation
    ├── API.md               # API reference
    ├── USER_MANUAL.md       # User guide
    ├── ARCHITECTURE.md      # System architecture
    └── FEATURES_CHECKLIST.md
```

---

## ✨ Features Implementation Checklist

### ✅ Core Features (Mandatory)
- [x] **Manajemen Data (BST + Hash Table)**
  - Binary Search Tree untuk indexing buku
  - Hash Table untuk lookup username & title
  - Combined approach untuk optimal performance

- [x] **Sistem Transaksi (Queue + Stack)**
  - Queue untuk processing transaksi secara FIFO
  - Stack untuk undo/redo transaction history
  - Detailed transaction logging

- [x] **Pencarian Multi-Kriteria (Tree Traversal + Hashing)**
  - Search by title, author, category, year
  - Combined BST traversal + filtering
  - Fast lookup menggunakan Hash Table

- [x] **Sistem Rekomendasi (Graph Algorithms)**
  - Graph-based book relationship
  - DFS traversal untuk recommendation generation
  - Weighted edges untuk relevance scoring

- [x] **Manajemen User (Hash Table + Encryption)**
  - Hash Table untuk user storage
  - PBKDF2-SHA256 password hashing
  - Session-based authentication

- [x] **Analytics & Reporting (Array Operations)**
  - Book popularity statistics
  - Category-based analytics
  - User transaction analysis
  - Comprehensive dashboard

### ✅ Technical Requirements

- [x] **GUI - Tkinter**
  - Login/Registration interface
  - Main menu with role-based options
  - Search interface dengan multi-criteria
  - Book list dengan sorting
  - Transaction management
  - Admin dashboard

- [x] **6+ Data Structures**
  1. Binary Search Tree (BST)
  2. Hash Table
  3. Queue (FIFO)
  4. Stack (LIFO)
  5. Graph
  6. Linked List
  7. Min Heap (Bonus)

- [x] **Sistem Autentikasi User**
  - User registration dengan validation
  - Secure password hashing
  - Session management
  - Rate limiting untuk failed login

- [x] **Persistensi Data**
  - JSON-based file storage
  - Save/load functionality
  - Error handling untuk I/O

- [x] **Error Handling**
  - Input validation
  - Business logic validation
  - Exception handling
  - User-friendly error messages

### ✅ Additional Features

- [x] **Reservasi Buku**
  - Reserve unavailable books
  - Priority queue management
  - Auto-expiry setelah 7 hari

- [x] **Rating & Review System**
  - 1-5 star rating
  - User reviews/comments
  - Automatic rating aggregation

- [x] **Search History**
  - Track user searches
  - Useful untuk analytics

- [x] **Overdue Tracking**
  - Identify overdue books
  - Fine calculation system

- [x] **Book Relationships**
  - Similar books recommendation
  - Category-based grouping

- [x] **User Role Management**
  - Admin: Full access
  - Librarian: Book & transaction management
  - Member: Limited access

---

## 🧪 Running Tests

```bash
# Run semua tests
python -m pytest tests/test_system.py -v

# Run specific test class
python -m pytest tests/test_system.py::TestDataStructures -v
python -m pytest tests/test_system.py::TestAuthentication -v
python -m pytest tests/test_system.py::TestLibraryManager -v

# Run dengan coverage report
python -m pytest tests/test_system.py --cov=src --cov-report=html
```

---

## 📊 Data Structure Complexity

| Operation | Complexity | Implementation |
|-----------|-----------|-----------------|
| Add Book | O(log n) | BST insertion |
| Search Book | O(1) avg | Hash Table lookup |
| Get All Books | O(n) | BST inorder traversal |
| Process Borrow | O(log n) | BST + update |
| Get Recommendations | O(V+E) | Graph DFS |
| Process Queue | O(1) | Queue enqueue/dequeue |
| Undo/Redo | O(1) | Stack operations |

---

## 🔐 Security Features

✅ **Password Security**
- PBKDF2-SHA256 hashing
- 100,000 iterations
- Random 16-byte salt

✅ **Session Management**
- 64-character hex tokens
- Automatic expiration (1 hour default)
- Session validation

✅ **Rate Limiting**
- Max 5 failed login attempts
- 5-minute cooldown period

✅ **Data Validation**
- Input type checking
- Range validation
- Duplicate prevention

---

## 📈 System Statistics

Generate laporan comprehensive:
1. Total books & availability
2. User statistics
3. Transaction history
4. Fine collection
5. Rating analytics
6. Popular books
7. Category trends

---

## 💡 Usage Examples

### As a Member
1. Login dengan akun member
2. Cari buku yang diinginkan
3. Lihat detail buku
4. Ajukan peminjaman
5. Lihat transaksi saya
6. Beri rating & review

### As a Librarian
1. Login dengan akun librarian
2. Tambah buku baru ke sistem
3. Proses peminjaman dari member
4. Proses pengembalian buku
5. Kelola reservasi
6. Lihat laporan transaksi

### As an Admin
1. Login dengan akun admin
2. Kelola user accounts
3. Lihat statistik komprehensif
4. Monitor sistem
5. Generate reports

---

## 🐛 Troubleshooting

### Aplikasi tidak bisa start
```bash
# Check Python installation
python --version

# Check dependencies
pip list

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### GUI tidak muncul
- Pastikan Tkinter terinstall: `python -m tkinter`
- Restart aplikasi

### Data tidak tersimpan
- Check folder `data/` ada dan writable
- Check available disk space
- Lihat error messages di console

### Login failed
- Check username & password benar (case-sensitive)
- Tunggu 5 menit setelah 5x failed attempts

---

## 📚 Documentation

- **README.md**: Dokumentasi lengkap sistem
- **API.md**: API reference untuk developers
- **USER_MANUAL.md**: Panduan penggunaan
- **ARCHITECTURE.md**: Desain & arsitektur sistem
- **FEATURES_CHECKLIST.md**: Checklist requirements

---

## 🎯 Next Steps

1. Generate sample data: `python generate_sample_data.py`
2. Run aplikasi: `python main.py`
3. Login dengan credentials dari list di atas
4. Explore berbagai fitur
5. Lihat dokumentasi untuk detail lebih lanjut

---

## ✉️ Support

Jika ada pertanyaan atau issues:
1. Check dokumentasi di folder `docs/`
2. Review error messages di console
3. Check test cases untuk examples

---

**Last Updated**: December 4, 2024
**Version**: 1.0.0
**Status**: ✅ Complete & Ready to Deploy
