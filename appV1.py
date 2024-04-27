### In python each method in class has an instance of the class which is passed as its first parameter. 
### Mongodb uses '_'to identify their keys for ids.
#url_is used for links
#render template is a function which is used to render the html files in flask
#redirect is a builtin function in python. It assigns a specified code and allows the  developers to connect with specific URL. 
from flask import Flask, render_template, request, url_for, redirect, session,jsonify
#pymongo is a mongo db file for python
import pymongo
#bcrypt is used for password hashing
import bcrypt
app=Flask(__name__)
#secret key is used for security which keeps the client side more secure
app.secret_key = "Covidtesting"

#Database
#client is an object
client = pymongo.MongoClient("mongodb+srv://Areesha:gmail678@cluster0.bdzokrx.mongodb.net/")

#covidData is a database name
db = client.get_database('covidData')

### So here we create named db database" an object to represent the collection. 
#users are the collection name
user_records = db.users
corona_records=db.coronaPatients


# routes links the files to each other. 
#Methods for CRUD operations in python
#Through "POST Method" user can send data or information to server
#Through "GET METHOD" user can request and get the information from the server or specific resource
@app.route("/", methods=['post', 'get'])
def login():
    message = ''
# In sessions the server stored the data.It is basically a time period where client logsin and logout to the server.The server temporaily stores the user data    
    if "email" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

       
        emailFounded = user_records.find_one({"email": email})
        if emailFounded:
            emailvalue = emailFounded['email']
            passwordcheck = emailFounded['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = emailvalue
                return redirect(url_for('dashboard'))
            else:
                if "email" in session:
                    return redirect(url_for("dashboard"))
                message = 'password is incorrect'
                return render_template('loginform.html', message=message)
        else:
            message = 'Email is not found'
            return render_template('loginform.html', message=message)
    return render_template('loginform.html', message=message)
@app.route('/dashboard')
def dashboard():
    if "email" in session:
        email = session["email"]
        return render_template('dashboard.html', email=email)
    else:
        return redirect(url_for("login"))
if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True, port=8080)