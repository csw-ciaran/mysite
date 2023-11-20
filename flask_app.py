from flask import Flask, render_template, request  # from module import Class.


import os

import hfpy_utils
import swim_utils


app = Flask(__name__)


@app.get("/")
def hello():
    return "Hello from my first web app - cool, isn't it?"  # ANY string.


@app.route("/events", methods=["POST"])
def display_chart():
    selected_file = request.form["file"]
    (
        name,
        age,
        distance,
        stroke,
        the_times,
        converts,
        the_average,
    ) = swim_utils.get_swimmers_data(selected_file)

    the_title = f"{name} (Under {age}) {distance} {stroke}"
    from_max = max(converts) + 50
    the_converts = [hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts]

    the_data = zip(the_converts, the_times)

    return render_template(
        "chart.html",
        title=the_title,
        average=the_average,
        data=the_data,
    )


@app.get("/getswimmers")
def get_swimmers_names():
    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")
    names = set()
    for swimmer in files:
        names.add(swim_utils.get_swimmers_data(swimmer)[0])

    return render_template(
        "select.html",
        title="Select a Swimmer to chart",
        data=sorted(names),
    )


@app.route("/getswimmers", methods=["POST"])
def get_swimmers():
    selected_name = request.form["swimmer"]
    files = [f for f in os.listdir(swim_utils.FOLDER) if f.startswith(selected_name)]
    return render_template(
        "events.html",
        title="Select a Event to chart",
        files=files,
    )


if __name__ == "__main__":
    # Starts a local (test) webserver, and waits... forever.
    app.run(debug=True)
