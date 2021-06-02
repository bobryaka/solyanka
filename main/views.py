from django.shortcuts import render, redirect
from cont import *
from tokens import keys


def index(request):
    return render(request, 'main/index.html')


def handshake(request):
    if request.method == 'POST':
        context = list()
        context.append(request.POST.get('firstman'))
        context.append(request.POST.get('secondman'))

        return render(request, 'main/handshake.html', {'context': context})
    return render(request, 'main/handshake.html')


def contacts(request):
    return render(request, 'main/contacts.html')


