from flask import jsonify

# base exception class for all custom exceptions
class AlkionException(Exception):
    status_code = 400
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# specific exceptions for common error scenarios
class NotFoundError(AlkionException):
    status_code = 404

# specific exceptions for authentication and authorization errors
class UnauthorizedError(AlkionException):
    status_code = 401

# specific exceptions for forbidden access
class ForbiddenError(AlkionException):
    status_code = 403

# specific exceptions for validation errors
class ValidationError(AlkionException):
    status_code = 422

# specific exceptions for conflict errors
class ConflictError(AlkionException):
    status_code = 409

# specific exceptions for internal server errors
def register_error_handlers(app):
    @app.errorhandler(AlkionException)
    def handle_alkion(e):
        return jsonify({
            "success": False,
            "message": e.message,
            "data": None,
            "tipo": type(e).__name__
        }), e.status_code

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "success": False,
            "message": "Endpoint not found",
            "data": None
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "success": False,
            "message": "HTTP method not allowed",
            "data": None
        }), 405

    @app.errorhandler(500)
    def internal(e):
        return jsonify({
            "success": False,
            "message": "Internal server error",
            "data": None
        }), 500