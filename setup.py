#!/usr/bin/env python3
"""
Installation & Setup Script untuk Sistem Perpustakaan Digital
Jalankan script ini untuk setup lengkap sistem
"""

import subprocess
import sys
import os
import shutil


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_step(number, text):
    """Print step"""
    print(f"\n[{number}] {text}...")


def check_python_version():
    """Check Python version"""
    print_step(1, "Checking Python version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, but found {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is OK")
    return True


def check_tkinter():
    """Check if Tkinter is available"""
    print_step(2, "Checking Tkinter availability")
    
    try:
        import tkinter
        print("✅ Tkinter is available")
        return True
    except ImportError:
        print("❌ Tkinter not found!")
        print("   On Windows: Tkinter is included with Python")
        print("   On Linux: sudo apt-get install python3-tk")
        print("   On macOS: Tkinter is included with Python")
        return False


def install_dependencies():
    """Install Python dependencies"""
    print_step(3, "Installing Python dependencies")
    
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"❌ {requirements_file} not found!")
        return False
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-q", "-r", requirements_file
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_data_directory():
    """Create data directory if not exists"""
    print_step(4, "Creating data directory")
    
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"✅ Created '{data_dir}' directory")
    else:
        print(f"✓ '{data_dir}' directory already exists")
    
    return True


def verify_project_structure():
    """Verify project structure"""
    print_step(5, "Verifying project structure")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "src/data_structures.py",
        "src/models.py",
        "src/auth.py",
        "src/library_manager.py",
        "src/persistence.py",
        "src/gui.py",
        "tests/test_system.py",
        "generate_sample_data.py",
        "docs/README.md",
        "docs/USER_MANUAL.md",
        "docs/API.md",
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print(f"✅ All {len(required_files)} required files found")
    return True


def generate_sample_data():
    """Ask user if they want to generate sample data"""
    print_step(6, "Sample data generation")
    
    response = input("\nWould you like to generate sample data? (y/n): ").strip().lower()
    
    if response == 'y':
        try:
            print("Generating sample data...")
            from generate_sample_data import generate_sample_data
            generate_sample_data()
            print("✅ Sample data generated successfully")
            return True
        except Exception as e:
            print(f"⚠️  Sample data generation failed: {e}")
            print("   You can run 'python generate_sample_data.py' later")
            return False
    else:
        print("⏭️  Sample data generation skipped")
        return True


def print_next_steps():
    """Print next steps"""
    print_header("SETUP COMPLETED!")
    
    print("""
✅ Installation and setup completed successfully!

📝 Next Steps:

1. Start the application:
   python main.py

2. Default login credentials (if sample data was generated):
   Admin:      admin / admin123456
   Librarian:  librarian / librarian123
   Member:     budi / budi123456

3. For detailed information, read:
   - QUICK_START.md          (Quick startup guide)
   - docs/USER_MANUAL.md     (Complete user guide)
   - docs/README.md          (Full documentation)

4. To run tests:
   python -m pytest tests/test_system.py -v

5. To generate sample data later:
   python generate_sample_data.py

📚 Documentation location: docs/

❓ For help, check the documentation or run:
   python main.py --help

""")


def main():
    """Main setup function"""
    print_header("SISTEM PERPUSTAKAAN DIGITAL - SETUP")
    
    steps = [
        ("Python version", check_python_version),
        ("Tkinter", check_tkinter),
        ("Dependencies", install_dependencies),
        ("Data directory", create_data_directory),
        ("Project structure", verify_project_structure),
        ("Sample data", generate_sample_data),
    ]
    
    for title, func in steps:
        try:
            if not func():
                print(f"\n⚠️  Setup warning: {title} check failed")
                if title in ["Python version", "Tkinter", "Dependencies", "Project structure"]:
                    print("❌ Setup cannot continue!")
                    return False
        except Exception as e:
            print(f"\n❌ Error during {title}: {e}")
            return False
    
    print_next_steps()
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
