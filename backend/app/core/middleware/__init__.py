import time
from flask import g, request, jsonify

CLIENTES_VALIDOS = {"web", "mobile", "desktop", "admin"}

def register_middlewares(app):

    @app.before_request
    def iniciar_request():
        g.start_time = time.time()

        cliente = request.headers.get("X-Client-Type", "web").lower()

        if cliente not in CLIENTES_VALIDOS:
            return jsonify({
                "erro": "Cliente não reconhecido",
                "dica": "Envie o header X-Client-Type: web | mobile | desktop | admin"
            }), 400
        g.client_type = cliente

    @app.after_request
    def finalizar_request(response):
        duracao = time.time() - getattr(g, "start_time", time.time())
        response.headers["X-Response-Time"]      = f"{duracao:.4f}s"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"]        = "DENY"
        return response