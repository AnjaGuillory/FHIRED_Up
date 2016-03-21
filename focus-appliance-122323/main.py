﻿from flask import Flask, Response, session, request, flash, url_for, redirect, render_template, abort, g
import jinja2

from fhired import User
from fhired.FHIRQueries import FHIRQueries
from fhired.tests import testing
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

app = Flask(__name__)
app.jinja_loader = jinja2.FileSystemLoader('fhired/templates')
app.secret_key = "^{N^Em4B-SDV^QZ6/w[-keJ6'+KK{dt~Yz_GQmvp"
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query_user(id)


@app.before_request
def before_request():
    g.user = current_user


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for('login'))


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        remember_me = False
        if 'remember_me' in request.form:
            remember_me = True
        registered_user = User.auth(username=username, password=password)
        if registered_user is None:
            flash('Username or Password is invalid', 'error')
            return redirect(url_for('login'))
        login_user(registered_user, remember=remember_me)
        flash('Logged in successfully')
        return redirect(request.args.get('next') or url_for('dashboard'))
    return redirect(url_for("index"))


@login_required
@app.route('/patient_lookup', methods=['POST'])
def patient_lookup():
    fhir_queries = FHIRQueries()

    # TODO: (time permitting) Add support for other search options such as patient id, gender, dob, city, state

    # build list of querystring params passed to the FHIR server.
    query = {'name': request.form['pt_id']}

    return render_template('patient_lookup.html', data=fhir_queries.get_patient_for(query))


@login_required
@app.route('/analysis_table', methods=['GET'])
def analysis_table():
    fhir_queries = FHIRQueries()
    patient_id = request.args.get('pt_id', '')
    analysis_data = fhir_queries.get_analysis_data(patient_id)
    return render_template('analysis_table.html', data=analysis_data)


@login_required
@app.route('/candidate_hcc_table', methods=['GET'])
def candidate_hcc_table():
    fhir_queries = FHIRQueries()
    patient_id = request.args.get('pt_id', '')
    return render_template('candidate_hcc_table.html',
                           data={"pt_id": patient_id, "hccs": fhir_queries.get_candidate_hcc_for(patient_id)})


@login_required
@app.route('/add_candidate_hcc', methods=['POST'])
def add_candidate_hcc():
    fhir_queries = FHIRQueries()
    patient_id = request.args.get('pt_id', '')
    hcc = request.args.get('hcc', '')
    return render_template('add_candidate_hcc.html',
                           data={"pt_id": patient_id, "hcc": fhir_queries.add_hcc_candidate_hcc_for(patient_id, hcc)})


@login_required
@app.route('/reject_candidate_hcc', methods=['POST'])
def reject_candidate_hcc():
    fhir_queries = FHIRQueries()
    patient_id = request.args.get('pt_id', '')
    hcc = request.args.get('hcc', '')
    return render_template('reject_candidate_hcc.html',
                           data={"pt_id": patient_id, "hcc": fhir_queries.reject_hcc_candidate_hcc_for(patient_id, hcc)})


@login_required
@app.route('/view_candidate_hcc', methods=['POST'])
def view_candidate_hcc():
    fhir_queries = FHIRQueries()
    patient_id = request.args.get('pt_id', '')
    hcc = request.args.get('hcc', '')
    return render_template('view_candidate_hcc.html',
                           data={"pt_id": patient_id, "hcc": fhir_queries.view_hcc_candidate_hcc_for(patient_id, hcc)})



@login_required
@app.route('/tests')
def tests():
    output = testing()
    return render_template('tests.html', data=output)


@login_required
@app.route('/candidate_hcc', methods=['get'])
def candidate_hcc():
    fhir_queries = FHIRQueries()
    patient_id = request.args.get('pt_id', '')
    patient = fhir_queries.get_patient_by_id(patient_id)
    if patient is not None:
        return render_template('candidate_hcc.html', patient=patient)
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
