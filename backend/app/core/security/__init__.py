from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

# Decorations for route protection based on permissions and client types
def requer_permissao(codigo: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            usuario_id = get_jwt_identity()

            from app.modules.auth.services import verificar_permissao
            if not verificar_permissao(usuario_id, codigo):
                return jsonify({
                    "erro": "Você não tem permissão para esta ação",
                    "permissao_necessaria": codigo
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Decorations for route protection based on client types (e.g., web, mobile, admin)
def requer_cliente(*clientes_permitidos: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            cliente_atual = getattr(g, "client_type", "web")

            if cliente_atual not in clientes_permitidos:
                return jsonify({
                    "erro": f"Esta rota não está disponível para '{cliente_atual}'",
                    "clientes_permitidos": list(clientes_permitidos)
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Decorations for route protection based on specific client types
def requer_admin():
    return requer_cliente("admin")