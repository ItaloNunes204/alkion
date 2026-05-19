from flask_restx import Namespace, Resource

bi_ns = Namespace(
    "bi",
    description="Business Intelligence"
)

@bi_ns.route("/")
class BiIndex(Resource):
    @bi_ns.doc("bi_index")
    def get(self):
        return {"module": "bi", "status": "ok"}, 200
