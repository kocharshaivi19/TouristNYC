from flask import Flask, render_template, session, redirect, url_for,request,flash
import hashlib
import string
import random
import sqlite3
import requests


app = Flask(__name__)
app.config['DEBUG'] =True
app.config['SECRET_KEY'] = hashlib.sha1("".join([hex(ord(x)).strip("0x") for x in string.printable])).hexdigest()

headers = {'Authorization': 'Bearer P2-HNVXnq9MOtC-ejRjAE7poK10HwsIbdWrui2p0e8iiAklkGoUoF23J_B38sG7jaQyoiqyFWOUDq1ztVinkiumCEKsE7P46MeK3gh91FeMMGY-UVQeGeU33K5X8WHYx'}


class User():
    def __init__(self,email,password):
        self.username = email
        self.password = password

    def __repr__(self):
        return 'User %r' % self.username


#Routing/Rendering template
@app.route("/")
def index():
	return redirect(url_for('explore'));


@app.route("/explore",methods=['GET'])
def explore():
    if 'username' in session:
    	return render_template("explore.html", username=session['username'])
    return render_template("explore.html", username=None)

@app.route("/profile",methods=['GET'])
def profile():
    if 'username' in session:
    	return render_template("profile.html", username=session['username'])
    else:
        flash('Please log in to view your profile!','error')
        return redirect(url_for('login'))


@app.route("/groups",methods=['GET'])
def groups():
    if 'username' in session:
        return render_template("group.html", username=session['username'])
    return render_template("group.html", username=None)


@app.route("/trips",methods=['GET'])
def trips():
    if 'username' in session:
        return render_template("trips.html", username=session['username'])
    return render_template("trips.html", username=None)

@app.route("/itinerary",methods=['GET'])
def itinerary():
    if 'username' in session:
        return render_template("itinerary.html", username=session['username'])
    return render_template("itinerary.html", username=None)


@app.route("/events",methods=['GET'])
def events():
    if 'username' in session:

        r = requests.get("https://api.yelp.com/v3/businesses/search?location=New%20York%20City", headers=headers);
        print r.text

        return render_template("events.html", username=session['username'])
    return render_template("events.html", username=None)



@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['email']
        password = hashlib.sha256(request.form['password']).hexdigest()
        confirm = hashlib.sha256(request.form['confirm']).hexdigest()
        pin = request.form['pin']                
        tel = request.form['telephone']
        birth= request.form['birthday']
        country = request.form['cnt']
        gender= request.form['sex']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(""" SELECT * FROM user WHERE username = ? """,(username,))
        data = c.fetchone()

        if data:
            flash("Account already exists!",'error')
            return redirect(url_for('signup'))


        if username and password and confirm and tel and birth and country and gender and pin:
            if confirm != password:
                flash('Password do not match!','error')
                return redirect(url_for('signup'))

            
            c.execute(""" INSERT INTO user VALUES(NULL,?,?,?,?,?,?,?)""",(username,password,pin,tel,birth,country,gender))
            conn.commit()
            conn.close()
            flash("You have successfully registered :)")
            return redirect(url_for('login'))
        else:
            flash("All fields are required to register!",'unfinished')
            return redirect(url_for('signup'))
        
        
    return render_template('signup.html',username=None)           




@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = hashlib.sha256(request.form['password']).hexdigest()
        pin = request.form['pin']
      
        #print session['username']
    
        print "Username: %s Password: %s Pin: %s" % (username,password,pin) 
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM user WHERE username= ? and password= ?""",(username,password))
        account = c.fetchone()

        if account:
            #print "You are loggined in!"
            session['username'] = hashlib.sha256(username+str(random.randint(0,99999))).hexdigest()
            return redirect(url_for('explore'))
        else:
            flash('Wrong Username or Password. Try again!','error')
            return redirect(url_for('login'))

    return render_template("login.html",username=None)



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('explore'))



# TODO
# figure out how to connect SQL to Flask
# write out ER diagram thing

if __name__ == "__main__":
    app.run()
