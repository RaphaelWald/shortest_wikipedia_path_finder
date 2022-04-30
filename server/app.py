from flask import Flask, jsonify, redirect, url_for, request, json
import path_finder

app = Flask(__name__)


@app.route('/members')
def member():
    return {"members": ["Member1", "Member2", "Member3"]}


@app.route('/post', methods=['POST'])
def testPost():
    start = request.json["start"]
    destination = request.json["destination"]

    paths = path_finder.bidirectional_BFS(start, destination)

    return str(paths)


if __name__ == "__main__":
    app.run(debug=True)