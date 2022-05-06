from requests_html import HTMLSession
from bot.helpers import Car
session = HTMLSession()

URL_BASE = "https://lista.mercadolivre.com.br/carros#D[A:carros]"
SELECTOR = "#root-app > div > div > section > ol > li > div > div"

r = session.get(URL_BASE)
html = r.html
elements = html.find(SELECTOR)

def get():
    lista = []
    for eleme in elements:
        el = eleme.element
        try:
            price = el.find_class("price-tag-text-sr-only")[0].text_content().split()[0]
            ano = el.find_class("ui-search-card-attributes__attribute")[0].text_content()
            km = el.find_class("ui-search-card-attributes__attribute")[1].text_content()
            name = el.find_class("ui-search-item__group ui-search-item__group--title")[0].text_content()
            fonte = el.cssselect("a")[1].attrib["href"]
            img = el.cssselect("img")[0].attrib["data-src"]
            lista.append(Car(price=price, year=ano, km=km, name=name, fonte=fonte, photo=img, found=URL_BASE))
        except:
            pass
    return tuple(lista)