from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Position, Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        position = Position.objects.filter(code="MATRONA").first()
        Profile.objects.create(user=instance, position=position)


def ensure_positions():
    roles = [
        ("ADMIN", "Administrador"),
        ("SUPERVISOR", "Supervisor"),
        ("MATRONA", "Matrona")
    ]

    for code, name in roles:
        Position.objects.get_or_create(code=code, name=name)
