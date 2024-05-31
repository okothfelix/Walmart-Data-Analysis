from flask import Flask
from flask_cors import CORS
from analytics.routes import analytics_bp
from pos.routes import pos_bp

app = Flask(__name__)
CORS(app, resources={r'*': {'origins': 'https://537f-197-232-122-151.ngrok-free.app'}})

app.register_blueprint(analytics_bp, url_prefix='/')
app.register_blueprint(pos_bp, url_prefix='/pos')

if __name__ == '__main__':
    app.run(debug=True)
