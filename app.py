from flask import Flask, render_template, session, redirect,url_for, request,jsonify

import pymongo

import bcrypt


#app=Flask(__name__)
#secret key is used for security which keeps the client side more secure
#app.secret_key = "afn123"

#Database
#client is an object
client = pymongo.MongoClient("mongodb+srv://Areesha:gmail678@cluster0.bdzokrx.mongodb.net/" )


#covidData is a database name
db = client.get_database('HR-Management-System')

#collections in database
user_records = db.Users
corona_records = db.Students
student_records = db.Staff


app = Flask(__name__)

app.secret_key = "super secret key"
@app.route("/", methods=['post', 'get'])
def login():
    message = ''
# In sessions the server stored the data.It is basically a time period where client login and logout to the server.The server temporaily stores the user data    
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
                return render_template('index.html', message=message)
        else:
            message = 'Email is not found'
            return render_template('index.html', message=message)
    return render_template('index.html', message=message)

@app.route('/dashboard')
def dashboard():
    if "email" in session:
        email = session["email"]
        return render_template('dashboard.html', email=email)
    else:
        return redirect(url_for("login"))
    

@app.route("/register", methods=['post', 'get'])
def register():
    message = ''
# In sessions the server stored the data.It is basically a time period where client logsin and logout to the server.The server temporaily stores the user data
    if "email" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
       
        passwordA = request.form.get("passwordA")
        passwordB = request.form.get("passwordB")
       
        alreadyuser = user_records.find_one({"name": user})
        emailFounded = user_records.find_one({"email": email})
        if alreadyuser:
            message = 'The user is already exist'
            return render_template('RegistrationPage.html', message=message)
        if emailFounded:
            message = 'This email is already exist in database'
            return render_template('RegistrationPage.html', message=message)
        if passwordA != passwordB:
            message = 'Passwords should be matched!'
            return render_template('RegistrationPage.html', message=message)
        else:
            hashed = bcrypt.hashpw(passwordB.encode('utf-8'), bcrypt.gensalt())
            usersInput = {'name': user, 'email': email, 'password': hashed}
            user_records.insert_one(usersInput)
           
            userData = user_records.find_one({"email": email})
            new_email = userData['email']
   
            return render_template('dashboard.html', email=new_email)
        #We create a register form with home function
    return render_template('RegistrationPage.html')





@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("Loggedout.html")
    else:
        return render_template('RegistrationPage.html')
    

#through post operation adding a record of new patient in database.
@app.route('/createStudent', methods=['POST'])
def createNewStudent():
    
    if request.method == "POST":
     headers = {'Content-Type': 'application/json'}
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    
    student_id = student_records.insert_one({'first_name': first_name, 'last_name': last_name}).inserted_id
    newStudent = student_records.find_one({'_id': student_id})
   
    response = {
        'id': str(newStudent['_id']),
        'first_name': newStudent['first_name'],
        'last_name': newStudent['last_name']
    }  
    return jsonify(response), 200, headers
   
@app.route("/newPatient")
def newPatient():
    return render_template('newPatient.html')
@app.route("/PatientDetails")
def PatientDetails():
    return render_template('PatientDetails.html')

#through post operation adding a record of new patient in database.
@app.route('/newPatient', methods=['POST'])

def createNewpatient():
    if request.method == "POST":
     headers = {'Content-Type': 'application/json'}
    registration_date=request.form.get('registration_date')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    patient_age = request.form.get('patient_age')
    patient_gender = request.form.get('patient_gender')
    patient_country=request.form.get('patient_country')
    patient_city=request.form.get('patient_city')
    patient_postal_address = request.form.get('patient_postal_address')
    patient_email_address = request.form.get('patient_email_address')
    patient_phone_number=request.form.get('patient_phone_number')
    patient_covid_test=request.form.get('patient_covid_test')
    fever_symptom = request.form.get('fever_symptom')
    cold_symptom=request.form.get('cold_symptom')
    cough_symptom=request.form.get('cough_symptom')
    patient_id = corona_records.insert_one({'registration_date':registration_date,'first_name': first_name, 'last_name': last_name,
                                               'patient_age': patient_age, 'patient_gender': patient_gender,'patient_country':patient_country,'patient_city':patient_city, 'patient_postal_address':patient_postal_address,
                                               'patient_email_address': patient_email_address,'patient_phone_number':patient_phone_number,'patient_covid_test':patient_covid_test,'fever_symptom': fever_symptom,'cold_symptom':cold_symptom,
                                               'cough_symptom': cough_symptom}).inserted_id
    newCovidPatient = corona_records.find_one({'_id': patient_id})
   
    response = {
        'id': str(newCovidPatient['_id']),
        'registration_date':newCovidPatient['registration_date'],
        'first_name': newCovidPatient['first_name'],
        'last_name': newCovidPatient['last_name'],
        'patient_age': newCovidPatient['patient_age'],
        'patient_gender': newCovidPatient['patient_gender'],
        'patient_country':newCovidPatient['patient_country'],
        'patient_city':newCovidPatient['patient_city'],
        'patient_postal_address': newCovidPatient['patient_postal_address'],
        'patient_email_address': newCovidPatient['patient_email_address'],
        'patient_phone_number':newCovidPatient['patient_phone_number'],
        'patient_covid_test':newCovidPatient['patient_covid_test'],
        'fever_symptom': newCovidPatient['fever_symptom'],
        'cold_symptom':newCovidPatient['cold_symptom'],
        'cough_symptom ': newCovidPatient['cough_symptom']
 
    }  
    return jsonify(response), 200, headers
   
 
###########################################################################################################
 
