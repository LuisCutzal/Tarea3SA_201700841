from flask import Flask
from routes.ci_routes import ci_bp
from routes.relationship_routes import relationship_bp

app = Flask(__name__)
app.register_blueprint(ci_bp)
app.register_blueprint(relationship_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
