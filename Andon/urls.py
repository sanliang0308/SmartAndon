from django.conf.urls import url
from django.contrib import admin

admin.autodiscover()

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^InvaildAccess', views.InvaildAccess, name='InvaildAccess'),
    url(r'^$', views.index, name='index'),
    url(r'^subIndex', views.subIndex, name='subIndex'),
    url(r'^notify', views.notify, name='notify'),
    url(r'^acknowledgement', views.acknowledgement, name='acknowledgement'),
    url(r'^sendNotification', views.sendNotification, name='sendNotification'),
    url(r'^Dashboard/', views.Dashboard, name='Dashboard'),
    url(r'^viewConcern/', views.viewConcern, name='viewConcern'),
    url(r'^viewSupportPersonnel/', views.viewSupportPersonnel, name='viewSupportPersonnel'),
    url(r'^viewIssue/', views.viewIssue, name='viewIssue'),
    url(r'^viewAcknowledgement/', views.viewAcknowledgement, name='viewAcknowledgement'),
    url(r'^testnotify', views.testnotify, name='testnotify'),
]