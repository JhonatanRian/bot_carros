from os import system
from unicodedata import name
from celery import shared_task
from celery.utils.log import get_task_logger
from apps.home.models import Cars, Year
from apps.home.bot.bot_mercado_livre import get as get_mercado_livre
from apps.home.bot.bot_icarros import get as get_icarros
from apps.home.bot.helpers import Car

logger = get_task_logger(__name__)

@shared_task
def save_cars_mercado_livre():
    logger.info("Capturando informações - Mercado Livre")
    cars = get_mercado_livre()
    for car in cars:
        car: Car = car
        try:
            if Year.objects.filter(name=car.year).exists():
                d = Year.objects.get(name=car.year)
            else:
                d = Year.objects.create(
                    name=car.year
                )
            Cars.objects.create(
                name=car.name.lower().strip(),
                price=car.price,
                km=car.km,
                year=d,
                source=car.source,
                found_in="https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/particular/carros_NoIndex_True#applied_filter_id%3Dseller_type%26applied_filter_name%3DVendedor%26applied_filter_order%3D11%26applied_value_id%3Dprivate_seller%26applied_value_name%3DParticular%26applied_value_order%3D2%26applied_value_results%3D3017%26is_custom%3Dfalse",
                provider_name="Mercado Livre",
                photo=car.photo,
                disclosed=car.disclosed,
                owners=car.owners,
                visible=1
                )
            logger.info("salvo")
        except:
            ...

@shared_task
def save_icarros():
    logger.info("Capturando informação - Icarros")
    cars = get_icarros()
    logger.info(len(cars))
    for car in cars:
        car: Car = car
        
        try:
            if Year.objects.filter(name=car.year).exists():
                d = Year.objects.get(name=car.year)
            else:
                d = Year.objects.create(
                    name=car.year
                )
            Cars.objects.create(
                name=car.name.lower().strip(),
                price=car.price,
                km=car.km,
                year=d,
                source=car.source,
                found_in="https://www.icarros.com.br/ache/listaanuncios.jsp?bid=0&pag=1&lis=0&ord=14&sop=sta_1.1_-esc_4.1_-rai_0.1_-tan_1.1_",
                provider_name="Icarros",
                photo=car.photo,
                disclosed=car.disclosed,
                owners=car.owners,
                visible=1
                )
            logger.info("salvo um carro")
        except:
            ...
        

