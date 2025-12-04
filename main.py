"""
Sistem Perpustakaan Digital - Main Entry Point
Mengintegrasikan semua modul untuk sistem perpustakaan yang lengkap
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui import main


if __name__ == "__main__":
    main()
