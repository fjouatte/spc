from django.shortcuts import render


def home(request):
    return render(request, 'spc/home.html', locals())
