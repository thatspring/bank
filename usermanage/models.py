from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings
class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=20)

    def __unicode__(self):
        return self.user.username
