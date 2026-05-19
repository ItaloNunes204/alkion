from flask_restx import Namespace, Resource

sales_force_ns = Namespace(
    "sales_force",
    description="Sales Force management"
)

@sales_force_ns.route("/")
class SalesForceIndex(Resource):
    @sales_force_ns.doc("sales_force_index")
    def get(self):
        return {"module": "sales_force", "status": "ok"}, 200
