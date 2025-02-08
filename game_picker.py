import json
import random

# Load JSON files
with open("leaders.json", "r") as f:
    leaders_data = json.load(f)

with open("civilizations.json", "r") as f:
    civs_data = json.load(f)

# Available playstyles
playstyles = ["Militaristic", "Economic", "Cultural", "Scientific", "Diplomatic", "Expansionist"]

# Ask user for game type
print("What type of game do you want to play?")
print("Options: Militaristic, Economic, Cultural, Scientific, Diplomatic, Expansionist, or Random")
game_type = input("Enter your choice: ").strip().capitalize()

# If "Random" is chosen, pick a random playstyle
if game_type == "Random":
    game_type = random.choice(playstyles)
    print(f"Randomly chosen playstyle: {game_type}")

# Match leaders and civilizations based on the chosen playstyle
matching_leaders = [leader for leader in leaders_data["Leaders"] if game_type in leader["Playstyle"]]
matching_civs = [civ for civ in civs_data["Civilizations"] if game_type in civ["Attributes"]]

# Select a random leader and civilization
if matching_leaders and matching_civs:
    chosen_leader = random.choice(matching_leaders)
    chosen_civ = random.choice(matching_civs)

    # Display results
    print("\n🎮 Your Civilization 7 Game Setup 🎮")
    print(f"🔹 Playstyle: {game_type}")
    print(f"👑 Leader: {chosen_leader['Name']}")
    print(f"🏛 Civilization: {chosen_civ['Name']}")
else:
    print("No matching leaders or civilizations found for this playstyle.")
