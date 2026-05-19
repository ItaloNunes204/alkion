from flask_restx import Namespace, Resource

order_ns = Namespace(
    "order",
    description="Order management"
)

@order_ns.route("/")
class OrderIndex(Resource):
    @order_ns.doc("order_index")
    def get(self):
        return {"module": "order", "status": "ok"}, 200
