from datetime import date
from typing import Tuple
from requests_html import HTMLSession
from home.bot.helpers import Car


def get() -> Tuple[Car]:
    session = HTMLSession()

    URL_BASE = "https://www.icarros.com.br/ache/listaanuncios.jsp?bid=0&pag=1&lis=0&ord=24&sop=sta_1.1_-cid_9668.1_-esc_2.1_-rai_50.1_-tan_1.1_"
    SELECTOR = ".anuncio_container"

    r = session.get(URL_BASE)
    html = r.html
    elements = html.find(SELECTOR)
    
    lista = []
    for element in elements:
        try:
            name = element.element.cssselect("a[class='clearfix']")[0].attrib["title"]
            source = "https://www.icarros.com.br" + element.element.cssselect("a[class='clearfix']")[0].attrib["href"]
            owner = get_data(source)
            price = "".join([x for x in element.element.cssselect("h3")[0].text_content() if x.isdigit()])
            ano = "".join([x for x in element.element.cssselect("div:nth-child(2) a ul li[class='primeiro']")[0].text_content().split("/")[0] if x.isdigit()])
            km = "".join([x for x in element.element.cssselect("div:nth-child(2) a ul li[class='usado']")[0].text_content() if x.isdigit()])
            try:
                img = element.element.cssselect(".imglazy")[0].attrib["src"]
            except:
                try:
                    img = element.element.cssselect(".imglazy")[0].attrib["data-src"]
                except:
                    img = ''
            lista.append(Car(name=name, price=price, year=ano, km=km, photo=img, source=source, owners=owner, disclosed=date.today()))
        except Exception as err:
            print(err)
            print(source)
    return tuple(lista)

def get_data(url):
    session = HTMLSession()
    SELECTOR = "body > div > div:nth-child(4) > div > div > div > div:nth-child(1) > ul"
    response = session.get(url)
    html = response.html
    text = html.find(SELECTOR)[0].element.text_content()
    
    verify_prop1 = "proprietários anteriores: 1" in text or "segundo dono" in text or "segundo propietário" in text
    verify_prop2 = verify = "proprietários anteriores: 0" in text or "único dono" in text or "único propietário" in text or "unido dono" in text or "unido propietário" in text

    if verify_prop1:
        owners = "2"
    elif verify_prop2:
        owners = "1"
    else:
        owners = "não definido"
    
    return owners

if __name__ == "__main__":
    print(get())