from flask_restx import Namespace, Resource

inventory_ns = Namespace(
    "inventory",
    description="Inventory management"
)

@inventory_ns.route("/")
class InventoryIndex(Resource):
    @inventory_ns.doc("inventory_index")
    def get(self):
        return {"module": "inventory", "status": "ok"}, 200
