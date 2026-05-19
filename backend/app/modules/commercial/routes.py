from flask_restx import Namespace, Resource

commercial_ns = Namespace(
    "commercial",
    description="Commercial operations"
)

@commercial_ns.route("/")
class CommercialIndex(Resource):
    @commercial_ns.doc("commercial_index")
    def get(self):
        return {"module": "commercial", "status": "ok"}, 200
