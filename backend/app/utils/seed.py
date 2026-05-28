from app.core.extensions import db
from app.modules.permissions.models import Permission
from app.modules.roles.models import Role

# This seed script is designed to be idempotent, meaning it can be run multiple times without creating duplicates.
def seed_permissions():
    permissions = [
        # PDV
        ("pdv:view",            "pdv",       "view",           "Access POS",              "Access the Point of Sale screen"),
        ("pdv:create_sale",     "pdv",       "create_sale",    "Create Sale",             "Register a new sale"),
        ("pdv:cancel_sale",     "pdv",       "cancel_sale",    "Cancel Sale",             "Cancel an existing sale"),
        ("pdv:apply_discount",  "pdv",       "apply_discount", "Apply Discount",          "Apply discount to a sale or item"),
        # Inventory
        ("inventory:view",      "inventory", "view",           "View Inventory",          "View products and stock levels"),
        ("inventory:create",    "inventory", "create",         "Create Product",          "Register new products"),
        ("inventory:edit",      "inventory", "edit",           "Edit Product",            "Edit existing products"),
        ("inventory:delete",    "inventory", "delete",         "Delete Product",          "Deactivate products"),
        ("inventory:audit",     "inventory", "audit",          "Perform Audit",           "Perform inventory audit"),
        # Financial
        ("financial:view",      "financial", "view",           "View Financial",          "View financial transactions"),
        ("financial:create",    "financial", "create",         "Create Transaction",      "Create financial transactions"),
        ("financial:edit",      "financial", "edit",           "Edit Transaction",        "Edit financial transactions"),
        ("financial:export",    "financial", "export",         "Export Financial",        "Export financial data"),
        # Fiscal
        ("fiscal:view",         "fiscal",    "view",           "View Fiscal",             "View invoices and fiscal documents"),
        ("fiscal:issue",        "fiscal",    "issue",          "Issue Invoice",           "Issue NF-e and NFC-e"),
        ("fiscal:cancel",       "fiscal",    "cancel",         "Cancel Invoice",          "Cancel issued invoices"),
        # Users
        ("users:view",          "users",     "view",           "View Users",              "View company users"),
        ("users:create",        "users",     "create",         "Create User",             "Create new users"),
        ("users:edit",          "users",     "edit",           "Edit User",               "Edit user information"),
        ("users:delete",        "users",     "delete",         "Delete User",             "Deactivate users"),
        ("users:manage_roles",  "users",     "manage_roles",   "Manage Roles",            "Create and assign roles"),
        # Reports
        ("reports:view",        "reports",   "view",           "View Reports",            "View basic reports"),
        ("reports:bi",          "reports",   "bi",             "Access BI",               "Access full BI dashboard"),
        ("reports:export",      "reports",   "export",         "Export Reports",          "Export report data"),
        # Customers
        ("customers:view",      "customers", "view",           "View Customers",          "View customer list"),
        ("customers:create",    "customers", "create",         "Create Customer",         "Register new customers"),
        ("customers:edit",      "customers", "edit",           "Edit Customer",           "Edit customer information"),
        # Orders
        ("orders:view",         "orders",    "view",           "View Orders",             "View open orders"),
        ("orders:create",       "orders",    "create",         "Create Order",            "Create new orders"),
        ("orders:edit",         "orders",    "edit",           "Edit Order",              "Edit existing orders"),
        ("orders:close",        "orders",    "close",          "Close Order",             "Close and finalize orders"),
        # Ecommerce
        ("ecommerce:view",      "ecommerce", "view",           "View Ecommerce",          "View online store"),
        ("ecommerce:manage",    "ecommerce", "manage",         "Manage Ecommerce",        "Manage online store products"),
        # WMS
        ("wms:view",            "wms",       "view",           "View Warehouse",          "View warehouse operations"),
        ("wms:manage",          "wms",       "manage",         "Manage Warehouse",        "Manage warehouse operations"),
        # Loyalty
        ("loyalty:view",        "loyalty",   "view",           "View Loyalty",            "View loyalty program"),
        ("loyalty:manage",      "loyalty",   "manage",         "Manage Loyalty",          "Manage loyalty program"),
        # Company
        ("company:view",        "company",   "view",           "View Company",            "View company information"),
        ("company:edit",        "company",   "edit",           "Edit Company",            "Edit company information"),
        ("company:billing",     "company",   "billing",        "Manage Billing",          "Manage subscription and billing"),
        # Permissions
        ("permission:view", "permission", "view", "View Permissions", "View system permissions"),
        ("permission:edit", "permission", "edit", "Edit Permissions", "Edit system permissions"),
        # Adicionar no seed.py
        ("stores:view",   "stores", "view",   "View Stores",   "View company stores"),
        ("stores:create", "stores", "create", "Create Store",  "Create new stores"),
        ("stores:edit",   "stores", "edit",   "Edit Store",    "Edit store information"),
        ("stores:delete", "stores", "delete", "Delete Store",  "Deactivate stores"),
    ]

    created = 0
    for code, module, action, name, description in permissions:
        if not Permission.query.filter_by(code=code).first():
            db.session.add(Permission(
                code=code,
                module=module,
                action=action,
                name=name,
                description=description,
            ))
            created += 1

    db.session.commit()

# System roles are predefined roles that come with the platform and are not tied to any specific company. They provide a baseline set of permissions for different types of users (e.g., system administrators, support staff, developers).
def seed_roles():
    system_roles = [
        (
            "system_admin",
            "Full access to the Alkion platform — Alkion team only",
        ),
        (
            "support",
            "Support team — limited access to help clients (permissions to be defined)",
        ),
        (
            "dev",
            "Development team — technical access for debugging (permissions to be defined)",
        ),
        (
            "owner",
            "Company owner — full access to the company system",
        ),
    ]

    created = 0
    for name, description in system_roles:
        if not Role.query.filter_by(name=name, company_id=None).first():
            db.session.add(Role(
                name        = name,
                description = description,
                is_system   = True,
                company_id  = None,
            ))
            created += 1

    db.session.commit()

# This function can be called to run all seed operations. It's designed to be idempotent, so it can be safely run multiple times without creating duplicates.
def run_seed():
    seed_permissions()
    seed_roles()