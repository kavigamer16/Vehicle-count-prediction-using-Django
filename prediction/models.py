from django.db import models
from django.contrib.auth.models import User

class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    predicted_count = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)