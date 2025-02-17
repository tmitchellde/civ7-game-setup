import json
import random

class GameSetup:
    """Handles game setup, leader/civilization selection, and rerolling"""
    
    PLAYSTYLES = ["Militaristic", "Economic", "Cultural", "Scientific", "Diplomatic", "Expansionist"]
    REGIONS = {
        "Europe": ["France", "Italy", "Spain", "Prussia", "Russia", "Franks"],
        "Asia": ["Persia", "Han", "Maurya", "Vietnam", "Yamato", "Philippines"],
        "Africa": ["Aksum", "Egypt"],
        "Americas": ["America", "Shawnee", "Inca", "Gran Colombia"],
        "Global": []  # Used for Random
    }

    def __init__(self):
        """Loads data from JSON and initializes variables"""
        with open("leaders.json", "r", encoding="utf-8") as f:
            self.leaders_data = json.load(f)

        with open("civilizations.json", "r", encoding="utf-8") as f:
            self.civs_data = json.load(f)

        self.region = None
        self.playstyle = None
        self.leader = None
        self.civilization = None
        self.matching_leaders = []

    def get_random_choice(self, options, exclude=None):
        """Randomly selects an option from a list, excluding a given value"""
        return random.choice([opt for opt in options if opt != exclude])

    def select_leader_civ(self):
        """Selects a leader and civilization based on the chosen region and playstyle"""
        valid_civs = [civ for civ in self.civs_data["Civilizations"] if civ["Name"] in self.REGIONS[self.region] or self.region == "Global"]
        valid_leaders = [leader for leader in self.leaders_data["Leaders"] if any(civ in leader["Historical Civ"] for civ in self.REGIONS[self.region]) or self.region == "Global"]

        self.matching_leaders = [leader for leader in valid_leaders if self.playstyle in leader["Playstyle"]]
        matching_civs = [civ for civ in valid_civs if self.playstyle in civ["Attributes"]]

        if not self.matching_leaders or not matching_civs:
            return None, None

        self.leader = random.choice(self.matching_leaders)
        self.civilization = random.choice(matching_civs)

    def display_setup(self):
        """Displays the selected game setup"""
        print("\n🎮 **Your Civilization 7 Game Setup** 🎮")
        print(f"🔹 **Region**: {self.region}")
        print(f"🔹 **Playstyle**: {self.playstyle}")
        print(f"👑 **Leader**: {self.leader['Name']}")
        print(f"🏛 **Civilization**: {self.civilization['Name']}")

        if "Ability" in self.leader:
            print(f"🏆 **Leader Ability**: {self.leader['Ability']}")
        if "Bonuses" in self.civilization:
            print(f"🎖️ **Civilization Bonuses**: {', '.join(self.civilization['Bonuses'])}")
        if "Unique Units" in self.civilization:
            print(f"⚔️ **Unique Units**: {', '.join(self.civilization['Unique Units'])}")

    def get_user_choice(self, prompt, options):
        """Handles user input for choosing an option, displaying options before input"""
        options_display = " | ".join(options)
        while True:
            print(f"{prompt} ({options_display})")
            choice = input("Enter your choice: ").strip().lower()
            options_lower = [opt.lower() for opt in options]
            if choice in options_lower:
                return options[options_lower.index(choice)]  # Return correctly capitalized version
            print("❌ Invalid choice. Please try again.")

    def select_initial_setup(self):
        """Handles initial selection of region and playstyle"""
        choice_order = self.get_user_choice(
            "🎭 How would you like to choose your setup?",
            ["Playstyle", "Region", "Random Everything"]
        )

        if choice_order == "Random Everything":
            self.region = self.get_random_choice(list(self.REGIONS.keys())[:-1])
            self.playstyle = self.get_random_choice(self.PLAYSTYLES)
        else:
            if choice_order == "Playstyle":
                self.playstyle = self.get_user_choice("🎭 Choose your playstyle:", self.PLAYSTYLES + ["Random"])
                if self.playstyle == "Random":
                    self.playstyle = self.get_random_choice(self.PLAYSTYLES)

                self.region = self.get_user_choice("🌍 Choose your region:", list(self.REGIONS.keys())[:-1] + ["Random"])
                if self.region == "Random":
                    self.region = self.get_random_choice(list(self.REGIONS.keys())[:-1])
            else:
                self.region = self.get_user_choice("🌍 Choose your region:", list(self.REGIONS.keys())[:-1] + ["Random"])
                if self.region == "Random":
                    self.region = self.get_random_choice(list(self.REGIONS.keys())[:-1])

                self.playstyle = self.get_user_choice("🎭 Choose your playstyle:", self.PLAYSTYLES + ["Random"])
                if self.playstyle == "Random":
                    self.playstyle = self.get_random_choice(self.PLAYSTYLES)

        self.select_leader_civ()

    def reroll_options(self):
        """Handles rerolling logic"""
        while True:
            self.display_setup()

            reroll_choices = ["Both", "Playstyle", "Region", "No"]
            if len(self.matching_leaders) > 1:
                reroll_choices.insert(1, "Leader Only")

            reroll_choice = self.get_user_choice("🔄 Do you want to reroll?", reroll_choices)

            if reroll_choice == "Both":
                print("\n🎲 Rerolling everything...\n")
                self.select_initial_setup()
            elif reroll_choice == "Playstyle":
                self.playstyle = self.get_random_choice(self.PLAYSTYLES)
                print(f"🎲 New Playstyle: {self.playstyle}")
            elif reroll_choice == "Region":
                self.region = self.get_random_choice(list(self.REGIONS.keys())[:-1])
                print(f"🎲 New Region: {self.region}")
            elif reroll_choice == "Leader Only":
                self.leader = self.get_random_choice(self.matching_leaders, exclude=self.leader)
                print(f"\n👑 Rerolling leader...\n🎲 New Leader: {self.leader['Name']}")
            elif reroll_choice == "No":
                print("\n✅ Setup finalized! Enjoy your game!")
                exit()  # 🚀 Fix: Properly ends the script when "No" is selected!

            self.select_leader_civ()

class GameManager:
    """Manages the game loop"""
    @staticmethod
    def start_game():
        game = GameSetup()
        game.select_initial_setup()
        game.reroll_options()

if __name__ == "__main__":
    GameManager.start_game()
