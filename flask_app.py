from flask import Flask, render_template, request, session
from sqlite3 import *

app = Flask(__name__)
app.secret_key = "hello"


@app.route('/', methods = ["GET", "POST"])
def index():
    db = connect('DataBase.db')
    c = db.cursor()
    if request.method == "POST":
        session.pop("user", None)

    # getting online statue
    if 'user' not in session:
        login = "Please Login"
    else:
        login = session['user']

    # getting all the songs
    c.execute('''SELECT * FROM Songs;''')
    songs = c.fetchall()
    db.close()
    
    return render_template('index.html', songs = songs, login = login)

@app.route('/search', methods = ["POST"])
def search():

    db = connect('DataBase.db')
    c = db.cursor()

    search = request.form.get('search')

    #finding songs related to search
    c.execute('''SELECT * from Songs\
            WHERE name_of_song like ?''', ('%'+search+'%',))
    results = c.fetchall()

    # getting online statue
    if "user" in session:
        login = session["user"]
    else:
        login = "Please Login"
    
    return render_template('search.html', songs = results, login = login)

@app.route('/search/<string:song>')
def search_using_tab(song):
    search = song

    db = connect('DataBase.db')
    c = db.cursor()

    if "user" in session:
        login = session["user"]
    else:
        login = "Please Login"

    # getting the songs
    c.execute('''SELECT * FROM Songs\
            WHERE name_of_song like ?''', ('%' + search + '%',))
    results = c.fetchall()
    
    return render_template('search.html', songs = results, login = login)

@app.route('/login_public', methods = ["GET", "POST"])
def profilelogin():
    wronginfo = None
    if request.method == "GET":
        return render_template('loginconsumer.html')
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        db = connect('DataBase.db')
        c = db.cursor()
        c.execute('''SELECT * FROM CONSUMER\
                WHERE email = ?\
                AND password = ?''',(email, password))
        info = c.fetchone()
        if info == None:
            wronginfo = True
            return render_template('loginconsumer.html', wronginfo = wronginfo)

        c.execute('''SELECT * FROM Consumer\
            WHERE email = ?\
            AND password = ?''', (email, password))

        online = c.fetchone()

        session['user'] = online
       
        db.commit()
        db.close()
        
        return render_template('profile.html', login = online)


@app.route('/login_artist', methods = ["GET", "POST"])
def artistlogin():
    if request.method == "GET":
        return render_template('loginartist.html')
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        db = connect('DataBase.db')
        c = db.cursor()
        c.execute('''SELECT * FROM ARTIST\
                WHERE email = ?\
                AND password = ?''',(email, password))
        info = c.fetchone()
        if info == None:
            wronginfo = True
            return render_template('loginartist.html', wronginfo = wronginfo)

        db = connect('DataBase.db')
        c = db.cursor()

        c.execute('''SELECT * FROM Artist\
                WHERE email = ?\
                AND password = ?''', (email, password))
        
        online = c.fetchone()
        session['user'] = online

        
        db.commit()
        db.close()
        
        return render_template('profile.html', login = online)



@app.route('/reset_password', methods = ["GET", "POST"])
def resetpassword():
    if request.method == "GET":
        return render_template("resetpassword.html")
    else:
        
        email = request.form.get("email")
        checker = request.form.get("password_checker")

        db = connect('DataBase.db')
        c = db.cursor()

        if checker == "Login":

            c.execute('''SELECT email FROM Consumer\
                    WHERE email = ?''', (email,))
        
            check = c.fetchone()
            if check == None:
                wronginfo = True
                return render_template("resetpassword.html",wronginfo = wronginfo)
            if check [0]== email:
                return render_template("passwordresetpage.html", email = email)
            else:
                wronginfo = True
                return render_template("resetpassword.html", wronginfo = wronginfo)


        
        if checker != "Login":
            Password = request.form.get("Password")
            Confirm = request.form.get("confirm")
            if Password != Confirm or Password == '' or Confirm == '':
                return render_template("passwordresetpage.html", incorrect = True, email = checker)
            else:
                newPass = Password
                c.execute('''UPDATE Consumer SET password = ?\
                            WHERE email = ?''',(newPass, checker))

                c.execute('''SELECT * FROM Consumer\
                            WHERE email = ?''', (checker,))

                online = c.fetchone()

                session['user'] = online

                db.commit()
                db.close()

                return render_template('profile.html', login = online)

                


