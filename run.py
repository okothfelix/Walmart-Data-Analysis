from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.secret_key = '70b76438bbccfd3ec8ab0ec170d4e179'
    CORS(app, resources={r'*': {'origins': 'https://beemultiscent.com'}})

    # bms routes
    from analytics.routes import analytics_bp
    from pos.routes import pos_bp

    app.register_blueprint(analytics_bp, url_prefix='/')
    app.register_blueprint(pos_bp, url_prefix='/pos')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)