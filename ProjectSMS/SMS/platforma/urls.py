from django.conf.urls import url
from django.contrib import admin
from .views import index,confirm,remember,OWnLogout,chooseVerion

urlpatterns = [
    url(r'^management/(?P<typeMethod>([a-z]+))/((?P<activeid>(\w)+)/)?$', index),
    url(r'^$', index),
    url(r'^confirm/$', confirm),
    url(r'^remind/$', remember),
    url(r'^logout/$', OWnLogout),
    url(r'^version/$', chooseVerion)
]
