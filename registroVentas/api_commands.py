from base import app, api, ma, db, process_venta,  q, Resource, Flask, request

class RegistroVentaResource(Resource):

    def post(self):

        venta = q.popleft()