@app.route('/profile')
def profile():
    artist = False
    db = connect('DataBase.db')
    c = db.cursor()

    if "user" in session:
        online = session["user"]
    else:
        online = "Please Login"
       
    if online == "Please Login":
        return render_template('loginconsumer.html',login = 'Please login')
    return render_template('profile.html', login = online, artist = artist)

@app.route('/profile/general_settings', methods = ["GET", "POST"])
def general():
    artist = False
    db = connect('DataBase.db')
    c = db.cursor()

    if "user" in session:
        online = session["user"]
    else:
        online = "Please Login"
        
    if online == None:
        return render_template("create_account.html", login = online)

    name = online[3]
    nickname = online[4]
    email = online[1]
    balance = online[6]

    return render_template('general.html',artist = artist, login = online, name = name, nickname = nickname, email = email, balance = balance)

    

@app.route('/profile/sign_up', methods = ["GET", "POST"])
def create_account():
    checker = False
    db = connect('DataBase.db')
    c = db.cursor()

    if "user" in session:
        login = session["user"]
    else:
        login = "Please Login"


    if request.method == "GET":
        return render_template("create_account.html", login = login)

    if request.method == "POST":
        #check if we fill in everything
        password = request.form.get("password")
        check = request.form.get("confirm")
        username = request.form.get("username")
        email = request.form.get("email")
        name = request.form.get("name")
        particulars = (email, password, name,check, username )
        for info in particulars:
            if info == "":
                checker = True
                return render_template("create_account.html",login = login, checker_information = checker)
        
        #check password
        if password != check:
            checker = True
            return render_template("create_account.html",login = login, checker_password = checker)

        #check if Username is taken
        c.execute('''SELECT username FROM Consumer\
                    WHERE username = ?''',(username,))
        user = c.fetchone()
        if user != None:
            if user[0] == username:
                checker = True
                return render_template("create_account.html", login = login, checker_username = checker)


        #check if email is taken
        c.execute('''SELECT email FROM Consumer\
                    WHERE email = ?''', (email,))
        user = c.fetchone()
        if user != None:
            if user[0] == email:
                checker = True
                return render_template("create_account.html", login = login, check_email_validity = checker)

        #check if email is valid
        if '@' not in email:
            checker = True
            return render_template("create_account.html", login = login, checker_email = checker)


        #all the checks are clear

        create_account = True
        new_account = (email, password, name, username, 'False', 0)
        

        c.execute('''INSERT INTO Consumer(\
        email, password, name, username, login, balance)
        VALUES(?,?,?,?,?,?)''',new_account)

        c.execute('''SELECT * FROM Consumer\
                    WHERE email = ?''', (new_account[0],))

        login = c.fetchone()

        db.commit()
        db.close()

        session['user'] = login
        
        return render_template("profile.html", login = login, create_account = create_account)


