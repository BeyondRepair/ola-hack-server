from flask import Flask, request, make_response
from flask.ext.pymongo import PyMongo
from config import DefaultConfig
import requests

app = Flask(__name__)
config = DefaultConfig()
app.config.from_object(config)
mongo = PyMongo(app)


@app.route('/book', methods=['POST'])
def book_ride():
    try:
        payload = {'pickup_lat': request.get_json()['ride']['pickup_lat'],
                   'pickup_lng': request.get_json()['ride']['pickup_lon'],
                   'pickup_mode': 'NOW',
                   'category': request.get_json()['ride']['category']}
    except KeyError:
        serverResponse = make_response()
        serverResponse.status_code = 404
        return serverResponse
    response = requests.get('http://sandbox-t.olacabs.com/v1/bookings/create?',
                            payload,
                            headers={'Authorization':
                                     'Bearer %s' % request.get_json()[
                                         'ride']['access_token'],
                                     'X-APP-TOKEN':
                                     app.config.get('X_APP_TOKEN')})
    if response.status_code == 200:
        mongo.db.rides.save(request.get_json()['ride'])
    return make_response()


if __name__ == "__main__":
    app.run()