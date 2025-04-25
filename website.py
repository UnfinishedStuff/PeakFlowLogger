# The main website Python script

from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import datetime
import time

from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import components

app = Flask(__name__)

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
                print("Error, reading out of range")
                return redirect(url_for('index'))

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
       
            return redirect(url_for('index'))

        except ValueError:
            # The value of reading isn't an int or float, so ignore it
            print("Error, value is not a number")
            return redirect(url_for('index'))

    else:

        connection = sqlite3.connect("peakFlowData.db")
        cur = connection.cursor()
        cur.execute("SELECT * FROM peakFlow")

        data = cur.fetchall()

        x = []
        y = []

        for entry in data:
            x.append(entry[0])
            y.append(entry[1])

        plot = figure(title="Peak Flow",\
            x_axis_label="Date",\
            y_axis_label = "Peak Flow",
            x_axis_type="datetime")
        
        plot.line(x, y, legend_label="Peak Flow", line_width=2)

        script, div = components(plot)

        return render_template(
            "index.html", 
            script=script,
            div=div,
            resources=CDN.render()
        )
