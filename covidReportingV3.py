# server file of covid reporting system
#rendertemplate helps to render the html pages in the flask app
from flask import Flask, render_template, request, jsonify  #this will allow using this device as a local server
from flask_pymongo import PyMongo    #imported the flask from pyMongo. It allows to use mongo db database.

app = Flask(__name__)       #app is an instance from the server. It is a standard code which we have to write when we perform the tasks in flask
#Methods
#Routes are used to link the files in flasks
@app.route('/')
def home():               #This method is used to examine the working of the server if it is running fine.
    return ("the server is sucessfully is connecting")

app.config[                           #cofig method is used to define and specify the path of mongodb database
    'MONGO_URI'] = 'mongodb+srv://areeshatahir321:gmail678@cluster0.mjfivyq.mongodb.net/restfuldatabase?retryWrites=true&w=majority'
mongo = PyMongo(app)


#################################################################################################

# Adding a record of new patient.
@app.route('/coronaPatients', methods=['POST'])
def createNewpatient():
    headers = {'Content-Type': 'application/json'}
    patientFirstName = request.json['patientFirstName']
    patientLastName = request.json['patientLastName']
    patientAge = request.json['patientAge']
    patientGender = request.json['patientGender']
    patientPostalAddress = request.json['patientPostalAddress']
    patientEmailAddress = request.json['patientEmailAddress']
    patientSymptom_Fever = request.json['patientSymptom_Fever']
    patientSymptom_Cough = request.json['patientSymptom_Cough']
    patient_id = mongo.db.coronaPatients.insert_one({'patientFirstName': patientFirstName, 'patientLastName': patientLastName,
                                               'patientAge': patientAge, 'patientGender': patientGender, 'patientPostalAddress': patientPostalAddress,
                                               'patientEmailAddress': patientEmailAddress, 'patientSymptom_Fever': patientSymptom_Fever,
                                               'patientSymptom_Cough': patientSymptom_Cough}).inserted_id
    newPatient = mongo.db.coronaPatients.find_one({'_id': patient_id})
    response = {
        'id': str(newPatient['_id']),
        'patientFirstName': newPatient['patientFirstName'],
        'patientLastName': newPatient['patientLastName'],
        'patientAge': newPatient['patientAge'],
        'patientGender': newPatient['patientGender'],
        'patientPostalAddress': newPatient['patientPostalAddress'],
        'patientEmailAddress': newPatient['patientEmailAddress'],
        'patientSymptom_Fever': newPatient['patientSymptom_Fever'],
        'patientSymptom_Cough': newPatient['patientSymptom_Cough']
    }
    return jsonify(response), 200, headers


##############################################################################################################################
# Get the data of all patients
@app.route('/coronaPatients', methods=['GET'])
def get_patients_details():
    headers = {'Content-Type': 'application/json'}
    patients_details = mongo.db.coronaPatients.find()
    response = []
    for patient_details in patients_details:
        response.append({
            'id': str(patient_details['_id']),
            'patientFirstName': patient_details['patientFirstName'],
            'patientLastName': patient_details['patientLastName'],
            'patientAge': patient_details['patientAge'],
            'patientGender': patient_details['patientGender'],
            'patientPostalAddress': patient_details['patientPostalAddress'],
            'patientEmailAddress': patient_details['patientEmailAddress'],
            'patientSymptom_Fever': patient_details['patientSymptom_Fever'],
            'patientSymptom_Cough': patient_details['patientSymptom_Cough']
        })
    return jsonify(response), 200, headers


########################################################################################################

# Get a record of particular patient.
@app.route('/coronaPatients/<patientFirstName>/<patientLastName>', methods=['GET'])
def get_patientInfo(patientFirstName, patientLastName):
    headers = {'Content-Type': 'application/json'}
    SpecificPatient = mongo.db.coronaPatients.find_one({'patientFirstName': patientFirstName, 'patientLastName': patientLastName})
    if SpecificPatient:
        response = {
            'id': str(SpecificPatient['_id']),
            'patientFirstName': SpecificPatient['patientFirstName'],
            'patientLastName': SpecificPatient['patientLastName'],
            'patientAge': SpecificPatient['patientAge'],
            'patientGender': SpecificPatient['patientGender'],
            'patientPostalAddress': SpecificPatient['patientPostalAddress'],
            'patientEmailAddress': SpecificPatient['patientEmailAddress'],
            'patientSymptom_Fever': SpecificPatient['patientSymptom_Fever'],
            'patientSymptom_Cough': SpecificPatient['patientSymptom_Cough']
        }
    else:
        response = {'message': 'patient not found'}
    return jsonify(response), 200, headers




#################################################################################################
# Update a specific patient record
@app.route('/coronaPatients/<patientFirstName>/<patientLastName>', methods=['PUT'])
def updatePatientDetails(patientFirstName, patientLastName):
    headers = {'Content-Type': 'application/json'}
    SpecificPatient = mongo.db.coronaPatients.find_one({'patientFirstName': patientFirstName, 'patientLastName': patientLastName})
    if SpecificPatient:
        patientAge = request.json.get('patientAge', SpecificPatient['patientAge'])
        patientGender = request.json.get('patientGender', SpecificPatient['patientGender'])
        patientPostalAddress = request.json.get('patientPostalAddress', SpecificPatient['patientPostalAddress'])
        patientEmailAddress = request.json.get('patientEmailAddress', SpecificPatient['patientEmailAddress'])
        patientSymptom_Fever= request.json.get('patientSymptom_Fever', SpecificPatient['patientSymptom_Fever'])
        patientSymptom_Cough = request.json.get('patientSymptom_Cough', SpecificPatient['patientSymptom_Cough'])
        mongo.db.coronaPatients.update_one({'_id': SpecificPatient['_id']},
                                     {'$set': {'patientFirstName': patientFirstName, 'patientLastName': patientLastName,
                                               'patientAge': patientAge, 'patientGender': patientGender, 'patientPostalAddress': patientPostalAddress,
                                               'patientEmailAddress': patientEmailAddress, 'patientSymptom_Fever': patientSymptom_Fever,
                                               'patientSymptom_Cough': patientSymptom_Cough}})
        updatedpatientrecord = mongo.db.coronaPatients.find_one({'patientFirstName': patientFirstName, 'patientLastName': patientLastName})
        response = {
            'id': str(updatedpatientrecord['_id']),
            'patientFirstName': updatedpatientrecord['patientFirstName'],
            'patientLastName': updatedpatientrecord['patientLastName'],
            'patientAge': updatedpatientrecord['patientAge'],
            'patientGender': updatedpatientrecord['patientGender'],
            'patientPostalAddress': updatedpatientrecord['patientPostalAddress'],
            'patientEmailAddress': updatedpatientrecord['patientEmailAddress'],
            'patientSymptom_Fever': updatedpatientrecord['patientSymptom_Fever'],
            'patientSymptom_Cough': updatedpatientrecord['patientSymptom_Cough']
        }
    else:
        response = {'message': 'patient not found'}
    return jsonify(response), 200, headers




###############################################################################################
# Delete a patient record
@app.route('/coronaPatients/<patientFirstName>/<patientLastName>', methods=['DELETE'])
def deletepatientrecord(patientFirstName, patientLastName):
    headers = {'Content-Type': 'application/json'}
    result = mongo.db.coronaPatients.delete_one({'patientFirstName': patientFirstName, 'patientLastName': patientLastName})
    if result.deleted_count == 1:
        response = {'message': 'patient record is deleted successfully'}
    else:
        response = {'message': 'patient record is not found'}
    return jsonify(response), 200, headers


if __name__ == '__main__':
    app.run(debug=True)