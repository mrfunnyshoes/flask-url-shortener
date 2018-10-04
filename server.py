from flask import Flask, jsonify, request, redirect, url_for, render_template
from urllib.parse import urlparse
import socket
import validators

app = Flask(__name__)
urls = ["https://www.freecodecamp.com"]


@app.route("/")
def index():
    return render_template("index.html"), 200


@app.route("/shorten/new", methods=["POST"])
def shorten():
    if request.method == "POST":
        original_url = request.json["url"]
        urlp = urlparse(original_url)
        valid_site = True
        try:
            socket.gethostbyname(urlp.netloc)
        except socket.gaierror:
            valid_site = False
        if validators.url(original_url) and valid_site:
            urls.append(original_url)
            return jsonify(dict(
                original_url=original_url,
                short_url=len(urls)
            )), 200
        else:
            return jsonify(dict(error="invalid URL")), 400
    else:
        return "Try POSTing instead", 400


@app.route("/shorten/<int:id>")
def short_url(id):
    try:
        return redirect(urls[id - 1], code=302)
    except:
        return "<h1>NOT FOUND!</h1>", 404


if __name__ == "__main__":
    app.run(debug=True, port=9876)
