from flask_restx import Namespace, Resource

pos_ns = Namespace(
    "pos",
    description="Point of Sale operations"
)

@pos_ns.route("/")
class PosIndex(Resource):
    @pos_ns.doc("pos_index")
    def get(self):
        return {"module": "pos", "status": "ok"}, 200
