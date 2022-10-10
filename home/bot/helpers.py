from datetime import date


class Car:
    def __init__(self: object,
                 name: str,
                 price: str,
                 year: str,
                 km: str,
                 source: str,
                 photo: str,
                 disclosed: date,
                 owners: str):
        self.name = name
        self.price= price
        self.year = year
        self.km = km
        self.source = source
        self.photo = photo
        self.disclosed = disclosed
        self.owners = owners