@app.route('/profile/update', methods = ["GET", "POST"])
def updateprofile():
    checker = None
    artist = False
    if request.method == "POST":

        db = connect('DataBase.db')
        c = db.cursor()


        online = session['user']
    
        updated = "You have successfully updated your profile"
        name = request.form.get('name')
        password = request.form.get("password")
        check = request.form.get("confirm")
        email = request.form.get('email')
        username = request.form.get('username')
        particulars = (email, password, name, username)
        column = [email, password, name, username]

        if password != check:
            checker = True
            return render_template("profile.html", login = online, create_password = checker)


        c.execute('''SELECT username FROM Consumer\
                    WHERE username = ?''',(username,))
        
        user = c.fetchone()
        if user != None:
            if user[0] == username:
                checker = True
                return render_template("profile.html", login = online, checker_username = checker)


        num = 0
        for info in particulars:
            
            if info != '':
                if artist == False:
                    c.execute('''SELECT Consumer SET login = "True"\
                        WHERE email = ?''', (online[1],))
                    if email == column[num]:
                        c.execute('''UPDATE Consumer SET email = ?\
                                WHERE login = "True" ''',(info,))
        
                    if password == column[num]:
                        c.execute('''UPDATE Consumer SET password = ?\
                                WHERE login = "True" ''',(info,))
            
                    if name == column[num]:
                            c.execute('''UPDATE Consumer SET name = ?\
                                WHERE login = "True" ''',(info,))
                    if username == column[num]:
                            c.execute('''UPDATE Consumer SET username = ?\
                                WHERE login = "True" ''',(info,))
                    c.execute('''SELECT Consumer Set login = False\
                                WHERE Consumer_ID = ?''', (online[0],))
                    
                else:
                    c.execute('''SELECT Artist SET login = "True"\
                        WHERE email = ?''', (online[1],))
                    if email == column[num]:
                        
                        c.execute('''UPDATE Artist SET email = ?\
                                WHERE login = "True" ''',(info,))
        
                    if password == column[num]:
                        c.execute('''UPDATE Artist SET password = ?\
                                WHERE login = "True" ''',(info,))
            
                    if name == column[num]:
                            c.execute('''UPDATE Artist SET name = ?\
                                WHERE login = "True" ''',(info,))
                    if username == column[num]:
                            c.execute('''UPDATE Artist SET username = ?\
                                WHERE login = "True" ''',(info,))

                    c.execute('''SELECT Artist Set login = False\
                                WHERE Artist_ID =?''', (online[0],))

                db.commit()
                    
            num += 1


        c.execute('''SELECT * FROM Consumer\
                    WHERE email = ?''', (particulars[0],))

        online = c.fetchone()

        session['user'] = online
            

        checker = True
        return render_template("profile.html",login = online, checker_updated = checker, updated = updated)
        
@app.route('/profile/top_up', methods = ["GET", "POST"])
def topup():
    successful = False
    particulars = False
    db = connect('DataBase.db')


    online = session['user']
    
    if request.method == "GET":
        return render_template('topup.html', login = online)
    if request.method == "POST":
        name = request.form.get('name')
        number = request.form.get('number')
        ccv = request.form.get('CCV')
        date = request.form.get('date')

        checking = (name, number, ccv, date)
        for check in checking:
            if check == "":
                particulars = True
                return render_template('topup.html', login = online, particulars = particulars) 
        amount = request.form.get('amount')

        #updating the amount
        current = online[6]
        new_current = current + int(amount)

        c.execute('''UPDATE Consumer SET\
                balance = ?\
                WHERE email = ?''',(new_current, online[1]))
        
        c.execute('''SELECT * FROM Consumer\
        WHERE email =  ?''', (online[1],))
        
        online = c.fetchone()

        session['user'] = online


        db.commit()
        db.close()
        successful = True

        return render_template('topup.html', login = online, successful = successful) 


@app.route('/profile/donation')
def donated():
    artist = None
    empty = None

    db = connect('DataBase.db')
    c = db.cursor()

    online = session['user']

    userID = online[0]

    
    if artist == None:
        c.execute('''SELECT Donation_ID ,name_of_song, picture, youtube_link, Price, Comment FROM Songs, Donation\
                WHERE Songs.Song_ID = Donation.SongID\
                AND Donation.collected = "False"\
                AND Donation.UserID = ?''',(userID,))
    else:
        c.execute('''SELECT Donation_ID, name_of_song, picture, youtube_link, Price, Comment FROM Songs, Donation, Artist\
                WHERE Songs.Song_ID = Donation.SongID\
                AND Artist.Artist_ID = Songs.artist_id\
                AND Donation.collected = "False"\
                AND Songs.artist_id = ?''', (userID,))
            

    donations = c.fetchall()

    if len(donations) == 0:
        empty = True

    
        
    return render_template('donated.html',empty = empty,  login = online, donations = donations, artist = artist)

