from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from spc.forms import LoginForm, UserRegistrationForm, UserEditForm
from spc.models import Edition, Rule


def home(request):
    return render(request, 'spc/home.html', locals())


def rules(request):
    rule = Rule.objects.filter(active=True)
    return render(request, 'spc/rules.html', {'rule': rule[0]})


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
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
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
            return render(request,
                          'spc/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'spc/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
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
