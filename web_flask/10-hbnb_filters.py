#!/usr/bin/python3
from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.route('/hbnb_filters')
def hbnb_filters():
    states = sorted(storage.all("State").values(), key=lambda s: s.name)
    amenities = sorted(storage.all("Amenity").values(), key=lambda a: a.name)
    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

