from django.http import JsonResponse
from picker.scripts.game_logic import get_leader_civ

def get_random_setup(request):
    """API endpoint to return a random Civilization 7 setup."""
    region = request.GET.get("region", "Americas")
    playstyle = request.GET.get("playstyle", "Diplomatic")

    leader, civ = get_leader_civ(region, playstyle)

    if not leader or not civ:
        return JsonResponse({"error": "No matching leader or civilization found"}, status=400)

    return JsonResponse({
        "region": region,
        "playstyle": playstyle,
        "leader": leader["Name"],
        "civilization": civ["Name"]
    })
