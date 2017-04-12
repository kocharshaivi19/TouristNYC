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


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#         <form method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''


# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))


# TODO
# figure out how to connect SQL to Flask
# write out ER diagram thing

if __name__ == "__main__":
    app.run()