import flask
from flask import jsonify, request
from models import Restaurants

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def inicio():
    return '''<h1>Test de apis</h1>
<p>Pruebas de CRUD del modelo de Restaurante.</p>'''


### Funciones de Apis de CRUD
##############################
@app.route("/api/restaurant/", methods=['GET'])
def restaurant_all():
    filter = ""
    if request.form['q']:
        filter = request.form['q']
    rest = Restaurants()
    restaurants = rest.filter(filter)
    return jsonify(restaurants)


@app.route("/api/restaurant/nuevo/", methods=['POST'])
def restaurant_new():
    """
        @rating: Number between 0 and 4
        @name: Name of the restaurant
        @site: Url of the restaurant
        @email: Email of the restaurant
        @phone: Phone of the restaurant
        @street: Street of the restaurant
        @city: City of the restaurant
        @state: State of the restaurant
        @lat: Latitude of the restaurant
        @lng: Longitude of the restaurant
    :return: Notification of query
    """
    rest = Restaurants()
    rest.create(request.args)
    restaurants = [{"success": "El registro de restaurante es satisfactorio"}]
    return jsonify(restaurants)


@app.route("/api/restaurant/editar/", methods=['PUT'])
def restaurant_edit():
    """
        @id: Unique Identifier of Restaurant
        @rating: Number between 0 and 4
        @name: Name of the restaurant
        @site: Url of the restaurant
        @email: Email of the restaurant
        @phone: Phone of the restaurant
        @street: Street of the restaurant
        @city: City of the restaurant
        @state: State of the restaurant
        @lat: Latitude of the restaurant
        @lng: Longitude of the restaurant
    :return: Notification of query
    """
    restaurants = None
    if request.args['id']:
        rest = Restaurants()
        restaurants = rest.update(request.args)
    else:
        restaurants = [{"error": "El id es un campo obligatorio para la actualización"}]
    return jsonify(restaurants)


@app.route("/api/restaurant/eliminar/", methods=['DELETE'])
def restaurant_delete():
    restaurants = None
    if request.args['id']:
        rest = Restaurants()
        restaurants = rest.filter_geo(request.args['id'])
    else:
        restaurants = [{"error": "El id es un campo obligatorio para la eliminación del registro"}]
    return jsonify(restaurants)


@app.route("/api/restaurant/georeferencia/", methods=['GET'])
def restaurant_geo():
    """
        Api de estadisticas por tipo y filtros de busqueda
        @distancia = distancia en metros default 100 mtrs
        @lat = Parametro de la latitud del punto central ***Obligatorio***
        @lng = Parametro de la longitud del punto central ***Obligatorio***
    """
    restaurants = None
    if request.args['lat'] and request.args['lng']:
        rest = Restaurants()
        distancia = 100
        if request.args['distancia']:
            distancia = request.args['distancia']
        data = [request.args['lat'], request.args['lng'], distancia]
        restaurants = rest.filter_geo(data)
    return jsonify(restaurants)


@app.route("/api/restaurant/estadisticas/", methods=['GET'])
def restaurant_estadisticas():
    """
        Api de estadisticas por tipo y filtros de busqueda
        @tipo = 1(Estado, ciudad, raiting), 2(Estado, raiting), 3(Raiting) ***Obligatorio***
        @q = Parametro de filtrado por nombre, ciudad, estado, raiting
    """
    filter = ""
    restaurants = None
    if request.args:
        try:
            tipo = int(request.args['tipo'])
            try:
                if request.args['q']:
                    filter = request.args['q']
            except:
                pass
            rest = Restaurants()
            restaurants = rest.raiting(tipo, filter)
        except:
            restaurants = [{"error": "El tipo de filtro es obligatorio y de valor numerico"}]
    else:
        restaurants = [{"error": "No se recibio ningun parametro de filtrado"}]
    return jsonify(restaurants)


@app.errorhandler(404)
def recurso_no_encontrado(e):
    return "<h1>404</h1><p>Recurso no encontrado.</p>", 404


if __name__ == '__main__':
    app.run()