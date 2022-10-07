from datetime import date, datetime
from requests_html import HTMLSession
from apps.home.bot.helpers import Car


def get():
    session = HTMLSession()

    URL_BASE = "https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes-em-sao-paulo/particular/carros_NoIndex_True#applied_filter_id%3Dstate%26applied_filter_name%3DLocaliza%C3%A7%C3%A3o%26applied_filter_order%3D6%26applied_value_id%3DTUxCUFNBT085N2E4%26applied_value_name%3DS%C3%A3o+Paulo%26applied_value_order%3D25%26applied_value_results%3D28125%26is_custom%3Dfalse"
    SELECTOR = "#root-app > div > div > section > ol > li > div > div"

    r = session.get(URL_BASE)
    html = r.html
    elements = html.find(SELECTOR)
        
    lista = []
    for eleme in elements:
        el = eleme.element
        source = el.cssselect("a")[1].attrib["href"]
        data = get_data(source)
        if data:
            price = el.find_class("price-tag-text-sr-only")[0].text_content().split()[0]
            ano = el.find_class("ui-search-card-attributes__attribute")[0].text_content()
            km = "".join([x for x in el.find_class("ui-search-card-attributes__attribute")[1].text_content() if x.isdigit()])
            name = el.find_class("ui-search-item__group ui-search-item__group--title")[0].text_content()
            try:
                img = el.cssselect("img")[0].attrib["data-src"]
            except:
                img = el.cssselect("img")[0].attrib["src"]
            lista.append(Car(price=price, year=ano, km=km, name=name, source=source, photo=img, disclosed=data["disclosed"], owners=data["owners"]))
    return tuple(lista)

def get_days_date(element_days, html, url):
    date_ = None
    days = "".join([x for x in element_days.element.text_content().split("·")[1] if x.isdigit()]) if '·' in element_days.element.text_content() else False
    if not days:
        element = html.find("#vehicle_history_specs > div > p")
        try:
            date_str = element[0].element.text_content().split()[-1].replace('/', '-')
            datetime_: datetime = datetime.strptime(date_str, "%d-%m-%Y")
            date_ = date(datetime_.year, datetime_.month, datetime_.day)
        except:
            ...
    elif days and "dias" in element_days.element.text_content() and int(days) <=10:
        date_ = date(date.today().year, date.today().month, int(days))
    
    return date_


def get_data(url) -> dict:
    session = HTMLSession()
    return_values = {}
    
    URL = url
    SELECTOR_INFO = "#root-app > div > div.ui-pdp-container.ui-pdp-container--pdp > div > div.ui-pdp-container__col.col-2.pb-40 > div.ui-pdp-container__col.col-1.ui-vip-core-container--content-left"
    SELECTOR_DAYS = "#root-app > div > div.ui-pdp-container.ui-pdp-container--pdp > div > div.ui-pdp-container__col.col-1.ui-pdp-container--column-right.mt-16.pr-16 > div.ui-pdp-container__row.ui-pdp-component-list.pr-16.pl-16 > div > div.ui-pdp-container__row.ui-pdp-container__row--header > div > div.ui-pdp-header__subtitle > span"

    response = session.get(URL)
    html = response.html
    element_days = html.find(SELECTOR_DAYS)[0]
    date_ = get_days_date(element_days, html, URL)
    if date_:

        disclosed = date_
        
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
    else:
        return False
