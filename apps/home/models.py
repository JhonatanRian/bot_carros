# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from pydoc import visiblename
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cars(models.Model):
    name = models.CharField("nome do carro", max_length=300)
    price = models.CharField("preço", max_length=15)
    km = models.CharField("kilometragem", max_length=100)
    year = models.CharField("ano", max_length=15)
    source = models.CharField("link do anuncio", max_length=1500)
    found_in = models.CharField("url onde foi encontrado", max_length=1500)
    provider_name = models.CharField("Empresa anunciante", max_length=150)
    update = models.DateField("atualizado em", auto_now=True)
    photo = models.CharField("foto", max_length=2500)
    disclosed = models.DateField("Anunciado em")
    owners = models.CharField("quantidade de donos", max_length=50)
    visible = models.IntegerField("visivel")
    
    class Meta:
        verbose_name = "Carro"
        verbose_name_plural = "Carros"
        ordering = ["price"]
    
    def __str__(self) -> str:
        return self.name