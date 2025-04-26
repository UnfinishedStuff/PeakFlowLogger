from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import datetime
import time

from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.models import BoxAnnotation

app = Flask(__name__)


def generateGraph():
    connection = sqlite3.connect("peakFlowData.db")
    cur = connection.cursor()
    cur.execute("SELECT * FROM peakFlow")

    data = cur.fetchall()

    x = []
    y = []

    for entry in data:
        x.append(entry[0])
        y.append(int(entry[1]))

    try:
        avgPeakFlow = sum(y) / len(y)
    except ZeroDivisionError:
        avgPeakFlow = 0
    eightyPercentBox = BoxAnnotation(top=(avgPeakFlow * .8), fill_alpha=0.2, fill_color="#D55E00")

    plot = figure(title="Peak Flow",\
        x_axis_label="Date",\
        y_axis_label = "Peak Flow",
        x_axis_type="datetime")
        
    plot.line(x, y, legend_label="Peak Flow", line_width=2)
    plot.add_layout(eightyPercentBox)

    plots = gridplot([[plot]], sizing_mode="stretch_height")

    script, div = components(plots)

    return script, div


@app.route("/", methods=['GET'])
def index():

    if request.args.get("reading") != None:

        result = request.args.get("reading")

        try:
            # Check the value is a number
            result = int(result)

            # Check the value is in a valid range
            if (result > 900) or (result < 60):
                # The reading isn't valid
                print("Error, reading of out of range (60-900).")

                script, div = generateGraph()

                return render_template(
                "index.html",
                message = "<p style=\"color:rgb(255,0,0)\">Error, reading out of range (60-900).</p>",
                script=script,
                div=div,
                resources=CDN.render()
                )

            # Get the timestamp for the reading
            timestamp = datetime.datetime.now().timestamp() * 1000
        
            # Database called peakFlowData.db
            # Table called peakFlow
            # Fields called timestamp and reading
            connection = sqlite3.connect("peakFlowData.db")
            cur = connection.cursor()
            cur.execute("INSERT INTO peakFlow (timestamp, reading) VALUES (?, ?)", (timestamp, result))

            connection.commit()
            connection.close()

            script, div = generateGraph()

            return render_template(
            "index.html",
            message="Reading of " + str(result) + " successfully submitted!", 
            script=script,
            div=div,
            resources=CDN.render()
            )

        except ValueError:
            # The value of reading isn't an int or float, so ignore it
            print("Error, value is not a number")

            script, div = generateGraph()

            return render_template(
            "index.html",
            message = "<p style=\"color:rgb(255,0,0)\">Error, value is not a valid integer (60-900).</p>",
            #message="Error, value is not a valid number", 
            script=script,
            div=div,
            resources=CDN.render()
        )

    else:

        script, div = generateGraph()

        return render_template(
            "index.html",
            message="", 
            script=script,
            div=div,
            resources=CDN.render()
            )
