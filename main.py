from Orchestrator.app import app
from Orchestrator.database import db

db.create_all()
app.run(debug=True)