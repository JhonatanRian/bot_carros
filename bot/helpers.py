from requests_html import HTMLSession
class Car:
    def __init__(self: object,
                 name: str,
                 price: str,
                 year: str,
                 km: str,
                 fonte: str,
                 photo: str,
                 found: str):
        self.name = name
        self.price= price
        self.year = year
        self.km = km
        self.fonte = fonte
        self.photo = photo
        self.found = found
        
def getproxys():
    url = "https://free-proxy-list.net/"
    session = HTMLSession()
    response = session.get(url)
    html = response.html
    elem = html.element
    elements = elem.find("tr")
    lista = []
    for el in elements:
        try:
            dado = el.cssselect("td")[0]
            ip = dado.text_content()
            dado = el.cssselect("td")[1]
            port = dado.text_content()
            dado = el.cssselect("td")[5]
            dado = dado.text_content()
            if dado == "yes":
                lista.append({"ip": ip, "port": port})
        except:
            pass
    return (lista)

if __name__ == "__main__":
    print(getproxys())