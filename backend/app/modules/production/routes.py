from flask_restx import Namespace, Resource

production_ns = Namespace(
    "production",
    description="Production management"
)

@production_ns.route("/")
class ProductionIndex(Resource):
    @production_ns.doc("production_index")
    def get(self):
        return {"module": "production", "status": "ok"}, 200
