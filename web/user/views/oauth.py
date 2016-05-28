import requests
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from gitcodereview.settings import OAUTH_SETTINGS


class OAuthLogin(View):

    # noinspection PyMethodMayBeStatic
    def get(self, request):

        authorization_url = "{github_auth_uri}?client_id={client_id}&redirect_uri={redirect_uri}".format(
            github_auth_uri=OAUTH_SETTINGS.get('BASE_URL'),
            client_id=OAUTH_SETTINGS.get('CLIENT_ID'),
            redirect_uri=OAUTH_SETTINGS.get('REDIRECT_URL')
        )

        return redirect(authorization_url)


class OAuthCallback(View):

    # noinspection PyMethodMayBeStatic
    def get(self, request):

        code = request.GET.get('code', False)

        if not code:
            # Handle error gracefully!
            error_message = request.GET.get('error_description')
            return render(request, 'web/index.html', dict(error=error_message))

        payload = dict(
            client_id=OAUTH_SETTINGS.get('CLIENT_ID'),
            redirect_uri=OAUTH_SETTINGS.get('REDIRECT_URL'),
            client_secret=OAUTH_SETTINGS.get('CLIENT_SECRET'),
            code=code,
        )
        github_response = requests.post(
            OAUTH_SETTINGS.get('ACCESS_TOKEN_URL'),
            data=payload,
            headers=dict(Accept='application/json'),
        )

        if github_response.status_code != 200:
            error_message = request.GET.get('error_description')
            return render(request, 'web/index.html', dict(error=error_message))

        access_token = github_response.json().get('access_token')
        user = authenticate(access_token=access_token)
        login(request, user=user)

        return redirect(reverse('dashboard'))
