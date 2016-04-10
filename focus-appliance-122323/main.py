﻿from flask import Flask, Response, session, request, flash, url_for, redirect, render_template, abort, g
import jinja2
import logging
from fhired import User
from fhired.FHIRed_Up import FHIRedUp
from fhired.FHIRQueries import FHIRQueries
import fhired.Entities as Entities
import fhired.utils as utils
from datetime import datetime


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

    # TODO: (time permitting) Add support for other search options such as patient gender, dob, city, state

    # build list of querystring params passed to the FHIR server.

    #logging.log(logging.INFO, request.form['pt_lookupType'])
    
    if (request.form['pt_lookupType'] == 'id'):
        # search by patient Id
        query = {'_id': request.form['pt_id']}
    else:   
        # search by name
        query = {'name': request.form['pt_id']}

    #query = {'name': request.form['pt_id']}
    return render_template('patient_lookup.html', data=fhir_queries.get_patient_for(query, 50))


@login_required
@app.route('/analysis_table', methods=['GET'])
def analysis_table():
    fhir_up = FHIRedUp()
    patient_id = request.args.get('pt_id', '')
    year = Entities.get_current_year() - int(request.args.get('years', ''))
    include_selected = request.args.get('include_selected', '') == "true"
    score_lists = fhir_up.risks_scores_list(patient_id, include_selected)

    score_distribution = fhir_up.risks_scores_distribution(patient_id, include_selected)
    current_risk_score = fhir_up.get_current_risk_score_for_pt(patient_id, include_selected)
    candidate_risk_score = fhir_up.get_candidate_risk_score_for_pt(patient_id, include_selected, year)

    bar_categories, bar_values = utils.get_categories_for_risks(score_lists)
    data = {
            'current_risk_score': current_risk_score,
            'candidate_risk_score': candidate_risk_score,
            'pie_chart_data': score_distribution,
            'bar_chart_data': {"categories": bar_categories, "values": bar_values}
    }
    return render_template('analysis_table.html', data=data)


@login_required
@app.route('/candidate_hcc_table', methods=['GET'])
def candidate_hcc_table():
    fhir_up = FHIRedUp()
    patient_id = request.args.get('pt_id', '')
    max_past_years = Entities.get_current_year() - int(request.args.get('years', ''))
    include_rejected = request.args.get('include_rejected', '') == "true"
    hccs = fhir_up.get_candidate_hccs_for(patient_id, max_past_years, include_rejected)
    return render_template('candidate_hcc_table.html', data={"pt_id": patient_id, "hccs": hccs})


@login_required
@app.route('/current_hcc_table', methods=['GET'])
def current_hcc_table():
    fhir_up = FHIRedUp()
    patient_id = request.args.get('pt_id', '')
    hccs = fhir_up.get_current_hccs_for(patient_id)
    return render_template('current_hcc_table.html', data={"pt_id": patient_id, "hccs": hccs})


@login_required
@app.route('/add_candidate_hcc', methods=['POST'])
def add_candidate_hcc():
    fhir_up = FHIRedUp()
    patient_id = request.args.get('pt_id', '')
    hcc = request.args.get('hcc', '')
    return render_template('add_candidate_hcc.html',
                           data={"pt_id": patient_id, "hcc": fhir_up.add_hcc_candidate_hcc_for(patient_id, hcc)})


@login_required
@app.route('/reject_candidate_hcc', methods=['POST'])
def reject_candidate_hcc():
    fhir_up = FHIRedUp()
    patient_id = request.args.get('pt_id', '')
    hcc = request.args.get('hcc', '')
    return render_template('reject_candidate_hcc.html',
                           data={"pt_id": patient_id, "hcc": fhir_up.reject_hcc_candidate_hcc_for(patient_id, hcc)})


@login_required
@app.route('/view_candidate_hcc', methods=['POST'])
def view_candidate_hcc():
    fhir_up = FHIRedUp()
    patient_id = request.args.get('pt_id', '')
    hcc = request.args.get('hcc', '')
    return render_template('view_candidate_hcc.html',
                           data={"pt_id": patient_id, "hcc": fhir_up.view_hcc_candidate_hcc_for(patient_id, hcc)})


@login_required
@app.route('/create_sample')
def create_sample():
    from model import SampleModel
    s = SampleModel(name="Test")
    s.put()
    return redirect(url_for('login'))


@login_required
@app.route('/candidate_hcc', methods=['get'])
def candidate_hcc():
    fhir_queries = FHIRQueries()
    fhir_up = FHIRedUp()
    patient_id = request.args.get('pt_id', '')
    patient = fhir_queries.get_patient_by_id(patient_id)
    include_selected = False # TODO Get from persistence
    risk_value = fhir_up.get_current_risk_score_for_pt(patient_id, include_selected)
    current_year = Entities.get_current_year()

    if patient is not None:
        return render_template('candidate_hcc.html', patient=patient, risk_meter=risk_value, current_year=current_year)
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
