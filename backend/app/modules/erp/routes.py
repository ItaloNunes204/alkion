from flask_restx import Namespace, Resource

erp_ns = Namespace(
    "erp",
    description="Enterprise Resource Planning"
)

@erp_ns.route("/")
class ErpIndex(Resource):
    @erp_ns.doc("erp_index")
    def get(self):
        return {"module": "erp", "status": "ok"}, 200
