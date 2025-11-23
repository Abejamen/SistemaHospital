from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('SUPERVISOR', 'Supervisor'),
        ('MATRONA', 'Matrona'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='MATRONA')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = "ADMIN"

        super().save(*args, **kwargs)

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email
