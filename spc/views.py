# coding: utf-8

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView)
from spc.provider import ManiaplanetOAuth2Provider
from allauth.socialaccount import app_settings, providers
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.views.generic import DetailView
from spc.forms import LoginForm, SubscribeForm, UnsubscribeForm
from spc.models import Edition, EditionQualif, New, Rule
from spc.color_parser import ColorParser
import requests
import mysql.connector



def base(request):
    res = {'user_lang': 'fr'}
    providers_obj = providers.registry.get_list()
    if providers_obj:
        res.update(provider=providers_obj[0])
    if hasattr(request, 'session'):
        res.update(user_lang=request.session.get(LANGUAGE_SESSION_KEY, 'fr'))
    return res


def home(request):
    news = New.objects.filter(active=True).order_by('-create_date')
    paginator = Paginator(news, 5)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)
    return render(request, 'spc/home.html', {'news': news})


@login_required
def unsubscribe(request):
    """ Désincription d'un joueur à une édition
        Le joueur est supprimé de l'édition et de la table 'authorized_player' (MySQL xaseco)
        return False si une erreur se produit
    """
    base_return_url = '/edition/'
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            query = "delete from authorized_player where login = ('%s');" % (request.user.username)
            try:
                conn = mysql.connector.connect(host='localhost', user='root', database='Spam_Tech', password='cocorico')
            except Exception as ex:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute(query)
            except Exception as ex:
                return False
            finally:
                conn.close()
            cd = form.cleaned_data
            edition = Edition.objects.get(id=int(cd.get('edition_id')))
            edition.joueur_ids.remove(request.user.id)
            edition.save()
            return redirect(base_return_url+cd.get('edition_id'))


@login_required
def subscribe(request):
    """ Inscription d'un joueur à une édition
        Le joueur est ajouté à l'édition et à la table 'authorized_player' (MySQL xaseco)
        return False si une erreur se produit
    """
    base_return_url = '/edition/'
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            query = "insert into authorized_player (login) VALUES ('%s');" % (request.user.username)
            try:
                conn = mysql.connector.connect(host='localhost', user='root', database='Spam_Tech', password='cocorico')
            except Exception as ex:
                return False
            try:
                cursor = conn.cursor()
                cursor.execute(query)
            except Exception as ex:
                return False
            finally:
                conn.close()
            cd = form.cleaned_data
            edition = Edition.objects.get(id=int(cd.get('edition_id')))
            edition.joueur_ids.add(request.user.id)
            edition.save()
            return redirect(base_return_url+cd.get('edition_id'))



def rules(request):
    rule = Rule.objects.filter(active=True)
    if rule:
        rule = rule[0]
    return render(request, 'spc/rules.html', {'rule': rule})


def editions(request):
    old = Edition.objects.filter(date_end__lte=datetime.now())
    new = Edition.objects.filter(date_start__gte=datetime.now())
    current = Edition.objects.filter(date_start__lte=datetime.now()).filter(date_end__gte=datetime.now())
    values = dict(old=old, new=new, current=current, classement=False, erreur=False)
    # si une édition est en cours et que les qualifs sont en cours
    if current and current[0].editionqualif:
        qualif = current[0].editionqualif
        if qualif.date_start < datetime.now():
            classement = qualif.get_classement_qualif()
            if not classement:
                values.update(erreur=True)
            else:
                values.update(classement=classement)
        else:
            values.update(not_started=True)
    return render(
        request,
        'spc/editions.html',
        values
    )


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'spc/home.html', {})
                else:
                    return render(request, 'spc/login.html', {'form': form, 'error': u'Compte désactivé'})
            else:
                return render(request, 'spc/login.html', {'form': form, 'error': 'Utilisateur ou mot de passe erroné'})
    else:
        form = LoginForm()
    return render(request, 'spc/login.html', {'form': form})


def logged_out(request):
    return render(request, 'spc/logged_out.html', {})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(
                request, 'spc/register_done.html', {'new_user': new_user}
            )
        else:
            return render(
                request, 'spc/register.html', {'user_form': user_form, 'errors': user_form._errors}
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, 'spc/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'spc/edit.html', {'user_form': user_form})


class LireEdition(DetailView):

    context_object_name = "edition"
    model = Edition
    template_name = "spc/edition.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LireEdition, self).get_context_data(**kwargs)
        edition = context.get('edition')
        subscribed_users_ids = [j.id for j in edition.joueur_ids.all()]
        current_user_id = self.request.user.id
        context['subscribed'] = current_user_id in subscribed_users_ids
        context['user'] = self.request.user
        # si une édition est en cours et que les qualifs sont en cours
        qualif = edition.editionqualif
        if qualif.date_start < datetime.now():
            classement = qualif.get_classement_qualif()
            if not classement:
                context.update(erreur=True)
            else:
                paginator = Paginator(classement.ligneclassementqualif_set.all(), 20)
                page = self.request.GET.get('page')
                try:
                    ligneclassement = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    ligneclassement = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    ligneclassement = paginator.page(paginator.num_pages)
        else:
            context.update(not_started=True)
        context.update(ligneclassement=ligneclassement)
        return context


class ManiaplanetOAuth2Adapter(OAuth2Adapter):
    provider_id = ManiaplanetOAuth2Provider.id
    access_token_url = 'https://ws.maniaplanet.com/oauth2/token/'
    authorize_url = 'https://ws.maniaplanet.com/oauth2/authorize'
    profile_url = 'https://ws.maniaplanet.com/player/'

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(
            self.profile_url,
            headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        )
        return self.get_provider().sociallogin_from_response(request, resp.json())

oauth_login = OAuth2LoginView.adapter_view(ManiaplanetOAuth2Adapter)
oauth_callback = OAuth2CallbackView.adapter_view(ManiaplanetOAuth2Adapter)
