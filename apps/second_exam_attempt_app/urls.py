from django.conf.urls import url
from . import views
#from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^jobs/remove/(?P<job_id>\d+)$', views.remove),
    url(r'^jobs/new$', views.new),
    url(r'^jobs/create$', views.create),
    url(r'^jobs/(?P<job_id>\d+)$', views.view),
    url(r'^jobs/edit/(?P<job_id>\d+)$', views.edit_page),
    url(r'^jobs/edit/process/(?P<job_id>\d+)$', views.edit_process),
]