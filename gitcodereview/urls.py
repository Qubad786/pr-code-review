from django.conf.urls import include, url

urlpatterns = [
    url(r'', include('web.urls')),
]

handler404 = 'web.views.handler404'
handler500 = 'web.views.handler500'
