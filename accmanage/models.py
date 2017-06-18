from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TemporaryRecord(models.Model):
    transferID=models.CharField(max_length=24,unique=True)
    user = models.CharField(max_length=20,unique=True)
    money = models.DecimalField(decimal_places=2, max_digits=20)
    comment = models.TextField(null=True)
    target = models.CharField(default="",max_length=16)
    process = models.BooleanField()
    def __unicode__(self):
        return self.user.username
