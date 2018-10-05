from flask import Flask, jsonify, request, redirect, url_for, render_template
from urllib.parse import urlparse, urljoin
import socket
import validators

from tinydb import TinyDB, Query
import datetime as dt


app = Flask(__name__)
DB_PATH = "db.json"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def set_dt_now():
    return dt.datetime.utcnow().strftime(DATETIME_FORMAT)

# Initiliaze database
with TinyDB(DB_PATH) as db:
    db.purge()
    db.insert_multiple([
        dict(
            original_url="https://www.freecodecamp.com",
            created_at=set_dt_now(),
            last_visited=None,
            visits=0
        ),
        dict(
            original_url="https://www.w3schools.com",
            created_at=set_dt_now(),
            last_visited=None,
            visits=0
        )
    ])

@app.route("/")
def index():
    """Index site.
    Show a list with the short URLs and allows to copy each one to the
    clipboard.
    """
    host_url = request.host_url

    # Build URLs array to pass into the template
    with TinyDB(DB_PATH) as db:
        urls_array = [
            (
                url.doc_id,
                urljoin(
                    host_url,
                    url_for("short_url", url_id=url.doc_id)
                ),
                url["created_at"],
                url["last_visited"],
                url["visits"]
            ) for url in iter(db)
        ]
    return render_template("index.html", urls=urls_array), 200

@app.route("/shorten/new", methods=["POST"])
def shorten():
    """Shorten a URL."""
    if request.method == "POST":
        original_url = request.json["url"]
        urlp = urlparse(original_url)
        valid_site = True

        # DNS lookup
        try:
            socket.gethostbyname(urlp.netloc)
        except socket.gaierror:
            valid_site = False

        if validators.url(original_url) and valid_site:
            # Insert URL in database
            with TinyDB(DB_PATH) as db:
                url_id = db.insert(dict(
                    original_url=original_url,
                    created_at=set_dt_now(),
                    last_visited=None,
                    visits=0
                ))

            # Return JSON response
            return jsonify(
                dict(
                    original_url=original_url,
                    short_url=url_id
                )
            ), 200
        
        # If the URL is not valid or DNS lookup failed
        else:
            return jsonify(dict(error="invalid URL")), 400
    else:
        return "Try sending a POST request instead", 400

@app.route("/shorten/<int:url_id>")
def short_url(url_id):
    """Visit the original URL associated with a shortened one."""

    # Get database document with id equal to `url_id`
    with TinyDB(DB_PATH) as db:
        url = db.get(doc_id=url_id)

        # Update the URL document
        if url:
            visits = url["visits"]
            db.update({
                "last_visited": set_dt_now(),
                "visits": visits + 1
                }, doc_ids=[url_id]
            )

    if url:
        return redirect(url["original_url"], code=302)
    else:
        return redirect('/', code=302)

if __name__ == "__main__":
    app.run()
