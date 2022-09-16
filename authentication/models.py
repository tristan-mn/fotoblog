
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICES = (
        (CREATOR, 'créateur'),
        (SUBSCRIBER, 'abonné'),
    )

    profile_photo = models.ImageField(verbose_name='photo de profile')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
    follows = models.ManyToManyField(
        'self',
        limit_choices_to={'role': CREATOR},
        symmetrical=False,
        verbose_name='suit',
    )
