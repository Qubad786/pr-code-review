from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from views.logout import LogoutView
from views.oauth import OAuthLogin, OAuthCallback

urlpatterns = [
    url(r'authorize/$', OAuthLogin.as_view(), name='authorize'),
    url(r'auth-callback/$', OAuthCallback.as_view(), name='auth_callback'),
    url(r'logout/$', login_required(LogoutView.as_view()), name='logout'),
]
