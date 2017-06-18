from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^transferProcess', views.transferProcess, name='transferProcess'),
    url(r'^success/', views.paysuccess, name='paysuccess'),
    url(r'^fail/', views.insufficientBalance, name='insufficientBalance'),
]
