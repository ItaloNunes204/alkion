from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from dotenv import load_dotenv

from .core.config import config_by_name
from .core.extensions import db, migrate, jwt, redis_client
from .core.exceptions import register_error_handlers
from .core.middleware import register_middlewares

load_dotenv()

api = Api(
    title="Alkion API",
    version="1.0.0",
    description="API REST do sistema de gestao Alkion",
    doc="/docs",
)


def create_app(config_name: str = "development") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    redis_client.init_app(app)
    api.init_app(app)

    register_error_handlers(app)
    register_middlewares(app)
    _register_namespaces()

    return app


def _register_namespaces():
    from .modules.auth.routes       import auth_ns
    from .modules.sync.routes       import sync_ns
    from .modules.pos.routes        import pos_ns
    from .modules.inventory.routes  import inventory_ns
    from .modules.financial.routes  import financial_ns
    from .modules.fiscal.routes     import fiscal_ns
    from .modules.production.routes import production_ns
    from .modules.commercial.routes import commercial_ns
    from .modules.accounting.routes import accounting_ns
    from .modules.wms.routes        import wms_ns
    from .modules.loyalty.routes    import loyalty_ns
    from .modules.sales_force.routes import sales_force_ns
    from .modules.bi.routes         import bi_ns
    from .modules.ecommerce.routes  import ecommerce_ns
    from .modules.promotions.routes import promotions_ns
    from .modules.order.routes      import order_ns
    from .modules.erp.routes        import erp_ns
    from .modules.plans.routes      import plans_ns
    from .modules.companies.routes import companies_ns

    namespaces = [
        (auth_ns,        "/api/v1/auth"),
        (sync_ns,        "/api/v1/sync"),
        (pos_ns,         "/api/v1/pos"),
        (inventory_ns,   "/api/v1/inventory"),
        (financial_ns,   "/api/v1/financial"),
        (fiscal_ns,      "/api/v1/fiscal"),
        (production_ns,  "/api/v1/production"),
        (commercial_ns,  "/api/v1/commercial"),
        (accounting_ns,  "/api/v1/accounting"),
        (wms_ns,         "/api/v1/wms"),
        (loyalty_ns,     "/api/v1/loyalty"),
        (sales_force_ns, "/api/v1/sales-force"),
        (bi_ns,          "/api/v1/bi"),
        (ecommerce_ns,   "/api/v1/ecommerce"),
        (promotions_ns,  "/api/v1/promotions"),
        (order_ns,       "/api/v1/orders"),
        (erp_ns,         "/api/v1/erp"),
        (plans_ns,       "/api/v1/plans"),
        (companies_ns,   "/api/v1/companies"),
    ]

    for ns, path in namespaces:
        api.add_namespace(ns, path=path)