from flask_restx import Namespace, Resource

financial_ns = Namespace(
    "financial",
    description="Financial operations"
)

@financial_ns.route("/")
class FinancialIndex(Resource):
    @financial_ns.doc("financial_index")
    def get(self):
        return {"module": "financial", "status": "ok"}, 200
