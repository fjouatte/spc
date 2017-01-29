from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    user = models.ForeignKey(User,
                             related_name='actions',
                             db_index=True)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj')
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

class Edition(models.Model):

    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    numero = models.CharField(max_length=4)
    joueur_ids = models.ManyToManyField(
        User,
    )


class Map(models.Model):

    nom = models.CharField(max_length=128)
    edition_ids = models.ManyToManyField(
        Edition,
    )


class Rules(models.Model):

    content = HTMLField()
