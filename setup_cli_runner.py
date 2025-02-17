import os
import shutil

# Define project paths
PROJECT_ROOT = os.path.abspath(os.getcwd())  # Ensure it's running from civ7-game-setup root
CLI_FOLDER = os.path.join(PROJECT_ROOT, "cli")
SCRIPTS_FOLDER = os.path.join(PROJECT_ROOT, "picker", "scripts")

# Paths for CLI scripts
OLD_CLI_SCRIPT = os.path.join(CLI_FOLDER, "game_picker.py")
NEW_CLI_SCRIPT = os.path.join(CLI_FOLDER, "cli_runner.py")
GAME_LOGIC_SCRIPT = os.path.join(SCRIPTS_FOLDER, "game_logic.py")

# Step 1: Move CLI logic to `picker/scripts/game_logic.py`
def create_game_logic():
    os.makedirs(SCRIPTS_FOLDER, exist_ok=True)
    if not os.path.exists(GAME_LOGIC_SCRIPT):
        print("🔹 Creating shared game logic in 'picker/scripts/game_logic.py'...")
        with open(GAME_LOGIC_SCRIPT, "w", encoding="utf-8") as f:
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

# Step 2: Rename `game_picker.py` to `cli_runner.py`
def move_cli_script():
    os.makedirs(CLI_FOLDER, exist_ok=True)
    if os.path.exists(OLD_CLI_SCRIPT):
        print("🔹 Renaming 'game_picker.py' to 'cli_runner.py'...")
        shutil.move(OLD_CLI_SCRIPT, NEW_CLI_SCRIPT)
        print("✅ CLI script renamed.")

# Step 3: Update `cli_runner.py` to Use Shared Logic (Fixed Encoding Issue)
def update_cli_runner():
    print("🔹 Updating 'cli_runner.py' to use shared game logic...")
    with open(NEW_CLI_SCRIPT, "w", encoding="utf-8") as f:
        f.write("""from picker.scripts.game_logic import get_leader_civ, PLAYSTYLES, REGIONS

def main():
    print("\\n🎮 Civilization 7 Game Picker CLI 🎮")

    region = input(f"Choose a region {list(REGIONS.keys())}: ").strip()
    playstyle = input(f"Choose a playstyle {PLAYSTYLES}: ").strip()

    leader, civ = get_leader_civ(region, playstyle)

    if leader and civ:
        print("\\n🎮 **Your Civilization 7 Game Setup** 🎮")
        print(f"🔹 **Region**: {region}")
        print(f"🔹 **Playstyle**: {playstyle}")
        print(f"👑 **Leader**: {leader['Name']}")
        print(f"🏛 **Civilization**: {civ['Name']}")
    else:
        print("❌ No matching leader or civilization found!")

if __name__ == "__main__":
    main()
""")
    print("✅ 'cli_runner.py' updated to use shared logic.")

# Step 4: Verify CLI Runs Correctly
def test_cli():
    print("\n🚀 Testing CLI...")
    os.system(f"python {NEW_CLI_SCRIPT}")

# Run all setup steps
def main():
    create_game_logic()
    move_cli_script()
    update_cli_runner()
    test_cli()
    print("\n🎉 CLI setup complete! Run `python cli/cli_runner.py` to use the CLI.")

if __name__ == "__main__":
    main()
