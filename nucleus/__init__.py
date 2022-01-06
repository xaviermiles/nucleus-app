import os
from random import randint

from flask import Flask

from nucleus import landing_page, db, auth, profile


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "home-server.sqlite")
    )
    if test_config:
        app.config.update(test_config)
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    db.init_app(app)

    # simple test page
    @app.route("/hello")
    def hello():
        return "<p>Hello wingbats!</p>"

    # add other pages
    app.register_blueprint(landing_page.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)

    # function for sidebar functionality on all pages
    app.jinja_env.globals.update(get_greeting=get_greeting)

    return app


def get_greeting():
    greetings = [
        "hello",
        "guten tag", "hallo",
        "hola", "¿qué tal?",
        "bonjour", "salut",
        "zdravstvuyte", "privet",
        "nǐ hǎo",
        "salve", "ciao",
        "shalom",
        "god dag",
    ]
    i = randint(0, len(greetings) - 1)
    return greetings[i].title()


if __name__ == "__main__":
    app = create_app()
    app.run()
