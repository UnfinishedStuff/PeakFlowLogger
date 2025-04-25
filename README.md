<h1>PeakFlowLogger</h1>

This is a simple project for logging peak flow data to a website over time, and having that data graphed on an easy-to-use website.

If you're not familiar with peak flow, it is your maximum expiration rate.  You blow hard into a peak flow meter, and it tells you the maximum flow rate of air that you achieved.  This is a proxy measurement of lung health, and a decline in your readings can be an early indication of an exacerbation of your asthma.  You're meant to log this once or twice a day, and when first diagnosed you're often given a little paper booklet with a graph area to record this.  However, you run out of space after a few weeks, and having to keep loose bits of paper around to check what your peak flow used to be, compared to today's measurement, is a pain.  Hence, PeakFlowLogger.

PeakFlowLogger uses the [Flask Python web framework](https://flask.palletsprojects.com/en/stable/) and some basic HTML to present you with a website with a text input box.  When you measure your peak flow, you're supposed to blow into the meter three times, and record the highest.  You record the highest of these in the box, and press `Submit`.  This stores the value in an sqlite3 database, alongside a timestamp.  Every time you load the page, it reads the recorded data back, and uses [Bokeh](https://bokeh.org/) to render past data as a graph.  This allows you to keep tabs on the data over time, without having to faff around with bits of paper.

<h3>Current state</h3>
The basic functionality is all there.  I need to:

* Make the page a little more aesthetically pleasing, it is very basic at the moment.
* Figure out how to scale it properly for mobile devices
* I'm told that values less than 80% of your usual reading are the threshold for being concerned about an exacerbation.  It would be good to have some way to calculate this value from a certain past period (?), and to show this on the graph somehow.
* It would be good to be able to load the page after submitting data with a message, either stating that the value was successfully recieved, or giving a specific error.
* Maybe it would be helpful to have a way to delete the previous value, in case a mistake is made?


<h3>Installation</h3>

* Create a virtual environment in a terminal: `python3 -m venv ./peakFlowLogger` (replace `./PeakFlowLogger` with your desired location)
* Go into the virtual environment (`cd PeakFlowLogger`) and activate it: `source ./bin/activate`.  At any point, run `deactivate` to deactivate the environment.
* Install dependencies: `python3 -m pip install Flask bokeh`
* Copy `website.py` and `mkDB.py` to your virtual environment.  Create a directory there called `templates`, and copy `index.html` there.
* Create the database which will hold all of the data: `python3 mkDB.py`.  A file called `peakFlowData.db` should appear beside the Python scripts.
* Run Flask: `flask --app website run --host=0.0.0.0`
  * (`--host=0.0.0.0` makes the website available across your local network, but not over the internet)
* You should now be able to access the website at port 5000 at the IP address of the machine.  For example, if the IP address is `192.168.1.2`, use `192.168.1.2:5000` as the address in a web browser.
