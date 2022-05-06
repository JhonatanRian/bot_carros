# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cars(models.Model):
    name = models.CharField(max_length=300)
    price = models.CharField(max_length=15)
    km = models.CharField(max_length=100)
    year = models.CharField(max_length=15)
    source = models.CharField(max_length=1500)
    found_in = models.CharField(max_length=1500)
    provider_name = models.CharField(max_length=150)
    provider_url = models.CharField(max_length=1000)
    update = models.DateField(auto_now=True)
    photo = models.CharField(max_length=2500)
    
    def __str__(self) -> str:
        return self.name