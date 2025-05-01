import os
from applications import create_app
from applications.database import db
from applications.models import initialize_admin

app = create_app()

with app.app_context():
    db.create_all()
    initialize_admin()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
