import psycopg2


class Conexiondb:
    conexion = None

    def __init__(self):
        credenciales = {
            "dbname": "testapi",
            "user": "postgres",
            "password": "psql",
            "host": "localhost",
            "port": 5432
        }
        self.conexion = psycopg2.connect(**credenciales)
        super().__init__()

    def ejecutar(self, query):
        cursor = self.conexion.cursor()
        cursor.execute(query)
        return cursor

    def close(self):
        self.conexion.close()
