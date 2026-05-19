from flask_restx import Namespace, Resource

accounting_ns = Namespace(
    "accounting",
    description="Accounting management"
)

@accounting_ns.route("/")
class AccountingIndex(Resource):
    @accounting_ns.doc("accounting_index")
    def get(self):
        return {"module": "accounting", "status": "ok"}, 200