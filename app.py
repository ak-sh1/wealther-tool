"""
app.py
Web version of the weather tool, built with Flask.
Reuses weather.py exactly as main.py and gui.py do — the logic layer
still doesn't know or care what kind of interface is calling it.
"""

from flask import Flask, render_template, request
from weather import lookup

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    city = request.args.get("city", "").strip()
    report = None
    error = None

    if city:
        try:
            report = lookup(city)
        except ValueError as e:
            error = str(e)
        except Exception:
            error = "Something went wrong reaching the weather service."

    return render_template("index.html", city=city, report=report, error=error)


if __name__ == "__main__":
    app.run(debug=True)