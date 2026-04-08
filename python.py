import os
from flask import Flask, render_template, request, redirect

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__,
            template_folder=os.path.join(basedir, 'templates'),
            static_folder=os.path.join(basedir, 'static'))

patients = []
patient_id = 1  # unique ID

# Home Page
@app.route('/')
def home():
    return render_template("index.html", patients=patients)


# ➕ ADD Patient
@app.route('/add_patient', methods=['POST'])
def add_patient():
    global patient_id

    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']

    patient = {
        "id": patient_id,
        "name": name,
        "age": age,
        "gender": gender
    }

    patients.append(patient)
    patient_id += 1

    return redirect('/')


# 🚮 Delete a patient
@app.route('/delete/<int:id>')
def delete_patient(id):
    global patients
    patients = [p for p in patients if p["id"] != id]
    return redirect('/')



@app.route('/edit/<int:id>')
def edit_patient(id):
    patient = next((p for p in patients if p["id"] == id), None)
    return render_template("edit.html", patient=patient)


# 🛠️ UPDATE (Save Changes)
@app.route('/update_patient', methods=['POST'])
def update_patient():
    pid = int(request.form['id'])
    for p in patients:
        if p["id"] == pid:
            p["name"] = request.form['name']
            p["age"] = request.form['age']
            p["gender"] = request.form['gender']
            break
    return redirect('/')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)