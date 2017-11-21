from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<query_string>.+)/(?P<page>[0-9]+)/query$', views.query, name='query')
]
