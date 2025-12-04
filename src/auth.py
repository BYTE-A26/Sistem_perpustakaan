"""
Module Autentikasi untuk Sistem Perpustakaan Digital
Menangani user authentication dengan secure password hashing
"""

import hashlib
import secrets
from typing import Optional, Tuple
from datetime import datetime, timedelta
from src.data_structures import HashTable
from src.models import User, UserRole


class AuthenticationManager:
    """
    Manager untuk autentikasi user
    Menggunakan Hash Table untuk menyimpan user data
    """
    
    def __init__(self):
        self.users: HashTable = HashTable(capacity=200)
        self.sessions: dict = {}  # session_id -> (user_id, expiry_time)
        self.failed_login_attempts: dict = {}  # username -> (count, last_attempt_time)

    def hash_password(self, password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """
        Hash password menggunakan PBKDF2
        Returns: (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_hex(16)
        
        # PBKDF2 with SHA256
        hash_object = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        )
        hashed = hash_object.hex()
        return hashed, salt

    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """
        Verify password dengan stored hash
        """
        hashed, _ = self.hash_password(password, salt)
        return hashed == stored_hash

    def register_user(self, username: str, password: str, full_name: str, 
                     email: str, phone: str, address: str, 
                     user_id: str, role: str = UserRole.MEMBER.value) -> Tuple[bool, str]:
        """
        Register user baru
        Returns: (success, message)
        """
        # Validasi input
        if len(password) < 8:
            return False, "Password minimal 8 karakter"
        
        if self.users.search(username) is not None:
            return False, "Username sudah terdaftar"
        
        # Hash password
        password_hash, salt = self.hash_password(password)
        
        # Buat user baru
        user = User(
            user_id=user_id,
            username=username,
            password_hash=f"{password_hash}${salt}",
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            role=role,
            is_active=True
        )
        
        # Simpan ke hash table
        self.users.insert(username, user)
        
        return True, "Registrasi berhasil"

    def login(self, username: str, password: str, session_duration: int = 3600) -> Tuple[bool, str, Optional[str]]:
        """
        Login user
        session_duration: durasi session dalam detik (default 1 jam)
        Returns: (success, message, session_id)
        """
        # Check failed attempts (simple rate limiting)
        if username in self.failed_login_attempts:
            attempts, last_time = self.failed_login_attempts[username]
            if attempts >= 5:
                if (datetime.now() - last_time).seconds < 300:  # 5 menit cooldown
                    return False, "Terlalu banyak login gagal. Coba lagi dalam 5 menit", None
            else:
                self.failed_login_attempts[username] = (attempts + 1, datetime.now())
        
        # Cari user
        user = self.users.search(username)
        if user is None:
            self.failed_login_attempts[username] = (1, datetime.now())
            return False, "Username atau password salah", None
        
        # Verify password
        try:
            password_hash, salt = user.password_hash.split('$')
            if not self.verify_password(password, password_hash, salt):
                self.failed_login_attempts[username] = (1, datetime.now())
                return False, "Username atau password salah", None
        except Exception as e:
            return False, f"Error verifikasi: {str(e)}", None
        
        # Check user active
        if not user.is_active:
            return False, "User tidak aktif", None
        
        # Create session
        session_id = secrets.token_hex(32)
        expiry_time = datetime.now() + timedelta(seconds=session_duration)
        self.sessions[session_id] = (user.user_id, expiry_time)
        
        # Clear failed attempts
        if username in self.failed_login_attempts:
            del self.failed_login_attempts[username]
        
        return True, "Login berhasil", session_id

    def logout(self, session_id: str) -> bool:
        """Logout user"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def validate_session(self, session_id: str) -> Tuple[bool, Optional[str]]:
        """
        Validate session
        Returns: (is_valid, user_id)
        """
        if session_id not in self.sessions:
            return False, None
        
        user_id, expiry_time = self.sessions[session_id]
        
        if datetime.now() > expiry_time:
            del self.sessions[session_id]
            return False, None
        
        return True, user_id

    def change_password(self, username: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        """Change password user"""
        user = self.users.search(username)
        if user is None:
            return False, "User tidak ditemukan"
        
        # Verify old password
        try:
            password_hash, salt = user.password_hash.split('$')
            if not self.verify_password(old_password, password_hash, salt):
                return False, "Password lama tidak sesuai"
        except Exception as e:
            return False, f"Error verifikasi: {str(e)}"
        
        # Validate new password
        if len(new_password) < 8:
            return False, "Password baru minimal 8 karakter"
        
        if old_password == new_password:
            return False, "Password baru harus berbeda dengan password lama"
        
        # Hash new password
        new_hash, new_salt = self.hash_password(new_password)
        user.password_hash = f"{new_hash}${new_salt}"
        
        # Update user
        self.users.insert(username, user)
        
        return True, "Password berhasil diubah"

    def get_user(self, username: str) -> Optional[User]:
        """Get user data"""
        return self.users.search(username)

    def get_all_users(self) -> dict:
        """Get semua user"""
        return self.users.get_all()

    def update_user(self, username: str, **kwargs) -> Tuple[bool, str]:
        """Update user data (kecuali password)"""
        user = self.users.search(username)
        if user is None:
            return False, "User tidak ditemukan"
        
        # Update fields
        for key, value in kwargs.items():
            if key != 'password_hash' and hasattr(user, key):
                setattr(user, key, value)
        
        self.users.insert(username, user)
        return True, "User berhasil diupdate"

    def deactivate_user(self, username: str) -> Tuple[bool, str]:
        """Deactivate user account"""
        user = self.users.search(username)
        if user is None:
            return False, "User tidak ditemukan"
        
        user.is_active = False
        self.users.insert(username, user)
        
        # Logout semua session user ini
        sessions_to_remove = [sid for sid, (uid, _) in self.sessions.items() if uid == user.user_id]
        for sid in sessions_to_remove:
            del self.sessions[sid]
        
        return True, "User berhasil dinonaktifkan"

    def activate_user(self, username: str) -> Tuple[bool, str]:
        """Activate user account"""
        user = self.users.search(username)
        if user is None:
            return False, "User tidak ditemukan"
        
        user.is_active = True
        self.users.insert(username, user)
        return True, "User berhasil diaktifkan"
