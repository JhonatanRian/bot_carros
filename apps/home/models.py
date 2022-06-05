# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CarsManager(models.Manager):
    
    def search_price(self, query, p1, p2):
        lista = []
        for car in query:
            if int(car.price) >= int(p1) and int(car.price) <= int(p2):
                lista.append(car)
        return tuple(lista)
        
    def search_km(self, query, k1, k2):
        lista = []
        for car in query:
            if int(car.km) >= int(k1) and int(car.km) <= int(k2):
                lista.append(car)
        return tuple(lista)

class Year(models.Model):
    name = models.CharField(max_length=5)
    
    def __str__(self) -> str:
        return self.name
    

class Cars(models.Model):
    name = models.CharField("nome do carro", max_length=300)
    price = models.CharField("preço", max_length=15)
    km = models.CharField("kilometragem", max_length=100)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name="cars")
    source = models.CharField("link do anuncio", max_length=1500)
    found_in = models.CharField("url onde foi encontrado", max_length=1500)
    provider_name = models.CharField("Empresa anunciante", max_length=150)
    update = models.DateField("atualizado em", auto_now=True)
    photo = models.CharField("foto", max_length=2500)
    disclosed = models.DateField("Anunciado em")
    owners = models.CharField("quantidade de donos", max_length=50)
    visible = models.IntegerField("visivel")
    
    objects = CarsManager()
    
    class Meta:
        verbose_name = "Carro"
        verbose_name_plural = "Carros"
        ordering = ["price"]
    
    def __str__(self) -> str:
        return self.name
    
