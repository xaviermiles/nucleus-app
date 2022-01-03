import os

from flask import Flask, url_for

from nucleus import landing_page


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "home-server.sqlite")
    )
    
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
        
    # simple test page
    @app.route("/hello")
    def hello():
        return "<p>Hello wingbats!</p>"
        
    # add other pages
    app.register_blueprint(landing_page.bp)
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
