from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.transferAccount, name='transferAccount'),
    url(r'^checkTransfer', views.checkTransfer, name='checkTransfer'),
    url(r'^pay', views.pay,name='pay'),
]
