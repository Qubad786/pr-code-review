from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from web.pullrequest.views import PullRequestView

urlpatterns = [
    url(r'$', login_required(PullRequestView.as_view()), name='pull_request'),
]
