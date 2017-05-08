from flask import Flask, render_template, session, redirect, url_for,request,flash, jsonify
import hashlib
import string
import random
import sqlite3
import requests
import json
import math
import os


app = Flask(__name__)
app.config['DEBUG'] =True
app.config['SECRET_KEY'] = hashlib.sha1("".join([hex(ord(x)).strip("0x") for x in string.printable])).hexdigest()

headers = {'Authorization': 'Bearer P2-HNVXnq9MOtC-ejRjAE7poK10HwsIbdWrui2p0e8iiAklkGoUoF23J_B38sG7jaQyoiqyFWOUDq1ztVinkiumCEKsE7P46MeK3gh91FeMMGY-UVQeGeU33K5X8WHYx'}
stars = {'0.0': "/static/photo/nostar.png", '0.5': "/static/photo/halfstar.png", '1.0': "/static/photo/onestar.png", '1.5': "/static/photo/oneandhalfstar.png", '2.0': "/static/photo/twostar.png", '2.5': "/static/photo/twoandhalfstar.png", '3.0': "/static/photo/threestar.png", '3.5': "/static/photo/threeandhalfstar.png", '4.0': "/static/photo/fourstar.png", '4.5': "/static/photo/fourandhalfstar.png", '5.0': "/static/photo/fivestar.png" }
tripsGroupped=[]
businesses=[]

class User():
    def __init__(self,email,password):
        self.username = email
        self.password = password

    def __repr__(self):
        return 'User %r' % self.username


#Routing/Rendering template
@app.route("/")
def index():
	return redirect(url_for('explore'))


@app.route("/explore",methods=['GET'])
def explore():
    if 'username' in session:
    	return render_template("explore.html", username=session['username'])
    return render_template("explore.html", username=None)

@app.route("/editprofile",methods=['GET','POST'])
def editprofile():
    if request.method == 'POST':
        # print 'History' in request.form
        history = request.form.get('History', 0)
        art = request.form.get('Art', 0)
        music = request.form.get('Music', 0)
        theater = request.form.get('Theater', 0)
        shopping = request.form.get('Shopping', 0)
        food = request.form.get('Food', 0)
        sports = request.form.get('Sports', 0)
        parks = request.form.get('Parks', 0)

        photo = request.form.get('Upload Photo', 0)

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        username = session['username']

        c.execute(""" UPDATE interests SET history = ?, art = ?, music = ?, theater = ?, shopping = ?, food = ?, sports = ?, parks = ? WHERE username = ?""", (history,art,music,theater,shopping,food,sports,parks,username))
        c.execute("""UPDATE user SET picture=? WHERE username=?""", (photo, username))
        conn.commit()
        conn.close()
    return redirect(url_for('explore'))

