from flask import Flask, render_template, session, redirect, url_for
app = Flask(__name__)
app.config['DEBUG'] =True

@app.route("/")
def main():
	return render_template("main.html", username=None)

@app.route("/index")
def index():
	return render_template("index.html", username=None)

@app.route("/index-5")
def index_5():
	return render_template("index-5.html", username=None)

@app.route("/index-4")
def index_4():
	return render_template("index-4.html", username=None)

@app.route("/index-3")
def index_3():
	return render_template("index-3.html", username=None)

@app.route("/index-2")
def index_2():
	return render_template("index-2.html", username=None)

@app.route("/index-1")
def index_1():
	return render_template("index-1.html", username=None)


# @app.route("/explore",methods=['GET'])
# def explore():
#     if 'username' in session:
#     	return render_template("explore.html", username=session['username'])
#     return render_template("explore.html", username=None)
# 
# @app.route("/profile",methods=['GET'])
# def profile():
#     if 'username' in session:
#     	return render_template("profile.html", username=session['username'])
#     return render_template("profile.html", username=None)
# 
# 
# @app.route("/group",methods=['GET'])
# def group():
#     if 'username' in session:
#         return render_template("group.html", username=session['username'])
#     return render_template("group.html", username=None)
# 
# 
# @app.route("/trips",methods=['GET'])
# def trips():
#     if 'username' in session:
#         return render_template("trips.html", username=session['username'])
#     return render_template("trips.html", username=None)
# 
# 
# @app.route("/events",methods=['GET'])
# def events():
#     if 'username' in session:
#         return render_template("events.html", username=session['username'])
#     return render_template("events.html", username=None)




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
