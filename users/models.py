from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    is_professor = models.BooleanField(default=False)
    is_site_admin = models.BooleanField(default=False)
    niveau = models.CharField(null=False,max_length=8,default="")
    confirmation_code  = models.CharField(max_length=6,default="")
    numero  = models.CharField(max_length=8,unique=True)
    paiement = models.CharField(max_length=8,default= "AWAIT")