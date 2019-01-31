from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Roll(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    year_made = models.IntegerField(default=1923)
