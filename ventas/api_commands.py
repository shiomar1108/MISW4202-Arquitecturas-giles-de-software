from base import app, api, ma, db, Venta, venta_schema, q, Resource, Flask, request
from sender import send_venta
from putter import put_venta

class VentaListResource(Resource):

    def post(self):

        q.enqueue(send_venta, venta_schema.dump(venta))


class VentaResource(Resource):

    def put(self, venta_id):

         q.enqueue(put_venta, venta_schema.dump(venta))