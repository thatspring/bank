from __future__ import unicode_literals
from django.db import models
# Create your models here.
class BusinessRecord(models.Model):
    transferID=models.CharField(max_length=24,unique=True)
    user = models.CharField(max_length=16)
    money = models.DecimalField(decimal_places=2, max_digits=20)
    operation = models.BooleanField()
    date = models.DateTimeField()
    comment = models.TextField(null=True)
    target = models.CharField(max_length=16)
    def __unicode__(self):
        return self.user.username
