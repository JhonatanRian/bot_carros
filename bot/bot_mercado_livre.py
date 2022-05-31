from datetime import date
from requests_html import HTMLSession
from helpers import Car


def get():
    session = HTMLSession()

    URL_BASE = "https://lista.mercadolivre.com.br/carros#D[A:carros]"
    SELECTOR = "#root-app > div > div > section > ol > li > div > div"

    r = session.get(URL_BASE)
    html = r.html
    elements = html.find(SELECTOR)
        
    lista = []
    for eleme in elements:
        el = eleme.element
        source = el.cssselect("a")[1].attrib["href"] ; print("source")
        data = get_data(source)
        if data:
            price = el.find_class("price-tag-text-sr-only")[0].text_content().split()[0] ; print("price")
            ano = el.find_class("ui-search-card-attributes__attribute")[0].text_content() ; print("ano")
            km = el.find_class("ui-search-card-attributes__attribute")[1].text_content() ; print("km")
            name = el.find_class("ui-search-item__group ui-search-item__group--title")[0].text_content() ; print("name")
            try:
                img = el.cssselect("img")[0].attrib["data-src"]
            except:
                img = el.cssselect("img")[0].attrib["src"]
            lista.append(Car(price=price, year=ano, km=km, name=name, source=source, photo=img, disclosed=data["disclosed"], owners=data["owners"]))
    return tuple(lista)

def get_data(url) -> dict:
    session = HTMLSession()
    return_values = {}
    
    URL = url
    SELECTOR_INFO = "#root-app > div > div.ui-pdp-container.ui-pdp-container--pdp > div > div.ui-pdp-container__col.col-2.pb-40 > div.ui-pdp-container__col.col-1.ui-vip-core-container--content-left"
    SELECTOR_DAYS = "#root-app > div > div.ui-pdp-container.ui-pdp-container--pdp > div > div.ui-pdp-container__col.col-1.ui-pdp-container--column-right.mt-16.pr-16 > div.ui-pdp-container__row.ui-pdp-component-list.pr-16.pl-16 > div > div.ui-pdp-container__row.ui-pdp-container__row--header > div > div.ui-pdp-header__subtitle > span"

    response = session.get(URL)
    html = response.html
    element_days = html.find(SELECTOR_DAYS)[0]
    days = "".join([x for x in element_days.element.text_content().split("·")[1] if x.isdigit()])
    verify = element_days.element.text_content().split("·")[1]
    if "dias" in verify and int(days) < 5:
        disclosed = date(date.today().year, date.today().month, int(days))
        
        text_info = html.find(SELECTOR_INFO)[0].element.text_content().lower()
        
        verify_prop1 = "proprietários anteriores: 1" in text_info or "segundo dono" in text_info or "segundo propietário" in text_info
        verify_prop2 = verify = "proprietários anteriores: 0" in text_info or "único dono" in text_info or "único propietário" in text_info or "unido dono" in text_info or "unido propietário" in text_info

        if verify_prop1:
            owners = "2"
        elif verify_prop2:
            owners = "1"
        else:
            owners = "não definido"
        
        return_values["owners"] = owners
        return_values["disclosed"] = disclosed
        
        return return_values
