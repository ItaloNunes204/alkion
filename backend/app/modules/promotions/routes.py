from flask_restx import Namespace, Resource

promotions_ns = Namespace(
    "promotions",
    description="Promotion management"
)

@promotions_ns.route("/")
class PromotionsIndex(Resource):
    @promotions_ns.doc("promotions_index")
    def get(self):
        return {"module": "promotions", "status": "ok"}, 200
