from flask import Flask, request, jsonify
from geocodio import GeocodioClient
from pyzomato import Pyzomato


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def home():
    return '<h1>Welcome to Foodie Web Services</h1><p>Our web service takes a HTTP request with an address parameter and respond with a list popular restaurants nearby.</p><br /><hr /><h1>How to use our service:</h1><p>In the address bar, enterhttp://127.0.0.1:5000//restaurants/?address=&lt;ADDRESS&gt;</p><p>Make sure to have a valid address containing:</p><ol>  <li>Street </li>  <li>City/Town/Village </li>  <li>Zip Code</li></ol>'


@app.route("/restaurants")
def restaurants():
    address = request.args.get('address')
    if not address:
        return "Bad Request!<br>Address parameter is empty or invalid."
    client = GeocodioClient('e69dd65d59f64d56bb99e5fea55f5b1d999a696')
    zomato = Pyzomato('188eda180987998d1dd37a7b93fee08a')

    location = client.geocode(address) # .coords to get lat and lng right away
    lat = location['results'][0]['location']['lat']     # parsing json
    lng = location['results'][0]['location']['lng']

    zomatoData = zomato.getByGeocode(lat, lng)

    output = {
        'restaurants': []
    }
    for r in zomatoData['nearby_restaurants']:
        output['restaurants'].append(dict({'name': r['restaurant']['name'],
                                           'address': r['restaurant']['location']['address'],
                                           'cuisines:': r['restaurant']['cuisines'],
                                           'rating': r['restaurant']['user_rating']['aggregate_rating']
                                           }))
    print(output)
    return jsonify(output)


if __name__ == '__main__':
    app.run()
