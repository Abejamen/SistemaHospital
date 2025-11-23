from django.db import models
from django.contrib.auth.models import User

class Position(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.position}"
