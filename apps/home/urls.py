# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.contrib.auth.views import LogoutView


urlpatterns = [

    # The home page
    path('', views.index, name='painel'),
    path('', views.index, name='home'),
    path('', views.index, name='home'),
    path('painel', views.index, name='index'),
    path('save', views.save, name='save'),
    path('delete', views.delete, name='delete'),
    # path("logout/", LogoutView.as_view(), name="logout"),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
