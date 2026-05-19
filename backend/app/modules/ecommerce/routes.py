from flask_restx import Namespace, Resource

ecommerce_ns = Namespace(
    "ecommerce",
    description="E-commerce operations"
)

@ecommerce_ns.route("/")
class EcommerceIndex(Resource):
    @ecommerce_ns.doc("ecommerce_index")
    def get(self):
        return {"module": "ecommerce", "status": "ok"}, 200
