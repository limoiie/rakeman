from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {"items": range(1, 100)}
    return HttpResponse(render(request, 'rake/index.html', context))
