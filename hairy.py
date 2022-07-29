import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return "\"umm, actually this website is kinda shit\" - 🤓"

if __name__ == "__main__":
    app.run(debug=True)