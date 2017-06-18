from django.conf.urls import url

from . import views
from django.contrib.auth.decorators import login_required
from bank.settings import LOGIN_URL
urlpatterns = [
    url(r'^$', views.check, name='check'),
    
]
