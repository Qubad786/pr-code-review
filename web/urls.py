from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

import views

urlpatterns = [
    url(r'^$', views.index_handler, name='index'),
    url(r'^dashboard/$', login_required(views.dashboard_view), name='dashboard'),
    url(r'^account/', include('web.user.urls')),
    url(r'^pull-request/', include('web.pullrequest.urls')),
]
