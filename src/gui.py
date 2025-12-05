"""
Module GUI untuk Sistem Perpustakaan Digital
Menggunakan Tkinter untuk membuat antarmuka pengguna
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
from tkcalendar import DateEntry
from datetime import datetime
import uuid
from typing import Optional

from src.library_manager import LibraryManager
from src.auth import AuthenticationManager
from src.persistence import DataPersistence
from src.models import Book, BookStatus, UserRole


class LibraryGUI:
    """Main GUI class untuk Sistem Perpustakaan Digital"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sistem Perpustakaan Digital")
        self.root.geometry("1000x700")
        
        # Initialize managers
        self.library_manager = LibraryManager()
        self.auth_manager = AuthenticationManager()
        self.persistence = DataPersistence()
        
        # Load data
        self.persistence.load_all(self.library_manager, self.auth_manager)
        
        # Current user session
        self.current_user = None
        self.current_session_id = None
        self.current_user_role = None
        
        # Create login frame
        self.create_login_frame()

    def create_login_frame(self):
        """Create frame untuk login"""
        self.clear_frame()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)
        
        # Title
        title = ttk.Label(frame, text="Sistem Perpustakaan Digital", 
                         font=("Helvetica", 24, "bold"))
        title.pack(pady=20)
        
        # Login form
        form_frame = ttk.LabelFrame(frame, text="Login", padding="10")
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Username
        ttk.Label(form_frame, text="Username:").pack(pady=5)
        username_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=username_var, width=40)
        username_entry.pack(pady=5)
        
        # Password
        ttk.Label(form_frame, text="Password:").pack(pady=5)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=password_var, 
                                   show="*", width=40)
        password_entry.pack(pady=5)
        
        # Login button
        def login_action():
            username = username_var.get()
            password = password_var.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Username dan password harus diisi")
                return
            
            # Debug: Check if user exists
            user_check = self.auth_manager.users.search(username)
            if user_check is None:
                messagebox.showerror("Debug Info", f"User '{username}' tidak ditemukan di database.\n\nAvailable users:\n" + 
                                   "\n".join([f"- {u[0]}" for u in self.auth_manager.users.get_all()]))
                return
            
            success, message, session_id = self.auth_manager.login(username, password)
            if success:
                user = self.auth_manager.get_user(username)
                self.current_user = user
                self.current_session_id = session_id
                self.current_user_role = user.role
                messagebox.showinfo("Success", message)
                self.create_main_menu()
            else:
                messagebox.showerror("Login Failed", message)
        
        login_btn = ttk.Button(form_frame, text="Login", command=login_action)
        login_btn.pack(pady=10)
        
        # Register button
        def register_action():
            self.create_register_frame()
        
        register_btn = ttk.Button(form_frame, text="Registrasi Member Baru", 
                                 command=register_action)
        register_btn.pack(pady=5)

    def create_register_frame(self):
        """Create frame untuk registrasi"""
        self.clear_frame()
        
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill="both")
        
        # Title
        title = ttk.Label(frame, text="Registrasi Member Baru", 
                         font=("Helvetica", 20, "bold"))
        title.pack(pady=20)
        
        # Form
        form_frame = ttk.Frame(frame)
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Create variables
        vars_dict = {}
        fields = [
            ("Username", "username"),
            ("Password", "password"),
            ("Nama Lengkap", "full_name"),
            ("Email", "email"),
            ("Nomor Telepon", "phone"),
            ("Alamat", "address")
        ]
        
        for label, key in fields:
            ttk.Label(form_frame, text=f"{label}:").pack(pady=5)
            var = tk.StringVar()
            vars_dict[key] = var
            
            if key == "password":
                entry = ttk.Entry(form_frame, textvariable=var, show="*", width=40)
            elif key == "address":
                entry = tk.Text(form_frame, height=3, width=40)
                entry.pack(pady=5)
                vars_dict[key] = entry
                continue
            else:
                entry = ttk.Entry(form_frame, textvariable=var, width=40)
            
            entry.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)
        
        def register_submit():
            try:
                username = vars_dict["username"].get()
                password = vars_dict["password"].get()
                full_name = vars_dict["full_name"].get()
                email = vars_dict["email"].get()
                phone = vars_dict["phone"].get()
                address = vars_dict["address"].get("1.0", "end-1c")
                
                if not all([username, password, full_name, email, phone, address]):
                    messagebox.showerror("Error", "Semua field harus diisi")
                    return
                
                user_id = str(uuid.uuid4())[:8]
                success, message = self.auth_manager.register_user(
                    username, password, full_name, email, phone, address, user_id
                )
                
                if success:
                    messagebox.showinfo("Success", message)
                    self.create_login_frame()
                else:
                    messagebox.showerror("Error", message)
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
        
        ttk.Button(button_frame, text="Registrasi", 
                  command=register_submit).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Kembali", 
                  command=self.create_login_frame).pack(side="left", padx=5)

    def create_main_menu(self):
        """Create main menu setelah login"""
        self.clear_frame()
        
        frame = ttk.Frame(self.root, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Header
        header = ttk.Frame(frame)
        header.pack(fill="x", pady=10)
        
        ttk.Label(header, text=f"Selamat datang, {self.current_user.full_name}!", 
                 font=("Helvetica", 16, "bold")).pack(side="left")
        ttk.Label(header, text=f"({self.current_user_role})", 
                 font=("Helvetica", 12)).pack(side="left", padx=10)
        
        # Logout button
        def logout_action():
            self.auth_manager.logout(self.current_session_id)
            self.current_user = None
            self.current_session_id = None
            self.current_user_role = None
            self.create_login_frame()
        
        ttk.Button(header, text="Logout", command=logout_action).pack(side="right")
        
        # Menu buttons
        menu_frame = ttk.LabelFrame(frame, text="Menu Utama", padding="10")
        menu_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        buttons = []
        
        # Common menu
        buttons.append(("Cari Buku", self.open_search_books))
        buttons.append(("Lihat Daftar Buku", self.open_book_list))
        buttons.append(("Buku Rekomendasi", self.open_recommendations))
        buttons.append(("Lihat Transaksi Saya", self.open_my_transactions))
        
        if self.current_user_role in [UserRole.LIBRARIAN.value, UserRole.ADMIN.value]:
            buttons.append(("--- LIBRARIAN MENU ---", None))
            buttons.append(("Tambah Buku", self.open_add_book))
            buttons.append(("Kelola Buku", self.open_manage_books))
            buttons.append(("Proses Peminjaman", self.open_borrow_book))
            buttons.append(("Proses Pengembalian", self.open_return_book))
            buttons.append(("Kelola Reservasi", self.open_manage_reservations))
        
        if self.current_user_role == UserRole.ADMIN.value:
            buttons.append(("--- ADMIN MENU ---", None))
            buttons.append(("Kelola User", self.open_manage_users))
            buttons.append(("Statistik & Laporan", self.open_statistics))
        
        # Member menu
        if self.current_user_role == UserRole.MEMBER.value:
            buttons.append(("Ajukan Peminjaman", self.open_request_borrow))
            buttons.append(("Lihat Reservasi Saya", self.open_my_reservations))
            buttons.append(("Beri Rating & Review", self.open_add_review))
        
        # Create buttons
        for i, (text, command) in enumerate(buttons):
            if command is None:
                # Separator
                ttk.Label(menu_frame, text=text, 
                         font=("Helvetica", 10, "bold")).grid(row=i, column=0, columnspan=2, 
                                                              sticky="ew", pady=10)
            else:
                btn = ttk.Button(menu_frame, text=text, command=command, width=30)
                btn.grid(row=i, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    def open_search_books(self):
        """Search books window"""
        search_window = tk.Toplevel(self.root)
        search_window.title("Cari Buku")
        search_window.geometry("500x400")
        
        frame = ttk.Frame(search_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Search criteria
        ttk.Label(frame, text="Judul:").pack(pady=5)
        title_var = tk.StringVar()
        ttk.Entry(frame, textvariable=title_var, width=40).pack(pady=5)
        
        ttk.Label(frame, text="Author:").pack(pady=5)
        author_var = tk.StringVar()
        ttk.Entry(frame, textvariable=author_var, width=40).pack(pady=5)
        
        ttk.Label(frame, text="Kategori:").pack(pady=5)
        category_var = tk.StringVar()
        ttk.Entry(frame, textvariable=category_var, width=40).pack(pady=5)
        
        def search_action():
            results = self.library_manager.search_books_multi_criteria(
                title=title_var.get(),
                author=author_var.get(),
                category=category_var.get()
            )
            
            # Clear previous results
            for widget in results_frame.winfo_children():
                widget.destroy()
            
            if not results:
                ttk.Label(results_frame, text="Tidak ada hasil pencarian").pack(pady=10)
            else:
                for book in results:
                    book_text = f"{book.title} by {book.author} ({book.publication_year})\n" \
                               f"Tersedia: {book.available_copies}/{book.total_copies} | " \
                               f"Rating: {book.rating:.1f}★"
                    
                    book_frame = ttk.LabelFrame(results_frame, text=book.book_id, padding="5")
                    book_frame.pack(fill="x", pady=5)
                    
                    ttk.Label(book_frame, text=book_text, wraplength=400, justify="left").pack()
                    
                    if book.available_copies > 0:
                        ttk.Button(book_frame, text="Pinjam", 
                                  command=lambda b=book: self.quick_borrow(b.book_id)).pack()
                    
                    ttk.Button(book_frame, text="Lihat Detail", 
                              command=lambda b=book: self.show_book_detail(b)).pack()
        
        ttk.Button(frame, text="Cari", command=search_action).pack(pady=10)
        
        # Results area
        ttk.Label(frame, text="Hasil Pencarian:", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill="both", expand=True)

    def open_book_list(self):
        """Show list of all books"""
        list_window = tk.Toplevel(self.root)
        list_window.title("Daftar Buku")
        list_window.geometry("800x500")
        
        frame = ttk.Frame(list_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Create treeview
        tree = ttk.Treeview(frame, columns=("ID", "Judul", "Author", "Kategori", "Tersedia", "Rating"),
                           height=15)
        tree.heading("#0", text="No")
        tree.heading("ID", text="Book ID")
        tree.heading("Judul", text="Judul")
        tree.heading("Author", text="Author")
        tree.heading("Kategori", text="Kategori")
        tree.heading("Tersedia", text="Tersedia")
        tree.heading("Rating", text="Rating")
        
        tree.column("#0", width=30)
        tree.column("ID", width=60)
        tree.column("Judul", width=150)
        tree.column("Author", width=100)
        tree.column("Kategori", width=80)
        tree.column("Tersedia", width=60)
        tree.column("Rating", width=50)
        
        # Add books
        books = self.library_manager.get_all_books()
        for idx, (book_id, book) in enumerate(books, 1):
            tree.insert("", "end", text=str(idx),
                       values=(book_id, book.title, book.author, book.category,
                              f"{book.available_copies}/{book.total_copies}", f"{book.rating:.1f}"))
        
        tree.pack(fill="both", expand=True, pady=10)

    def show_book_detail(self, book: Book):
        """Show detailed book information"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Detail Buku: {book.title}")
        detail_window.geometry("500x600")
        
        frame = ttk.Frame(detail_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        details = [
            f"Judul: {book.title}",
            f"Author: {book.author}",
            f"Publisher: {book.publisher}",
            f"ISBN: {book.isbn}",
            f"Tahun Publikasi: {book.publication_year}",
            f"Kategori: {book.category}",
            f"Halaman: {book.pages}",
            f"Bahasa: {book.language}",
            f"Total Salinan: {book.total_copies}",
            f"Tersedia: {book.available_copies}",
            f"Rating: {book.rating:.1f}★",
            f"Jumlah Peminjaman: {book.borrow_count}",
            f"Status: {book.status}",
            f"\nDeskripsi:\n{book.description}"
        ]
        
        text = "\n".join(details)
        text_widget = tk.Text(frame, height=20, width=50, wrap="word")
        text_widget.insert("1.0", text)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True)

    def quick_borrow(self, book_id: str):
        """Quick borrow action"""
        if self.current_user_role != UserRole.MEMBER.value:
            messagebox.showerror("Error", "Hanya member yang dapat meminjam")
            return
        
        success, message, trans_id = self.library_manager.borrow_book(
            self.current_user.user_id, book_id
        )
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def open_recommendations(self):
        """Show book recommendations"""
        rec_window = tk.Toplevel(self.root)
        rec_window.title("Rekomendasi Buku")
        rec_window.geometry("600x400")
        
        frame = ttk.Frame(rec_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Buku Populer", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        popular = self.library_manager.get_popular_books(10)
        for book in popular:
            ttk.Label(frame, text=f"• {book.title} - {book.author}\n  Rating: {book.rating}★ | Dipinjam: {book.borrow_count}x",
                     wraplength=500, justify="left").pack(pady=5)

    def open_my_transactions(self):
        """Show user's transactions"""
        trans_window = tk.Toplevel(self.root)
        trans_window.title("Transaksi Saya")
        trans_window.geometry("700x400")
        
        frame = ttk.Frame(trans_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        transactions = self.library_manager.get_user_transactions(self.current_user.user_id)
        
        tree = ttk.Treeview(frame, columns=("Tipe", "Buku", "Tanggal", "Deadline", "Status"),
                           height=15)
        tree.heading("#0", text="ID Transaksi")
        tree.heading("Tipe", text="Tipe")
        tree.heading("Buku", text="Buku")
        tree.heading("Tanggal", text="Tanggal")
        tree.heading("Deadline", text="Deadline")
        tree.heading("Status", text="Status")
        
        for trans in transactions:
            book = self.library_manager.get_book(trans.book_id)
            book_title = book.title if book else "Unknown"
            tree.insert("", "end", text=trans.transaction_id,
                       values=(trans.transaction_type, book_title,
                              trans.transaction_date[:10], 
                              trans.due_date[:10] if trans.due_date else "-",
                              trans.status))
        
        tree.pack(fill="both", expand=True, pady=10)

    def open_add_book(self):
        """Add new book (librarian/admin)"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Tambah Buku")
        add_window.geometry("500x600")
        
        frame = ttk.Frame(add_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        vars_dict = {}
        fields = [
            ("Judul", "title", "entry"),
            ("Author", "author", "entry"),
            ("Publisher", "publisher", "entry"),
            ("ISBN", "isbn", "entry"),
            ("Tahun Publikasi", "publication_year", "entry"),
            ("Kategori", "category", "entry"),
            ("Lokasi", "location", "entry"),
            ("Total Salinan", "total_copies", "entry"),
            ("Halaman", "pages", "entry"),
            ("Deskripsi", "description", "text")
        ]
        
        for label, key, type_ in fields:
            ttk.Label(frame, text=f"{label}:").pack(pady=5)
            
            if type_ == "text":
                var = tk.Text(frame, height=3, width=40)
                var.pack(pady=5)
                vars_dict[key] = var
            else:
                var = tk.StringVar()
                ttk.Entry(frame, textvariable=var, width=40).pack(pady=5)
                vars_dict[key] = var
        
        def add_book_action():
            try:
                book_id = str(uuid.uuid4())[:8]
                book = Book(
                    book_id=book_id,
                    title=vars_dict["title"].get(),
                    author=vars_dict["author"].get(),
                    publisher=vars_dict["publisher"].get(),
                    isbn=vars_dict["isbn"].get(),
                    publication_year=int(vars_dict["publication_year"].get()),
                    category=vars_dict["category"].get(),
                    total_copies=int(vars_dict["total_copies"].get()),
                    available_copies=int(vars_dict["total_copies"].get()),
                    location=vars_dict["location"].get(),
                    description=vars_dict["description"].get("1.0", "end-1c"),
                    pages=int(vars_dict["pages"].get() or 0)
                )
                
                success, message = self.library_manager.add_book(book)
                if success:
                    messagebox.showinfo("Success", message)
                    add_window.destroy()
                else:
                    messagebox.showerror("Error", message)
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")
        
        ttk.Button(frame, text="Tambah Buku", command=add_book_action).pack(pady=10)

    def open_manage_books(self):
        """Manage existing books"""
        manage_window = tk.Toplevel(self.root)
        manage_window.title("Kelola Buku")
        manage_window.geometry("900x550")
        
        frame = ttk.Frame(manage_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        # Title
        ttk.Label(frame, text="Manajemen Buku", font=("Arial", 12, "bold")).pack(pady=5)
        
        books = self.library_manager.get_all_books()
        
        tree = ttk.Treeview(frame, columns=("Judul", "Author", "Tersedia", "Total", "Kategori"),
                           height=15)
        tree.heading("#0", text="Book ID")
        tree.heading("Judul", text="Judul")
        tree.heading("Author", text="Author")
        tree.heading("Tersedia", text="Tersedia")
        tree.heading("Total", text="Total")
        tree.heading("Kategori", text="Kategori")
        
        for book_id, book in books:
            tree.insert("", "end", text=book_id,
                       values=(book.title, book.author,
                              book.available_copies, book.total_copies, book.category))
        
        tree.pack(fill="both", expand=True, pady=10)
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=10)
        
        def edit_selected_book():
            """Edit selected book"""
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Pilih buku terlebih dahulu")
                return
            
            book_id = tree.item(selection[0])['text']
            book = self.library_manager.get_book(book_id)
            
            if book is None:
                messagebox.showerror("Error", "Buku tidak ditemukan")
                return
            
            # Create edit window
            edit_window = tk.Toplevel(manage_window)
            edit_window.title(f"Edit Buku - {book_id}")
            edit_window.geometry("500x450")
            
            edit_frame = ttk.Frame(edit_window, padding="15")
            edit_frame.pack(fill="both", expand=True)
            
            # Form fields
            ttk.Label(edit_frame, text="Judul:").pack(anchor="w", pady=5)
            title_var = tk.StringVar(value=book.title)
            ttk.Entry(edit_frame, textvariable=title_var, width=50).pack(anchor="w", pady=2)
            
            ttk.Label(edit_frame, text="Author:").pack(anchor="w", pady=5)
            author_var = tk.StringVar(value=book.author)
            ttk.Entry(edit_frame, textvariable=author_var, width=50).pack(anchor="w", pady=2)
            
            ttk.Label(edit_frame, text="Kategori:").pack(anchor="w", pady=5)
            category_var = tk.StringVar(value=book.category)
            ttk.Entry(edit_frame, textvariable=category_var, width=50).pack(anchor="w", pady=2)
            
            ttk.Label(edit_frame, text="ISBN:").pack(anchor="w", pady=5)
            isbn_var = tk.StringVar(value=book.isbn)
            ttk.Entry(edit_frame, textvariable=isbn_var, width=50).pack(anchor="w", pady=2)
            
            ttk.Label(edit_frame, text="Tahun Terbit:").pack(anchor="w", pady=5)
            year_var = tk.StringVar(value=str(book.year))
            ttk.Entry(edit_frame, textvariable=year_var, width=50).pack(anchor="w", pady=2)
            
            ttk.Label(edit_frame, text="Total Copies:").pack(anchor="w", pady=5)
            total_var = tk.StringVar(value=str(book.total_copies))
            ttk.Entry(edit_frame, textvariable=total_var, width=50).pack(anchor="w", pady=2)
            
            ttk.Label(edit_frame, text="Deskripsi:").pack(anchor="w", pady=5)
            desc_var = tk.StringVar(value=book.description)
            desc_text = scrolledtext.ScrolledText(edit_frame, width=50, height=5)
            desc_text.insert("1.0", book.description)
            desc_text.pack(anchor="w", pady=2)
            
            def save_changes():
                """Save changes to book"""
                try:
                    success, message = self.library_manager.update_book(
                        book_id,
                        title=title_var.get(),
                        author=author_var.get(),
                        category=category_var.get(),
                        isbn=isbn_var.get(),
                        year=int(year_var.get()),
                        total_copies=int(total_var.get()),
                        description=desc_text.get("1.0", "end-1c")
                    )
                    
                    if success:
                        messagebox.showinfo("Success", message)
                        self.persistence.save_all(self.library_manager, self.auth_manager)
                        edit_window.destroy()
                        manage_window.destroy()
                        self.open_manage_books()  # Refresh
                    else:
                        messagebox.showerror("Error", message)
                except ValueError:
                    messagebox.showerror("Error", "Tahun dan Total Copies harus berupa angka")
            
            # Save button
            ttk.Button(edit_frame, text="Simpan Perubahan", command=save_changes).pack(pady=10, fill="x")
        
        def delete_selected_book():
            """Delete selected book"""
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Pilih buku terlebih dahulu")
                return
            
            book_id = tree.item(selection[0])['text']
            
            # Confirmation dialog
            if messagebox.askyesno("Konfirmasi", f"Hapus buku {book_id}?\nIni tidak dapat dibatalkan!"):
                success, message = self.library_manager.delete_book(book_id)
                
                if success:
                    messagebox.showinfo("Success", message)
                    self.persistence.save_all(self.library_manager, self.auth_manager)
                    manage_window.destroy()
                    self.open_manage_books()  # Refresh
                else:
                    messagebox.showerror("Error", message)
        
        ttk.Button(button_frame, text="Edit Buku", command=edit_selected_book).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hapus Buku", command=delete_selected_book).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Tutup", command=manage_window.destroy).pack(side="right", padx=5)

    def open_borrow_book(self):
        """Process book borrowing (librarian)"""
        borrow_window = tk.Toplevel(self.root)
        borrow_window.title("Proses Peminjaman")
        borrow_window.geometry("400x200")
        
        frame = ttk.Frame(borrow_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="User ID:").pack(pady=5)
        user_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=user_id_var, width=40).pack(pady=5)
        
        ttk.Label(frame, text="Book ID:").pack(pady=5)
        book_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=book_id_var, width=40).pack(pady=5)
        
        def process_borrow():
            success, message, trans_id = self.library_manager.borrow_book(
                user_id_var.get(), book_id_var.get()
            )
            
            if success:
                messagebox.showinfo("Success", message)
                self.persistence.save_all(self.library_manager, self.auth_manager)
            else:
                messagebox.showerror("Error", message)
        
        ttk.Button(frame, text="Proses Peminjaman", command=process_borrow).pack(pady=10)

    def open_return_book(self):
        """Process book return (librarian)"""
        return_window = tk.Toplevel(self.root)
        return_window.title("Proses Pengembalian")
        return_window.geometry("400x200")
        
        frame = ttk.Frame(return_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Transaction ID:").pack(pady=5)
        trans_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=trans_id_var, width=40).pack(pady=5)
        
        def process_return():
            success, message, fine = self.library_manager.return_book(trans_id_var.get())
            
            if success:
                messagebox.showinfo("Success", f"{message}\nDenda: Rp {fine:,.0f}")
                self.persistence.save_all(self.library_manager, self.auth_manager)
            else:
                messagebox.showerror("Error", message)
        
        ttk.Button(frame, text="Proses Pengembalian", command=process_return).pack(pady=10)

    def open_manage_reservations(self):
        """Manage book reservations"""
        res_window = tk.Toplevel(self.root)
        res_window.title("Kelola Reservasi")
        res_window.geometry("700x400")
        
        frame = ttk.Frame(res_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        reservations = self.library_manager.reservation_list.get_all()
        
        tree = ttk.Treeview(frame, columns=("User", "Buku", "Tanggal", "Status"),
                           height=15)
        tree.heading("#0", text="ID Reservasi")
        tree.heading("User", text="User ID")
        tree.heading("Buku", text="Book ID")
        tree.heading("Tanggal", text="Tanggal")
        tree.heading("Status", text="Status")
        
        for res in reservations:
            tree.insert("", "end", text=res.reservation_id,
                       values=(res.user_id, res.book_id,
                              res.reservation_date[:10], res.status))
        
        tree.pack(fill="both", expand=True, pady=10)

    def open_manage_users(self):
        """Manage users (admin)"""
        users_window = tk.Toplevel(self.root)
        users_window.title("Kelola User")
        users_window.geometry("800x500")
        
        frame = ttk.Frame(users_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        all_users = self.auth_manager.get_all_users()
        
        tree = ttk.Treeview(frame, columns=("Nama", "Email", "Role", "Aktif"),
                           height=15)
        tree.heading("#0", text="Username")
        tree.heading("Nama", text="Nama")
        tree.heading("Email", text="Email")
        tree.heading("Role", text="Role")
        tree.heading("Aktif", text="Aktif")
        
        for username, user in all_users.items():
            tree.insert("", "end", text=username,
                       values=(user.full_name, user.email, user.role,
                              "Ya" if user.is_active else "Tidak"))
        
        tree.pack(fill="both", expand=True, pady=10)

    def open_statistics(self):
        """Show statistics and reports (admin)"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Statistik & Laporan")
        stats_window.geometry("600x500")
        
        frame = ttk.Frame(stats_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        stats = self.library_manager.generate_statistics()
        
        stats_text = f"""
STATISTIK PERPUSTAKAAN
{'='*50}

Total Buku: {stats.total_books}
Buku Tersedia: {stats.available_books}
Buku Dipinjam: {stats.borrowed_books}

Total Transaksi: {stats.total_transactions}
Total Denda: Rp {stats.total_fines:,.0f}

Rating Rata-rata: {stats.average_rating:.1f}★
Buku Paling Banyak Dipinjam: {stats.most_borrowed_book}
Kategori Paling Populer: {stats.most_borrowed_category}

Tanggal Generate: {stats.generated_date[:10]}
        """
        
        text_widget = tk.Text(frame, height=20, width=60, wrap="word")
        text_widget.insert("1.0", stats_text)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True)

    def open_request_borrow(self):
        """Member request to borrow book"""
        # Similar to open_borrow_book but for members
        self.open_book_list()

    def open_my_reservations(self):
        """Show member's reservations"""
        res_window = tk.Toplevel(self.root)
        res_window.title("Reservasi Saya")
        res_window.geometry("600x300")
        
        frame = ttk.Frame(res_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        reservations = self.library_manager.get_user_reservations(self.current_user.user_id)
        
        if not reservations:
            ttk.Label(frame, text="Anda tidak memiliki reservasi").pack(pady=20)
        else:
            tree = ttk.Treeview(frame, columns=("Buku", "Tanggal", "Status"),
                               height=10)
            tree.heading("#0", text="ID Reservasi")
            tree.heading("Buku", text="Book ID")
            tree.heading("Tanggal", text="Tanggal")
            tree.heading("Status", text="Status")
            
            for res in reservations:
                tree.insert("", "end", text=res.reservation_id,
                           values=(res.book_id, res.reservation_date[:10], res.status))
            
            tree.pack(fill="both", expand=True, pady=10)

    def open_add_review(self):
        """Add review for a book"""
        review_window = tk.Toplevel(self.root)
        review_window.title("Beri Rating & Review")
        review_window.geometry("500x400")
        
        frame = ttk.Frame(review_window, padding="10")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Book ID:").pack(pady=5)
        book_id_var = tk.StringVar()
        ttk.Entry(frame, textvariable=book_id_var, width=40).pack(pady=5)
        
        ttk.Label(frame, text="Rating (1-5):").pack(pady=5)
        rating_var = tk.IntVar(value=5)
        rating_spinbox = ttk.Spinbox(frame, from_=1, to=5, textvariable=rating_var, width=10)
        rating_spinbox.pack(pady=5)
        
        ttk.Label(frame, text="Review:").pack(pady=5)
        review_text = tk.Text(frame, height=8, width=40)
        review_text.pack(pady=5)
        
        def submit_review():
            book_id = book_id_var.get()
            rating = rating_var.get()
            review = review_text.get("1.0", "end-1c")
            
            success, message = self.library_manager.add_review(
                self.current_user.user_id, book_id, rating, review
            )
            
            if success:
                messagebox.showinfo("Success", message)
                review_window.destroy()
                self.persistence.save_all(self.library_manager, self.auth_manager)
            else:
                messagebox.showerror("Error", message)
        
        ttk.Button(frame, text="Submit Review", command=submit_review).pack(pady=10)

    def clear_frame(self):
        """Clear all widgets from root frame"""
        for widget in self.root.winfo_children():
            widget.destroy()


def main():
    """Main function untuk menjalankan aplikasi"""
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
