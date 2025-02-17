import json
import os
import django

# Setup Django environment
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "civ7_picker.settings")
django.setup()

from picker.models import Civilization, Leader

def load_civilizations():
    """Load civilizations from JSON into the database."""
    with open("data/civilizations.json", "r", encoding="utf-8") as f:
        civs = json.load(f)["Civilizations"]

    for civ in civs:
        Civilization.objects.get_or_create(name=civ["Name"], attributes=civ.get("Attributes", []))  # ✅ Ensures attributes is never missing

    print("✅ Civilizations imported successfully.")

def load_leaders():
    """Load leaders from JSON into the database."""
    with open("data/leaders.json", "r", encoding="utf-8") as f:
        leaders = json.load(f)["Leaders"]

    for leader in leaders:
        civ, _ = Civilization.objects.get_or_create(name=leader["Historical Civ"], defaults={"attributes": []})  # ✅ Ensures civilization exists
        Leader.objects.get_or_create(name=leader["Name"], playstyle=leader["Playstyle"], historical_civ=civ)

    print("✅ Leaders imported successfully.")

if __name__ == "__main__":
    load_civilizations()
    load_leaders()
