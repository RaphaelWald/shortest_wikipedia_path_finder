from flask import Flask
import server.path_finder as path_finder

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Wikipedia Shortest Path Finder</h1>"


if __name__ == "__main__":
    app.run(debug=True)