@app.route("/profile",methods=['GET'])
def profile():
    if 'username' in session:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM user WHERE username= ?""",(session['username'],))
        account = c.fetchone()

        c.execute("""SELECT * FROM interests WHERE username= ?""",(session['username'],))
        interests = c.fetchone()
    	return render_template("profile.html", account=account, interests=interests)
    else:
        flash('Please log in to view your profile!','error')
        return redirect(url_for('login'))


@app.route("/groups",methods=['GET'])
def groups():
    if 'username' in session:
        return render_template("group.html", username=session['username'])
    return render_template("group.html", username=None)


@app.route("/trips/<group>/1",methods=['GET'])
def trips(group):
    if 'username' in session:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        dest=[]
        if (group=="none"):
            c.execute("""SELECT * FROM trips WHERE username= ?""",(session['username'],))
        else:
            c.execute("""SELECT * FROM trips WHERE username= ?""", (group,))
        dest = c.fetchall()
        tripsGroupped[:]=[]
        for i in range (0, int(math.ceil(float(len(dest))/float(5)))):
            smallList=[]
            j=0
            while (j<5 and 5*i+j<len(dest)):
                smallList.insert(j, dest[5*i+j])
                j+=1
            if len(smallList)!=0:
                tripsGroupped.insert(i, smallList)
        if len(tripsGroupped)==0:
            return render_template("trips.html", username=session['username'], destinations = [], tripsList=[])

        return render_template("trips.html", username=session['username'], destinations=tripsGroupped[0], tripsList=tripsGroupped)
    flash('Please login to view your trip information!', 'error')
    return redirect(url_for('login'))

@app.route("/trips/<groups>/<page>",methods=['GET'])
def pageNumber(groups, page):
    if 'username' in session:
        if len(tripsGroupped)!=0:
            return render_template("trips.html", username=session['username'], destinations=tripsGroupped[int(page)-1],tripsList=tripsGroupped)
        return redirect(url_for('trips', group=groups))
    flash('Please log in to view your trip information!', 'error')
    return redirect(url_for('login'))

@app.route("/itinerary",methods=['GET'])
def itinerary():
    if 'username' in session:
        return render_template("itinerary.html", username=session['username'])
    flash('Please log in to view suggested events!', 'error')
    return redirect(url_for('login'))


@app.route("/events/<group>/1",methods=['GET'])
def events(group):
    if 'username' in session:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        interests=[1, 1, 1, 1, 1, 1, 1, 1, 1]
        if (group=='none'):
            c.execute("""SELECT * FROM interests WHERE username= ?""",(session['username'],))
            interests = c.fetchone()
        else:
            c.execute("""SELECT members FROM groups WHERE groupname= ?""", (group,))
            groupmembers=c.fetchone()[0].split(",")[1:-1]
            for i in range(len(groupmembers)):
                c.execute("""SELECT username FROM user WHERE user=?""", (groupmembers[i],))
                username=c.fetchone()[0]
                c.execute("""SELECT * FROM interests WHERE username= ?""", (username,))
                personalInterests=c.fetchone()
                for j in range(1, len(personalInterests)):
                    interests[j] = interests[j] and personalInterests[j]
        categories = ""
        if interests[1] or interests[2] or interests[3] or interests[4] or interests[5] or interests[6] or interests[7] or interests[8]:
            categories = "&categories="
        if interests[1]:
            categories += "historicaltours,landmarks,culturalcenter,festivals,"
        if interests[2]:
            categories += "galleries,artmuseums,arttours,publicart,"
        if interests[3]:
            categories += "jazzandblues,musicvenues,opera,"
        if interests[4]:
            categories += "theater,"
        if interests[5]:
            categories += "shoppingcenters,publicmarkets,fashion,fleamarkets,personal_shopping,"
        if interests[6]:
            categories += "food,"
        if interests[7]:
            categories += "active,"
        if interests[8]:
            categories += "boating,lakes,parks,hiking,"

        r = requests.get("https://api.yelp.com/v3/businesses/search?location=New%20York%20City" + categories[:-1], headers=headers);
        r = json.loads(r.text)

        for business in r["businesses"]:
            business['underScoredName'] = business['name'].replace(" ", "_")
            business['ratingPicture'] = stars[str(business['rating'])]
            business['underScoredAddress'] = ("_").join(business["location"]["display_address"])
            business['underScoredAddress']=business['underScoredAddress'].replace(" ", "-")

        businesses[:] = []
        for i in range(0, int(math.ceil(float(len(r["businesses"])) / 5))):
            smallList = []
            j = 0
            while j < 5 and 5 * i + j < len(r["businesses"]):
                smallList.insert(j, r["businesses"][5 * i + j])
                j += 1
            if len(smallList)!=0:
                businesses.insert(i, smallList)

        if len(businesses)==0:
            return render_template("events.html", username=session['username'], eventstoshow = [], events=[])
        return render_template("events.html", username=session['username'], eventstoshow = businesses[0], events=businesses)
    flash('Please log in to view suggested events!','error')
    return redirect(url_for('login'))

@app.route("/events/<groups>/<page>",methods=['GET'])
def eventsPageNumber(groups, page):
    if 'username' in session:
        if len(businesses)!=0:
            return render_template("events.html", username=session['username'], eventstoshow=businesses[int(page)-1], events=businesses)
        return redirect(url_for('events', group=groups))
    flash('Please log in to view suggested events!', 'error')
    return redirect(url_for('login'))

@app.route("/addEvent/<group>",methods=['POST'])
def addEvent(group):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    if (group!="none"):
        username = group
    else:
        username = session['username']
    c.execute(""" INSERT INTO trips VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""", (username, request.form["id"], 0, request.form["lat"], request.form["long"], request.form["image"], request.form["name"], request.form["url"], request.form["rating"], request.form["address"], request.form["phone"], request.form["ratingphoto"]))
    conn.commit()
    conn.close()
    return 'successful'

@app.route('/removeTrip',methods=['POST'])
def removeTrip():
    # print request.form
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""DELETE FROM trips WHERE url=?""", (request.form["url"],))
    conn.commit()
    conn.close()
    return "successful"


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

            user=username.split("@")[0]
            picture="http://websamplenow.com/30/userprofile/images/avatar.jpg"
            
            c.execute(""" INSERT INTO user VALUES(NULL,?,?,?,?,?,?,?,?,?)""",(username,user,password,pin,tel,birth,country,gender,picture))
            c.execute(""" INSERT INTO interests VALUES(?,?,?,?,?,?,?,?,?)""",(username,0,0,0,0,0,0,0,0))
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
        print account

        if account:
            #print "You are loggined in!"
            session['username'] = username
            # session['username'] = hashlib.sha256(username+str(random.randint(0,99999))).hexdigest()
            return redirect(url_for('explore'))
        else:
            flash('Wrong Username or Password. Try again!','error')
            return redirect(url_for('login'))

    return render_template("login.html",username=None)



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('explore'))

@app.route("/search",methods=['POST'])
def search():
    searchuser = request.form.keys()[0]
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(" SELECT user, picture FROM user WHERE user LIKE ?", (searchuser+'%',))
    found = c.fetchall()
    foundusers=[{"username": found[i][0], "picture":found[i][1]} for i in range(0, len(found))]
    conn.commit()
    conn.close()
    return jsonify(foundusers)

@app.route("/myGroups",methods=['GET'])
def myGroups():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("""SELECT user FROM user WHERE username=?""", (session['username'],))
    username = c.fetchone()[0]
    c.execute("""SELECT * FROM groups WHERE members LIKE ?""", ("%,"+username+",%",))
    found = c.fetchall()
    groupslist=[]
    for i in range(len(found)):
        newlist=found[i][1].split(",")[1:-1]
        listofusers=[]
        for j in range (len(newlist)):
            c.execute("""SELECT picture FROM user WHERE user=?""", (newlist[j],))
            image = c.fetchone()
            listofusers.append([newlist[j], image])
        groupslist.append(listofusers)

    foundgroups=[{"group": found[i][0], "members":groupslist[i]} for i in range(0, len(found))]
    conn.commit()
    conn.close()
    return jsonify(foundgroups)

@app.route("/createGroup",methods=['POST'])
def createGroup():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    print request.form.keys()[0]
    output=request.form.keys()[0].split(";")
    groupname=output[0]
    users=output[1]
    c.execute(""" INSERT INTO groups VALUES(?,?)""", (groupname, users,))
    conn.commit()
    conn.close()
    return "Success"

# TODO
# figure out how to connect SQL to Flask
# write out ER diagram thing

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5100))
    app.run(host='localhost', port=port)
