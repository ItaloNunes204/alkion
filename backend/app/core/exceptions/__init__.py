from flask import jsonify

class AlkionException(Exception):
    status_code = 400
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class NotFoundError(AlkionException):
    status_code = 404

class UnauthorizedError(AlkionException):
    status_code = 401

class ForbiddenError(AlkionException):
    status_code = 403

class ValidationError(AlkionException):
    status_code = 422

class ConflictError(AlkionException):
    status_code = 409

def register_error_handlers(app):
    @app.errorhandler(AlkionException)
    def handle_alkion(e):
        return jsonify({
            "erro": e.message,
            "tipo": type(e).__name__
        }), e.status_code

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro": "Endpoint não encontrado"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"erro": "Método HTTP não permitido"}), 405

    @app.errorhandler(500)
    def internal(e):
        return jsonify({"erro": "Erro interno do servidor"}), 500