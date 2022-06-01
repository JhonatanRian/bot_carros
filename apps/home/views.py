# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json
from datetime import date
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from apps.home.models import Cars

def dict2obj(d): 
    if isinstance(d, list): 
        d = [dict2obj(x) for x in d]  
    if not isinstance(d, dict): 
        return d 
    class C: 
        pass
    obj = C() 
    for k in d: 
        obj.__dict__[k] = dict2obj(d[k]) 
   
    return obj 

@login_required(login_url="/login/")
def index(request):
    all_cars = Cars.objects.all()
    context = {'cars': all_cars}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@csrf_exempt
def save(request):
    cars = json.loads(request.body)
    try:
        for car in cars:
            if not Cars.objects.filter(source=car["source"]).exists():
                Cars.objects.create(
                    name=car["name"],
                    price=car["price"],
                    km=car["km"],
                    year=car["year"],
                    source=car["source"],
                    found_in=car["https://www.webmotors.com.br/carros/estoque?tipoveiculo=carros&anunciante=Pessoa%20F%C3%ADsica"],
                    provider_name="Webmotors",
                    photo=car["img"],
                    disclosed=date.today(),
                    owners=car["owner"],
                    visible=1
                    )
        return HttpResponse(json.dumps({"AVISO MANÉ": "Deu sorte, teu código funcinou"}), content_type='application/json')
    except:
        return HttpResponse(json.dumps({"AVISO MANÉ": "Algo de errado não está certo"}), content_type='application/json')