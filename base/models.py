from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

ROLES_CHOICES = (
    ('cashier', 'Cashier'),
    ('manager', 'Manager'),
)

class User(AbstractUser):
  role = models.CharField(max_length=50, default='cashier', choices=ROLES_CHOICES)
  pass