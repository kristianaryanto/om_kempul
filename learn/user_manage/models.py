from django.db import models
from encrypted_field import EncryptedField
# Create your models here.

class user_database(models.Model):
    username = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    group = models.CharField(max_length = 200,blank=True, default='not_org_dwh')

class Foobar(models.Model):
    user = models.CharField(max_length=201)
    password = models.CharField(max_length=201)
