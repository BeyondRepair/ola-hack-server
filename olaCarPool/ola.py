from flask import Flask, request, make_response
from flask.ext.pymongo import PyMongo
from config import DefaultConfig


app = Flask(__name__)
config = DefaultConfig()
app.config.from_object(config)
mongo = PyMongo(app)


@app.route('/book', methods=['POST'])
def book_ride():
    mongo.db.rides.save(request.get_json()['ride'])
    return make_response()

if __name__ == "__main__":
    app.run()