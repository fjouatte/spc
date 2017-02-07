from __future__ import unicode_literals
from datetime import datetime
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
import mysql.connector


def get_now():
    return datetime.now()


class New(models.Model):

    author_id = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=128, unique=True)
    content = HTMLField()
    content_en = HTMLField()
    active = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=get_now, editable=False)


class User(AbstractUser):
    login_trackmania = models.CharField(max_length=64, unique=True)


class Edition(models.Model):

    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    numero = models.CharField(max_length=4, unique=True)
    joueur_ids = models.ManyToManyField(settings.AUTH_USER_MODEL)
    subscribe_date_start = models.DateTimeField()
    subscribe_date_end = models.DateTimeField()


class EditionQualif(models.Model):

    edition_id = models.OneToOneField(Edition, primary_key=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    classement = ArrayField(ArrayField(models.IntegerField()))

    def get_classement(self):
        conn = mysql.connector.connect(host='localhost', user='root', database='Spam_Tech')
        try:
            cursor = conn.cursor()
            cursor.execute("select * from rs_rank")
            rows = cursor.fetchall()
        finally:
            conn.close()



class EditionDemi(models.Model):

    edition_id = models.ForeignKey(Edition, related_name='demi_ids')
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    joueur_ids = models.ManyToManyField(settings.AUTH_USER_MODEL)


class EditionFinale(models.Model):

    edition_id = models.OneToOneField(Edition, primary_key=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    joueur_ids = models.ManyToManyField(settings.AUTH_USER_MODEL)


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
