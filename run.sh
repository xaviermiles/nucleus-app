export FLASK_APP=nucleus/__init__.py
export FLASK_ENV=development
source venv/bin/activate
# flask init-db  # uncomment to reset database
flask run
