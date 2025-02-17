import json
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
    """Returns a leader and civilization matching the given region and playstyle."""
    valid_civs = [civ for civ in civs_data if civ["Name"] in REGIONS.get(region, []) or region == "Global"]
    valid_leaders = [leader for leader in leaders_data if any(civ in leader["Historical Civ"] for civ in REGIONS.get(region, [])) or region == "Global"]

    filtered_leaders = [leader for leader in valid_leaders if playstyle in leader["Playstyle"]]
    filtered_civs = [civ for civ in valid_civs if playstyle in civ["Attributes"]]

    if not filtered_leaders or not filtered_civs:
        print(f"⚠️ No match for region: {region}, playstyle: {playstyle}")
        return {}, {}  # ✅ Return empty dictionaries instead of None

    return random.choice(filtered_leaders), random.choice(filtered_civs)


