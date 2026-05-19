from flask_restx import Namespace, Resource

fiscal_ns = Namespace(
    "fiscal",
    description="Fiscal operations"
)

@fiscal_ns.route("/")
class FiscalIndex(Resource):
    @fiscal_ns.doc("fiscal_index")
    def get(self):
        return {"module": "fiscal", "status": "ok"}, 200
