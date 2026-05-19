from flask_restx import Namespace, Resource

loyalty_ns = Namespace(
    "loyalty",
    description="Loyalty program management"
)

@loyalty_ns.route("/")
class LoyaltyIndex(Resource):
    @loyalty_ns.doc("loyalty_index")
    def get(self):
        return {"module": "loyalty", "status": "ok"}, 200
