from __future__ import unicode_literals
from django.conf import settings
from django.db import models


class Joueur(models.Model):
    trackmania_id = models.CharField(max_length=128)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
    )


class Edition(models.Model):

    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    numero = models.CharField(max_length=4)
    joueur_ids = models.ManyToManyField(
        Joueur,
    )


class Map(models.Model):

    nom = models.CharField(max_length=128)
    edition_ids = models.ManyToManyField(
        Edition,
    )
