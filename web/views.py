from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect


def index_handler(request):
    if request.user.is_authenticated():
        response = redirect(reverse('dashboard'))
    else:
        response = render(request, 'web/index.html')

    return response


def dashboard_view(request):
    return render(request, 'web/dashboard.html')


def handler404(request):
    return render(request, 'web/404.html')


def handler500(request):
    return render(request, 'web/500.html')
