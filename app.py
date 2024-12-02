from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__, static_folder='frontend', static_url_path='')
app.config.from_object(Config())


CORS(app)


def sortApps(totalApps, item):
    # translated from the JS version
    # sort total current applications by type - position, company, or location
    freq = {}
    for app in totalApps:
        elem = app[item]
        if item == "position" or item == "company" or item == "location":
            elem = elem.strip()
        if freq[elem]:
            freq[elem] += 1
        else:
            freq[elem] = 1
    freqKeyVals = list(freq.items())
    sortedFreqs = freqKeyVals.sorted(key=lambda x: x[1])
    return sortedFreqs


def countApps(totalApps, key, val):
    # count occurrences of specific vals within list of dicts
    count = 0
    for app in totalApps:
        if app[key] == val:
            count += 1
    return count


@app.route('/statistics', methods=['POST'])
@cross_origin()
def get_statistics():
    data = request.get_json()
    return jsonify({
        "Applications": len(data),
        "OA": countApps(data, 'online-assessment', True),
        "Interview": countApps(data, 'interview-round', True),
        "Company": sortApps(data, 'company'),
        "Position": sortApps(data, 'position'),
        "Location": sortApps(data, 'location')
    })


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run()
