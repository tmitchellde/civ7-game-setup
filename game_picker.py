import json
import random

# Load JSON files
with open("leaders.json", "r") as f:
    leaders_data = json.load(f)

with open("civilizations.json", "r") as f:
    civs_data = json.load(f)

# Define playstyles and regions
playstyles = ["Militaristic", "Economic", "Cultural", "Scientific", "Diplomatic", "Expansionist"]
regions = {
    "Europe": ["France", "Italy", "Spain", "Prussia", "Russia", "Franks"],
    "Asia": ["Persia", "Han", "Maurya", "Vietnam", "Yamato"],
    "Africa": ["Aksum", "Egypt"],
    "Americas": ["Inca", "Shawnee", "America", "Philippines"],
    "Global": []  # Used for Random
}

def get_leader_civ(region, game_type):
    """Select a leader & civilization based on region & playstyle"""
    
    # Get list of civilizations from selected region
    valid_civs = [civ for civ in civs_data["Civilizations"] if civ["Name"] in regions[region] or region == "Global"]
    valid_leaders = [leader for leader in leaders_data["Leaders"] if any(civ in leader["Historical Civ"] for civ in regions[region]) or region == "Global"]

    # Filter by playstyle
    filtered_leaders = [leader for leader in valid_leaders if game_type in leader["Playstyle"]]
    filtered_civs = [civ for civ in valid_civs if game_type in civ["Attributes"]]

    if not filtered_leaders or not filtered_civs:
        return None, None  # No matches found

    chosen_leader = random.choice(filtered_leaders)
    chosen_civ = random.choice(filtered_civs)

    return chosen_leader, chosen_civ

# Game loop to allow rerolling
while True:
    print("\n🎭 Do you want to pick by playstyle or region first?")
    print("Options: Playstyle, Region")
    choice_order = input("Enter your choice: ").strip().capitalize()

    if choice_order not in ["Playstyle", "Region"]:
        print("❌ Invalid choice. Please enter 'Playstyle' or 'Region'.")
        continue

    # If user chooses to pick by playstyle first
    if choice_order == "Playstyle":
        print("\n🎭 What type of game do you want to play?")
        print("Options: Militaristic, Economic, Cultural, Scientific, Diplomatic, Expansionist, or Random")
        game_type = input("Enter your choice: ").strip().capitalize()

        if game_type == "Random":
            game_type = random.choice(playstyles)
            print(f"🎲 Randomly chosen playstyle: {game_type}")

        print("\n🌍 What region do you want to play from?")
        print("Options: Europe, Asia, Africa, Americas, or Random")
        region_choice = input("Enter your choice: ").strip().capitalize()

        if region_choice == "Random":
            region_choice = random.choice(list(regions.keys())[:-1])  # Excludes "Global"
            print(f"🎲 Randomly chosen region: {region_choice}")

    # If user chooses to pick by region first
    else:
        print("\n🌍 What region do you want to play from?")
        print("Options: Europe, Asia, Africa, Americas, or Random")
        region_choice = input("Enter your choice: ").strip().capitalize()

        if region_choice == "Random":
            region_choice = random.choice(list(regions.keys())[:-1])  # Excludes "Global"
            print(f"🎲 Randomly chosen region: {region_choice}")

        print("\n🎭 What type of game do you want to play?")
        print("Options: Militaristic, Economic, Cultural, Scientific, Diplomatic, Expansionist, or Random")
        game_type = input("Enter your choice: ").strip().capitalize()

        if game_type == "Random":
            game_type = random.choice(playstyles)
            print(f"🎲 Randomly chosen playstyle: {game_type}")

    # Get a leader & civilization based on region & playstyle
    leader, civ = get_leader_civ(region_choice, game_type)

    if leader and civ:
        print("\n🎮 **Your Civilization 7 Game Setup** 🎮")
        print(f"🔹 **Region**: {region_choice}")
        print(f"🔹 **Playstyle**: {game_type}")
        print(f"👑 **Leader**: {leader['Name']}")
        print(f"🏛 **Civilization**: {civ['Name']}")
        
        # Show leader abilities if available
        if "Ability" in leader:
            print(f"🏆 **Leader Ability**: {leader['Ability']}")

        # Show civilization bonuses if available
        if "Bonuses" in civ:
            print(f"🎖️ **Civilization Bonuses**: {', '.join(civ['Bonuses'])}")

        # Show unique units if available
        if "Unique Units" in civ:
            print(f"⚔️ **Unique Units**: {', '.join(civ['Unique Units'])}")

        # Ask if user wants to reroll
        reroll = input("\n🔄 Do you want to reroll? (yes/no): ").strip().lower()
        if reroll != "yes":
            break
    else:
        print("⚠️ No matching leaders or civilizations found. Try again.")
