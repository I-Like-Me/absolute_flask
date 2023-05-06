from app import create_app, db
from app.models import User, App, Version

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'App': App, 'Version': Version}