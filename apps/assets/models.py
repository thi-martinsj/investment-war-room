from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Assets(models.Model):
    created_dt = models.DateTimeField(default=datetime.now)
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.ticker


class AssetsConfig(models.Model):
    created_dt = models.DateTimeField(default=datetime.now)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    asset_id = models.ForeignKey(Assets, on_delete=models.CASCADE)
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    frequency = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.asset_id} config for user {self.user_id}"


class AssetsValues(models.Model):
    created_dt = models.DateTimeField(default=datetime.now)
    asset_id = models.ForeignKey(Assets, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.asset_id}: R$ {(self.value/100):.2f}"