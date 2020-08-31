import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
message = [
    {
        "sentBy": "John Doe",
        "date": "11/09/2001",
        "time": "11:00AM",
        "message": "message"
     }
]


@app.route('/', methods=['GET'])
def home():
    return """<h1>Distant Reading Archive</h1><p>A prototype API for distant reading of science fiction novels.</p>"""


# A route to return all of the available entries in our catalog.
@app.route('/api/messages', methods=['GET'])
def api_all():
    return jsonify(message)

def main():

    print(" Go to http://127.0.0.1:5000/api/messages to see the request result")
    app.run()



if __name__ == "__main__":
    main()