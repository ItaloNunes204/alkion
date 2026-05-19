from flask_restx import Namespace, Resource

sync_ns = Namespace(
    "sync",
    description="Offline sync for mobile and desktop"
)

@sync_ns.route("/")
class SyncIndex(Resource):
    @sync_ns.doc("sync_index")
    def get(self):
        return {"module": "sync", "status": "ok"}, 200