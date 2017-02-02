from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from tinymce.models import HTMLField


class User(AbstractUser):
    login_trackmania = models.CharField(max_length=64)


class Edition(models.Model):

    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    numero = models.CharField(max_length=4)
    joueur_ids = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
    )


class Map(models.Model):

    nom = models.CharField(max_length=128)
    edition_ids = models.ManyToManyField(
        Edition,
    )


class Rule(models.Model):

    content = HTMLField()
    active = models.BooleanField(default=False)
