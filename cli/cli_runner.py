import sys
import os
import random

# Add the project root (civ7-game-setup) to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from picker.scripts.game_logic import get_leader_civ, PLAYSTYLES, REGIONS, leaders_data

def get_user_choice(prompt, options):
    """Handles user input and ensures a valid choice is selected."""
    options_display = " | ".join(options)
    while True:
        print(f"{prompt} ({options_display})")
        choice = input("Enter your choice: ").strip().title()
        if choice in options or choice == "Random":
            return choice
        print("❌ Invalid choice. Please try again.")

def select_setup():
    """Handles the initial setup selection for region and playstyle."""
    choice_order = get_user_choice(
        "🎭 How would you like to choose your setup?",
        ["Playstyle", "Region", "Random Everything"]
    )

    if choice_order == "Random Everything":
        region = random.choice(list(REGIONS.keys())[:-1])
        playstyle = random.choice(PLAYSTYLES)
    else:
        if choice_order == "Playstyle":
            playstyle = get_user_choice("🎭 Choose your playstyle:", PLAYSTYLES)
            region = get_user_choice("🌍 Choose your region:", list(REGIONS.keys())[:-1])
        else:
            region = get_user_choice("🌍 Choose your region:", list(REGIONS.keys())[:-1])
            playstyle = get_user_choice("🎭 Choose your playstyle:", PLAYSTYLES)

    return region, playstyle

def display_setup(region, playstyle, leader, civ):
    """Displays the current setup details."""
    print("\n🎮 **Your Civilization 7 Game Setup** 🎮")
    print(f"🔹 **Region**: {region}")
    print(f"🔹 **Playstyle**: {playstyle}")
    print(f"👑 **Leader**: {leader['Name']}")
    print(f"🏛 **Civilization**: {civ['Name']}\n")

def reroll_options(region, playstyle, leader, civ, matching_leaders):
    """Allows users to reroll parts of their setup."""
    while True:
        display_setup(region, playstyle, leader, civ)

        reroll_choices = ["Both", "Playstyle", "Region", "No"]
        if len(matching_leaders) > 1:
            reroll_choices.insert(1, "Leader Only")

        reroll_choice = get_user_choice("🔄 Do you want to reroll?", reroll_choices)

        if reroll_choice == "Both":
            print("\n🎲 Rerolling everything...\n")
            region, playstyle = select_setup()
            leader, civ = get_leader_civ(region, playstyle)

            # Ensure we return four values
            return region, playstyle, leader, civ  

        elif reroll_choice == "Playstyle":
            playstyle = random.choice(PLAYSTYLES)
            print(f"🎲 New Playstyle: {playstyle}")

        elif reroll_choice == "Region":
            region = random.choice(list(REGIONS.keys())[:-1])
            print(f"🎲 New Region: {region}")

        elif reroll_choice == "Leader Only":
            leader = random.choice(matching_leaders)
            print(f"\n👑 Rerolling leader...\n🎲 New Leader: {leader['Name']}")

        else:
            print("\n✅ Setup finalized! Enjoy your game!")
            return region, playstyle, leader, civ  # ✅ Ensure it returns four values

        leader, civ = get_leader_civ(region, playstyle)

        if not leader or not civ:
            print(f"❌ No valid leader or civilization found after reroll for Region: {region}, Playstyle: {playstyle}")
            return region, playstyle, None, None  # ✅ Ensuring we always return 4 values

        matching_leaders = [
            l for l in leaders_data if l["Historical Civ"] == civ["Name"] and playstyle in l["Playstyle"]
        ]

def main():
    """Main function to run the Civilization 7 CLI picker."""
    print("\n🎮 Civilization 7 Game Picker CLI 🎮")

    region, playstyle = select_setup()
    leader, civ = get_leader_civ(region, playstyle)

    # Debugging prints
    print(f"DEBUG: Leader returned: {leader}")
    print(f"DEBUG: Civ returned: {civ}")

    if not leader or not civ:
        print(f"❌ No valid leader or civilization found for region: {region}, playstyle: {playstyle}")
        return

    matching_leaders = [
        l for l in leaders_data if l["Historical Civ"] == civ["Name"] and playstyle in l["Playstyle"]
    ]

    region, playstyle, leader, civ = reroll_options(region, playstyle, leader, civ, matching_leaders)

if __name__ == "__main__":
    main()