@app.route('/profile/donation/received' ,methods = ["POST"])
def received():
    artist = True
    empty = None
    ID = request.form.get('button')

    db = connect('DataBase.db')
    c = db.cursor()

    online = session['user']

    ID = online[0]

    #get amount

    c.execute('''SELECT Price FROM Donation\
                WHERE Donation_ID = ?''', (ID,))

    amount = int(c.fetchone()[0])

    #get amount from artist

    c.execute('''SELECT Balance FROM Artist\
                WHERE Artist_Name = ?''', (online[1],))

    new_amount = int(c.fetchone()[0])
    new_amount += amount

    #update the artist wallet
    
    

    c.execute('''UPDATE Artist SET Balance = ?\
                WHERE Artist_ID = ?''', (new_amount, online[0]))

    #change the collected

    c.execute('''UPDATE Donation SET collected = "True"\
                WHERE Donation_ID = ?''', (ID,))

    userID = online[0]


    c.execute('''SELECT Donation_ID, name_of_song, picture, youtube_link, Price, Comment FROM Songs, Donation, Artist\
                WHERE Songs.Song_ID = Donation.SongID\
                AND Artist.Artist_ID = Songs.artist_id\
                AND Songs.artist_id = ?''', (userID,))


    donations = c.fetchall()


    if len(donations) == 0:
        empty = True

    
    db.commit()
    db.close()

    return render_template('donated.html',empty = empty,  login = online, donations = donations, artist = artist)

    

@app.route('/donation', methods = ["GET", "POST"])
def donation():
    method = False
    if request.method == "GET":
        return render_template('donation.html', method = True)

    songID = request.form.get('names')

    db = connect('DataBase.db')
    c = db.cursor()

    if 'user' in session:
        online = session['user']
    else:
        return render_template('create_account.html', login = "Please Login")

    #getting song 
    c.execute('''SELECT * FROM Songs\
                WHERE Song_ID = ?''', (songID,))

    song = c.fetchone()

        

    
    return render_template('donation.html', song = song, login =online )

@app.route('/donation/receipt', methods = ["POST"])
def receipt():
    check = None
    check_amount = None

    db = connect("DataBase.db")
    c = db.cursor()

    online = session['user']
    
    songID = request.form.get("songID")
    amount = request.form.get("amount")
    comment = request.form.get("comments")

    c.execute('''SELECT * FROM Songs\
            WHERE Song_ID = ?''', (songID,))
    song = c.fetchone()

    user = online[0]

    if amount == "":
        check = True
        return render_template('donation.html', song = song, login = online, check = check)
        
    if comment == "":
        comment = "NIL"

    #update the amount
    c.execute('''SELECT balance FROM Consumer\
                WHERE email = ?''', (online[1],))
 
    amount_left = c.fetchone()[0]
    amount_left -= int(amount)
    if amount_left < 0:
        check_amount = True
        return render_template('donation.html', song = song, login = online, check_amount = check_amount)
        

    #insert into donation

    c.execute('''INSERT INTO Donation (\
            UserID, SongID, Price, Comment, collected)
            VALUES(?,?,?,?,?)''', (user, songID, amount, comment, "False"))


    c.execute('''UPDATE Consumer SET balance = ?\
            WHERE email = ?''', (amount_left,online[1]))
    
    db.commit()
    db.close()
    
    

    return render_template('receipt.html', song  = song, login = online, amount = amount, comments = comment)




app.run(debug = True, port = 5065)
