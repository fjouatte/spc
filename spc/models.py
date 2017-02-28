# coding: utf-8

from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
import mysql.connector
from django.core.exceptions import ObjectDoesNotExist


def get_now():
    return datetime.now()


class User(AbstractUser):
    nickname = models.TextField(max_length=500)


class Classement(models.Model):
    last_updated_date = models.DateTimeField(null=True)


class LigneClassement(models.Model):
    # TODO: remove null option
    player_id = models.ForeignKey(User, null=True)
    position = models.IntegerField()

class New(models.Model):

    author_id = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=128, unique=True)
    content = HTMLField()
    content_en = HTMLField()
    active = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=get_now, editable=False)


class Edition(models.Model):

    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    numero = models.CharField(max_length=4, unique=True)
    joueur_ids = models.ManyToManyField(settings.AUTH_USER_MODEL)
    subscribe_date_start = models.DateTimeField()
    subscribe_date_end = models.DateTimeField()


class EditionQualif(models.Model):

    edition_id = models.OneToOneField(Edition, unique=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    def save(self, *args, **kwargs):
        is_new = True if not self.id else False
        super(EditionQualif, self).save(*args, **kwargs)
        if is_new:
            cq = ClassementQualif(qualif_id=self)
            cq.save()

    def get_classement_qualif(self):
        """
        récupère les données depuis la base de données distante ou depuis la base de données locale
        (pour ne pas trop faire d'appels)
        retourne une liste de dictionnaires ayant pour clés : position, login, pseudo et user_id
        """
        try:
            classement = self.classementqualif
        except ObjectDoesNotExist:
            return False
        last_updated_date = classement.last_updated_date
        cpt = 1
        # si la dernière mise à jour date de moins de 5 minutes alors on affiche le classement stocké
        if last_updated_date and last_updated_date > datetime.now()-timedelta(seconds=300):
            return self.classementqualif
        try:
            conn = mysql.connector.connect(host='localhost', user='root', database='Spam_Tech', password='cocorico')
        except Exception as ex:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute(
                "select players.login, players.nickname, rs_rank.playerid from players inner join rs_rank on (players.id = rs_rank.playerid);"
            )
            rows = cursor.fetchall()
            for row in rows:
                try:
                    user = User.objects.get(username=row[0])
                except User.DoesNotExist:
                    user = None
                ligne = LigneClassementQualif(player_id=user, position=cpt, classement_qualif_id=classement)
                ligne.save()
                cpt += 1
        except Exception as exc:
            return False
        finally:
            conn.close()
        classement.last_updated_date = datetime.now()
        classement.save()
        self.classementqualif = classement
        self.save()
        return classement


class EditionDemi(models.Model):

    edition_id = models.ForeignKey(Edition, related_name='demi_ids')
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    joueur_ids = models.ManyToManyField(settings.AUTH_USER_MODEL)


class EditionFinale(models.Model):

    edition_id = models.ForeignKey(Edition)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    joueur_ids = models.ManyToManyField(settings.AUTH_USER_MODEL)


class ClassementQualif(Classement):
    qualif_id = models.OneToOneField(EditionQualif, on_delete=models.CASCADE, primary_key=True)


class ClassementDemi(Classement):
    demi_id = models.ForeignKey(EditionDemi, on_delete=models.CASCADE, primary_key=True)


class ClassementFinale(Classement):
    finale_id = models.OneToOneField(EditionFinale, on_delete=models.CASCADE, primary_key=True)


class LigneClassementQualif(LigneClassement):
    classement_qualif_id = models.ForeignKey(ClassementQualif)


class LigneClassementDemi(LigneClassement):
    classement_demi_id = models.ForeignKey(ClassementDemi)


class LigneClassementFinale(LigneClassement):
    classement_finale_id = models.ForeignKey(ClassementFinale)


class Map(models.Model):


    nom = models.CharField(max_length=128, unique=True)
    edition_ids = models.ManyToManyField(
        Edition,
    )


class Rule(models.Model):

    content = HTMLField()
    content_en = HTMLField()
    active = models.BooleanField(default=False)



@admin.register(New)
class NewAdmin(admin.ModelAdmin):

    date_hierarchy = 'create_date'
    list_display = ('title', 'author_id', 'create_date', 'active')
    fields = ('title', 'content', 'content_en', 'active')

    def save_model(self, request, obj, form, change):
        obj.author_id = request.user
        super(NewAdmin, self).save_model(request, obj, form, change)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(UserAdmin, self).save_model(request, obj, form, change)


class EditionQualifInline(admin.StackedInline):
    model = EditionQualif


@admin.register(Edition)
class EditionAdmin(admin.ModelAdmin):

    fields = ('numero', 'date_start', 'date_end', 'subscribe_date_start', 'subscribe_date_end')
    list_display = ('numero', 'date_start', 'date_end')
    inlines = [
        EditionQualifInline,
    ]
