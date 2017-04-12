from flask import Flask, render_template, session, redirect, url_for
app = Flask(__name__)


@app.route("/")
def index():
	return redirect(url_for('explore'));


@app.route("/explore")
def explore():
    if 'username' in session:
    	return render_template("explore.html", username=session['username'])
    return render_template("explore.html", username=None)


@app.route("/trips")
def trips():
    if 'username' in session:
    	return render_template("trips.html", username=None)
    return render_template("trips.html", username=session['username'])


@app.route("/profile")
def profile():
    if 'username' in session:
    	return render_template("trips.html", username=None)
    return render_template("trips.html", username=session['username'])


if __name__ == "__main__":
    app.run()