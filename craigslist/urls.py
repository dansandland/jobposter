from django.conf.urls import url

from . import views

app_name = 'craigslist'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^cl/verify_auth$', views.verify_auth, name='verify_auth'),
]
