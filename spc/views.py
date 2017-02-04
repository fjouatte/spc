# coding: utf-8

from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from spc.forms import LoginForm, UserRegistrationForm, UserEditForm, SubscribeForm, UnsubscribeForm
from spc.models import Edition, New, Rule
from django.utils.translation import LANGUAGE_SESSION_KEY


def base(request):
    if hasattr(request, 'session'):
        return {'user_lang': request.session.get(LANGUAGE_SESSION_KEY, 'fr')}
    return {'user_lang': 'fr'}


def home(request):
    news = New.objects.filter(active=True)
    return render(request, 'spc/home.html', {'news': news})


@login_required
def unsubscribe(request):
    base_return_url = '/edition/'
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            edition = Edition.objects.get(id=int(cd.get('edition_id')))
            edition.joueur_ids.remove(request.user.id)
            edition.save()
            return redirect(base_return_url+cd.get('edition_id'))


@login_required
def subscribe(request):
    base_return_url = '/edition/'
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
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
    old = Edition.objects.filter(date_fin__lte=datetime.now())
    new = Edition.objects.filter(date_debut__gte=datetime.now())
    current = Edition.objects.filter(date_debut__lte=datetime.now()).filter(date_fin__gte=datetime.now())
    return render(
        request,
        'spc/editions.html',
        {
            'old': old,
            'new': new,
            'current': current,
        }
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
        return context
