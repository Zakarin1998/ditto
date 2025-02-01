from flask import Flask, render_template
from app.bot import bot_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bot_blueprint)
    
    @app.route("/")
    def index():
        return render_template("index.html")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
