from flask import Flask
app=Flask(__name__)
@app.route('/patients')
def patients():
    return "x"
if(__name__)=='__main__':
    app.run(debug=True)