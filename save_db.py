import os
from bot import bot_mercado_livre
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
get_wsgi_application()

from apps.home.models import Cars

PROVIDER_NAME = "Mercado Livre"
PROVIDER_URL = "https://www.mercadolivre.com.br/"

def init_save():
    carros = bot_mercado_livre.get()

    for carro in carros:
        Cars.objects.create(
            name=carro.name,
            price=carro.price,
            km=carro.km,
            year=carro.year,
            source=carro.fonte,
            photo=carro.photo,
            provider_name=PROVIDER_NAME,
            provider_url=PROVIDER_URL,
            found_in=carro.found
        )
        
if __name__ == "__main__":
    init_save()