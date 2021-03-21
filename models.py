from datetime import datetime
from hashlib import sha256
from manage import Conexiondb

"""

Restaurants (
    id TEXT PRIMARY KEY, -- Unique Identifier of Restaurant
    rating INTEGER, -- Number between 0 and 4
    name TEXT, -- Name of the restaurant
    site TEXT, -- Url of the restaurant
    email TEXT,
    phone TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    lat FLOAT, -- Latitude
    lng FLOAT -- Longitude
)    
"""


class Restaurants():
    conexion = None

    def __init__(self):
        self.conexion = Conexiondb()

    def create(self, data):
        id = sha256(datetime.today().__str__()).hexdigest()
        cursor = self.conexion.ejecutar(
            "INSERT INTO restaurants(id, rating, name, site, email, phone, street, city, state, lat, lng)"
            " VALUES ('{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', ?, ?);".format(
                id, data["rating"], data["name"], data["site"], data["email"], data["phone"], data["street"],
                data["city"], data["state"], data["lat"], data["lng"]
            )
        )
        return cursor

    def filter(self, filter=None):
        sql = "select * from restaurants"
        if filter:
            sql = "{} Where upper(restaurants.*::text) like upper('%baja%')".format(sql, filter)
        cursor = self.conexion.ejecutar(sql)
        return self.estructura(cursor.fetchall())

    def filter_geo(self, data):
        sql = "select res.*, ST_Distance(ST_MakePoint(res.lng, res.lat)::geography, ref_geoloc) AS distance " \
              "from restaurants res CROSS JOIN (" \
              "SELECT ST_MakePoint({lng}, {lat})::geography AS ref_geoloc) AS r " \
              "WHERE ST_DWithin(ST_MakePoint(res.lng, res.lat)::geography, ref_geoloc, {distancia}) " \
              "ORDER BY ST_Distance(ST_MakePoint(res.lng, res.lat), ref_geoloc);".format(lng=data[1], lat=data[0], distancia=data[2])

        cursor = self.conexion.ejecutar(sql)
        return self.estructura_distancia(cursor.fetchall())

    def raiting(self, tipo, filter=None):
        sql = "select * from restaurants"
        if tipo == 1:
            sql = "select state, city, rating, count(id) from restaurants where upper(state||city||rating)::text like upper('%{}%') group by state, city, rating order by state, city, rating ;".format(filter)
        if tipo == 2:
            sql = "select state, rating, count(id) from restaurants where upper(state||city||rating)::text like upper('%{}%') group by state, rating order by state, rating;".format(filter)
        if tipo == 3:
            sql = "select rating, count(id) from restaurants where rating::text like '%{}%'  group by rating order by rating;".format(filter)
        cursor = self.conexion.ejecutar(sql)
        return self.estructura_estadisticas(tipo, cursor.fetchall())

    def delete(self, id):
        cursor = None
        if id:
            cursor = self.conexion.ejecutar("delete from restaurants where id = {}".format(id))
        return cursor.fetchall()

    def update(self, data):
        cursor = None
        if id and data:
            cursor = self.conexion.ejecutar(
                "UPDATE restaurants "
                "SET rating={}, name={}, site={}, email={}, phone={}, street={}, city={}, state={}, lat={}, lng={}"
                "WHERE id = {}".format(
                    data["rating"], data["name"], data["site"], data["email"], data["phone"], data["street"],
                    data["city"], data["state"], data["lat"], data["lng"], data["id"]
                )
            )
        return cursor.fetchall()

    def estructura(self, objecto):
        data = []
        for obj in objecto:
            data.append({
                "id": obj[0],
                "rating": obj[1],
                "name": obj[2],
                "site": obj[3],
                "email": obj[4],
                "phone": obj[5],
                "street": obj[6],
                "city": obj[7],
                "state": obj[8],
                "lat": obj[9],
                "lng": obj[10]
            })
        return data

    def estructura_distancia(self, objecto):
        data = []
        for obj in objecto:
            data.append({
                "id": obj[0],
                "rating": obj[1],
                "name": obj[2],
                "site": obj[3],
                "email": obj[4],
                "phone": obj[5],
                "street": obj[6],
                "city": obj[7],
                "state": obj[8],
                "lat": obj[9],
                "lng": obj[10],
                "distancia": obj[11],
            })
        return data

    def estructura_estadisticas(self, tipo, objecto):
        data = []
        for obj in objecto:
            if tipo == 1:
                data.append({
                    "state": obj[0],
                    "city": obj[1],
                    "rating": obj[2],
                    "total": obj[3]
                })
            if tipo == 2:
                data.append({
                    "state": obj[0],
                    "rating": obj[1],
                    "total": obj[2]
                })
            if tipo == 3:
                data.append({
                    "rating": obj[0],
                    "total": obj[1]
                })
        return data
