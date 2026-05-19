from flask_restx import Namespace, Resource

auth_ns = Namespace(
    "auth",
    description="Authentication and access control"
)

@auth_ns.route("/")
class AuthIndex(Resource):
    @auth_ns.doc("auth_index")
    def get(self):
        return {"module": "auth", "status": "ok"}, 200
