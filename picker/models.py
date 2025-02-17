from django.db import models

class Civilization(models.Model):
    """Represents a Civilization in the game."""
    name = models.CharField(max_length=100, unique=True)
    attributes = models.JSONField(default=list)  # ✅ Ensures attributes is never NULL

    def __str__(self):
        return self.name


class Leader(models.Model):
    """Represents a Leader in the game."""
    name = models.CharField(max_length=100, unique=True)
    playstyle = models.JSONField()  # Stores list of playstyles (e.g., ['Diplomatic', 'Scientific'])
    historical_civ = models.ForeignKey(Civilization, on_delete=models.CASCADE, related_name="leaders")

    def __str__(self):
        return self.name
