import os
from app import create_app

env = os.getenv("FLASK_ENV", "development")
app = create_app(env)


@app.cli.command("seed")
def seed():
    with app.app_context():
        from app.utils.seed import run_seed
        run_seed()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=(env == "development"))