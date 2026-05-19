from flask_restx import Namespace, Resource

wms_ns = Namespace(
    "wms",
    description="Warehouse Management System"
)

@wms_ns.route("/")
class WmsIndex(Resource):
    @wms_ns.doc("wms_index")
    def get(self):
        return {"module": "wms", "status": "ok"}, 200
