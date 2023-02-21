from base import app, api, ma, db, RegistroVenta, process_venta,  registroventa_schema, q, Resource, Flask, request

class RegistroVentaResource(Resource):

    def post(self):

        venta = q.popleft()