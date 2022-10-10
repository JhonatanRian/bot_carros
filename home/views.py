# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import json
from django import template
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from home.models import Cars, Year

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
    try:
        market = request.GET["market"]
        if market == "M":
            market = "Mercado Livre"
            all_cars = Cars.objects.filter(provider_name="Mercado Livre", visible=True)
        elif market == "I":
            market = "Icarros"
            all_cars = Cars.objects.filter(provider_name="Icarros", visible=True)
        elif market == "W":
            market = "Webmotors"
            all_cars = Cars.objects.filter(provider_name="Webmotors", visible=True)
        else:
            all_cars = Cars.objects.all().filter(visible=True)
    except:
        market = None
        all_cars = Cars.objects.all().filter(visible=True)
    
    option = "name"
    search = ""
    try:
        search = request.GET["search"]
        option = request.GET["option"]
        if option == "name":
           all_cars = all_cars.filter(name__icontains=search.strip(), visible=True)
        elif option == "km":
            k1 = search.split("/")[0]
            k2 = search.split("/")[1]
            all_cars = Cars.objects.search_km(all_cars, k1, k2)
        elif option == "price":
            p1 = search.split("/")[0]
            p2 = search.split("/")[1]
            all_cars = Cars.objects.search_price(all_cars, p1, p2)
        elif option == "year":
            p1 = search.split("/")[0]
            p2 = search.split("/")[1]
            all_cars = Cars.objects.search_year(all_cars, p1, p2)
        elif option == "owner":
            all_cars = all_cars.filter(owners=search, visible=True)
        else:
            ...
            
    except Exception as err:
        ...

    v = ""
    v1 = ""
    v2 = ""
    try:
        v1 = search.split("/")[0]
        v2 = search.split("/")[1]
    except:
        v = search
        
    context = {'cars': all_cars, "v": v, "v1": v1, "v2": v2, "op": option}

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
                
                if Year.objects.filter(name=car["year"].split("/")[0]).exists():
                    d = Year.objects.get(name=car["year"].split("/")[0])
                else:
                    d = Year.objects.create(
                        name=car["year"].split("/")[0]
                    )
                
                Cars.objects.create(
                    name=car["name"].lower().strip(),
                    price="".join([x for x in car["price"] if x.isdigit()]),
                    km="".join([x for x in car["km"] if x.isdigit()]),
                    year=d,
                    source=car["source"],
                    found_in="https://www.webmotors.com.br/carros/estoque?tipoveiculo=carros&anunciante=Pessoa%20F%C3%ADsica",
                    provider_name="Webmotors",
                    photo=car["img"],
                    disclosed=date.today(),
                    owners=car["owner"],
                    visible=1
                    )
        return HttpResponse(json.dumps({"AVISO MANÉ": "Deu sorte, teu código funcinou"}), content_type='application/json')
    except Exception as err:
        print(err)
        return HttpResponse(json.dumps({"AVISO MANÉ": "Algo de errado não está certo"}), content_type='application/json')

@login_required(login_url="/login/")
def delete(request):
    id_ = request.GET["id"]

    if id_.isdigit():
        car = Cars.objects.get(id=id_)
        car.visible = 0
        car.save()
    else:
        all_cars = Cars.objects.all().filter(visible=1)
        for car in all_cars:
            car.visible = 0
    
    return HttpResponse(json.dumps({"del": "ete"}), content_type='application/json')