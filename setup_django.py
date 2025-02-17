import os
import shutil
import subprocess

# Define project root
PROJECT_ROOT = os.path.abspath(os.getcwd())  # C:\Repos\civ7-game-setup

# Define folders
DJANGO_PROJECT = os.path.join(PROJECT_ROOT, "civ7_picker")  # Django project folder
DJANGO_APP = os.path.join(PROJECT_ROOT, "picker")  # Django app folder
CLI_FOLDER = os.path.join(PROJECT_ROOT, "cli")  # CLI scripts folder
DATA_FOLDER = os.path.join(PROJECT_ROOT, "data")  # Data storage folder
SCRIPTS_FOLDER = os.path.join(DJANGO_APP, "scripts")  # Shared logic

# Step 1: Set up virtual environment
def setup_virtualenv():
    print("🔹 Setting up virtual environment...")
    subprocess.run(["python", "-m", "venv", "env"], check=True)
    print("✅ Virtual environment created.")

# Step 2: Install Django and Dependencies
def install_django():
    print("🔹 Installing Django & dependencies...")
    subprocess.run(["env\\Scripts\\pip", "install", "django", "djangorestframework"], check=True)
    print("✅ Django installed.")

# Step 3: Create Django Project & App
def setup_django_project():
    if not os.path.exists(DJANGO_PROJECT):
        print("🔹 Creating Django project...")
        subprocess.run(["env\\Scripts\\django-admin", "startproject", "civ7_picker", "."], check=True)
        print("✅ Django project created.")

    if not os.path.exists(DJANGO_APP):
        print("🔹 Creating Django app 'picker'...")
        subprocess.run(["env\\Scripts\\python", "manage.py", "startapp", "picker"], check=True)
        print("✅ Django app created.")

# Step 4: Move CLI script to `cli/`
def move_cli_script():
    os.makedirs(CLI_FOLDER, exist_ok=True)
    cli_script = os.path.join(PROJECT_ROOT, "game_picker.py")
    if os.path.exists(cli_script):
        print("🔹 Moving CLI script to 'cli/'...")
        shutil.move(cli_script, os.path.join(CLI_FOLDER, "game_picker.py"))
        print("✅ CLI script moved.")

# Step 5: Move JSON files to `data/`
def move_json_files():
    os.makedirs(DATA_FOLDER, exist_ok=True)
    json_files = ["leaders.json", "civilizations.json"]
    for json_file in json_files:
        src = os.path.join(PROJECT_ROOT, json_file)
        dest = os.path.join(DATA_FOLDER, json_file)
        if os.path.exists(src):
            print(f"🔹 Moving {json_file} to 'data/'...")
            shutil.move(src, dest)
            print(f"✅ {json_file} moved.")

# Step 6: Create Shared `game_logic.py`
def create_game_logic():
    os.makedirs(SCRIPTS_FOLDER, exist_ok=True)
    logic_file = os.path.join(SCRIPTS_FOLDER, "game_logic.py")
    if not os.path.exists(logic_file):
        print("🔹 Creating shared game logic in 'picker/scripts/game_logic.py'...")
        with open(logic_file, "w") as f:
            f.write("""import json
import random

# Load JSON data
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

PLAYSTYLES = ["Militaristic", "Economic", "Cultural", "Scientific", "Diplomatic", "Expansionist"]
REGIONS = {
    "Europe": ["France", "Italy", "Spain", "Prussia", "Russia", "Franks"],
    "Asia": ["Persia", "Han", "Maurya", "Vietnam", "Yamato", "Philippines"],
    "Africa": ["Aksum", "Egypt"],
    "Americas": ["America", "Shawnee", "Inca", "Gran Colombia"],
    "Global": []
}

leaders_data = load_json("data/leaders.json")["Leaders"]
civs_data = load_json("data/civilizations.json")["Civilizations"]

def get_leader_civ(region, playstyle):
    valid_civs = [civ for civ in civs_data if civ["Name"] in REGIONS.get(region, []) or region == "Global"]
    valid_leaders = [leader for leader in leaders_data if any(civ in leader["Historical Civ"] for civ in REGIONS.get(region, [])) or region == "Global"]

    filtered_leaders = [leader for leader in valid_leaders if playstyle in leader["Playstyle"]]
    filtered_civs = [civ for civ in valid_civs if playstyle in civ["Attributes"]]

    if not filtered_leaders or not filtered_civs:
        return None, None

    return random.choice(filtered_leaders), random.choice(filtered_civs)
""")
        print("✅ Shared game logic created.")

# Step 7: Update `.gitignore`
def update_gitignore():
    gitignore_path = os.path.join(PROJECT_ROOT, ".gitignore")
    if not os.path.exists(gitignore_path):
        print("🔹 Creating .gitignore file...")
        with open(gitignore_path, "w") as f:
            f.write("""env/
db.sqlite3
__pycache__/
*.pyc
*.log
data/*.json
""")
        print("✅ .gitignore created.")

# Step 8: Initialize Git
def initialize_git():
    if not os.path.exists(os.path.join(PROJECT_ROOT, ".git")):
        print("🔹 Initializing Git repository...")
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial Django and CLI setup"], check=True)
        print("✅ Git repository initialized.")

# Step 9: Final Django Configuration
def configure_django():
    print("🔹 Running Django migrations...")
    subprocess.run(["env\\Scripts\\python", "manage.py", "migrate"], check=True)
    print("✅ Migrations completed.")

# Run all setup steps
def main():
    setup_virtualenv()
    install_django()
    setup_django_project()
    move_cli_script()
    move_json_files()
    create_game_logic()
    update_gitignore()
    initialize_git()
    configure_django()
    print("🚀 Django and CLI setup complete!")

if __name__ == "__main__":
    main()