# Get the data of all patients
@app.route('/PatientDetails', methods=['GET'])
def get_all_patients():
   
    headers = {'Content-Type': 'application/json'}
    patients = corona_records.find()
    response = []
    # for patient in patients:
    for patient in patients:
        response.append({
        'id': str(patient['_id']),
        'registration_date':patient['registration_date'],
        'first_name': patient['first_name'],
        'last_name': patient['last_name'],
        'patient_age': patient['patient_age'],
        'patient_gender': patient['patient_gender'],
        'patient_country':patient['patient_country'],
        'patient_city':patient['patient_city'],
        'patient_postal_address': patient['patient_postal_address'],
        'patient_email_address': patient['patient_email_address'],
        'patient_phone_number':patient['patient_phone_number'],
        'patient_covid_test':patient['patient_covid_test'],
        'fever_symptom': patient['fever_symptom'],
        'cold_symptom':patient['cold_symptom'],
        'cough_symptom ': patient['cough_symptom']
        })
    return jsonify(response), 200, headers
#############################################################################################################
# Get a record of particular patient.
 
@app.route('/corona_records/<first_name>/<last_name>', methods=['GET'])
def SpecificPatientDetails(first_name, last_name):
    headers = {'Content-Type': 'application/json'}
    specificPatient = corona_records.find_one({'first_name': first_name, 'last_name': last_name})
    if specificPatient:
        response = {
            'id': str(specificPatient['_id']),
 
        'registration_date':specificPatient['registration_date'],
        'first_name': specificPatient['first_name'],
        'last_name': specificPatient['last_name'],
        'patient_age': specificPatient['patient_age'],
        'patient_gender': specificPatient['patient_gender'],
        'patient_country':specificPatient['patient_country'],
        'patient_city':specificPatient['patient_city'],
        'patient_postal_address': specificPatient['patient_postal_address'],
        'patient_email_address': specificPatient['patient_email_address'],
        'patient_phone_number':specificPatient['patient_phone_number'],
        'patient_covid_test':specificPatient['patient_covid_test'],
        'fever_symptom': specificPatient['fever_symptom'],
        'cold_symptom':specificPatient['cold_symptom'],
        'cough_symptom ': specificPatient['cough_symptom']
        }
    else:
        response = {'message': 'patient not found'}
    return jsonify(response), 200, headers
###############################################################################################################################################
# Update a specific patient record
@app.route('/corona_records/<first_name>/<last_name>', methods=['PUT'])
def updatePatient(first_name, last_name):
    headers = {'Content-Type': 'application/json'}
    patient = corona_records.find_one({'first_name': first_name, 'last_name': last_name})
    if patient:
        registration_date= request.form.get('registration_date', patient['registration_date'])
        patient_age = request.form.get('patient_age', patient['patient_age'])
        patient_gender = request.form.get('patient_gender', patient['patient_gender'])
        patient_country=request.form.get('patient_country'),patient['patient_country']
        patient_city=request.form.get('patient_city'),patient['patient_city']
        patient_postal_address = request.form.get('patient_postal_address', patient['patient_postal_address'])
        patient_email_address = request.form.get('patient_email_address', patient['patient_email_address'])
        patient_phone_number=request.form.get('patient_phone_number',patient['patient_phone_number'])
        fever_symptom = request.form.get('fever_symptom', patient['fever_symptom'])
        cold_symptom=request.form.get('cold_symptom',patient['cold_symptom'])
        cough_symptom = request.form.get('cough_symptom', patient['cough_symptom'])
        corona_records.update_one({'_id': patient['_id']},
                                     {'$set': {'first_name': first_name, 'last_name': last_name,'registration_date':registration_date,
                                               'apatient_ge': patient_age, 'patient_gender': patient_gender,'patient_country':patient_country,'patient_city':patient_city ,'patient_postal_address': patient_postal_address,
                                               'patient_email_address': patient_email_address,'patient_phone_number':patient_phone_number ,'fever_symptom': fever_symptom,'cold_symptom':cold_symptom,
                                               'cough_symptom': cough_symptom}})
        patientupdate = corona_records.find_one({'first_name': first_name, 'last_name': last_name})
        response = {
            'id': str(patientupdate['_id']),
            'registration_date':patientupdate['registration_date'],
            'first_name': patientupdate['first_name'],
            'last_name': patientupdate['last_name'],
            'patient_age': patientupdate['patient_age'],
            'patient_gender': patientupdate['patient_gender'],
            'patient_country':patientupdate['patient_country'],
             'patient_city':patientupdate['patient_city'],
            'patient_postal_address': patientupdate['patient_postal_address'],
            'patient_email_address': patientupdate['patient_email_address'],
             'patient_phone_number':patientupdate['patient_phone_number'],
            'patient_covid_test':patientupdate['patient_covid_test'],
            'fever_symptom': patientupdate['fever_symptom'],
            'cold_symptom':patientupdate['cold_symptom'],
            'cough_symptom ': patientupdate['cough_symptom']}
    else:
            response = {'message': 'patient does not exist'}
    return jsonify(response), 200, headers
#####################################################################################################################
# Delete a patient record
@app.route('/corona_records/<first_name>/<last_name>', methods=['DELETE'])
def deletePatient(first_name, last_name):
    headers = {'Content-Type': 'application/json'}
    results = corona_records.delete_one({'first_name': first_name, 'last_name': last_name})
    if results.deleted_count == 1:
        response = {'message': 'The patient record is deleted successfully'}
    else:
        response = {'message': 'patient does not exists'}
    return jsonify(response), 200, headers
 



 

if __name__ == '__main__':
   app.run(port=8080, debug = True)
 
