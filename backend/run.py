import os
from app import create_app

env = os.getenv("FLASK_ENV", "development")
app = create_app(env)


# Flask CLI command to seed the database
@app.cli.command("seed")
def seed():
    with app.app_context():
        from app.utils.seed import run_seed
        run_seed()

# Invoke the Flask application
if __name__ == "__main__":

    host  = os.getenv("FLASK_HOST", "0.0.0.0")
    port  = int(os.getenv("FLASK_PORT", "5000"))

    debug = (env == "development")

    app.run(host=host, port=port, debug=debug)