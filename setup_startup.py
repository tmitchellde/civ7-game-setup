import os
import subprocess
import sys

# Define project root directory
PROJECT_ROOT = os.path.abspath(os.getcwd())
ENV_DIR = os.path.join(PROJECT_ROOT, "env")
DJANGO_MANAGE = os.path.join(PROJECT_ROOT, "manage.py")

# Step 1: Check if Virtual Environment Exists, If Not, Create It
def setup_virtualenv():
    if not os.path.exists(ENV_DIR):
        print("🔹 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "env"], check=True)
        print("✅ Virtual environment created.")
    else:
        print("✅ Virtual environment already exists.")

# Step 2: Install Dependencies
def install_dependencies():
    print("🔹 Activating virtual environment and installing dependencies...")

    # Activate Virtual Environment
    env_python = os.path.join(ENV_DIR, "Scripts", "python.exe") if sys.platform == "win32" else os.path.join(ENV_DIR, "bin", "python")

    # Upgrade pip
    subprocess.run([env_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)

    # Install Django & Dependencies
    subprocess.run([env_python, "-m", "pip", "install", "django", "djangorestframework"], check=True)

    print("✅ Dependencies installed successfully.")

# Step 3: Run Migrations
def run_migrations():
    print("🔹 Running Django migrations...")
    env_python = os.path.join(ENV_DIR, "Scripts", "python.exe") if sys.platform == "win32" else os.path.join(ENV_DIR, "bin", "python")
    
    subprocess.run([env_python, DJANGO_MANAGE, "migrate"], check=True)
    print("✅ Migrations completed.")

# Step 4: Start Django Development Server
def start_server():
    print("🚀 Starting Django server at http://127.0.0.1:8000/ ...")
    env_python = os.path.join(ENV_DIR, "Scripts", "python.exe") if sys.platform == "win32" else os.path.join(ENV_DIR, "bin", "python")
    
    subprocess.run([env_python, DJANGO_MANAGE, "runserver"])

# Run All Setup Steps
def main():
    setup_virtualenv()
    install_dependencies()
    run_migrations()
    start_server()

if __name__ == "__main__":
    main()
