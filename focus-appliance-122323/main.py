from flask import Flask, Response, session, request, flash, url_for, redirect, render_template, abort, g
import jinja2

from fhired import User
from fhired.FHIRQueries import FHIRQueries
from fhired.tests import testing
from flask.ext.login import LoginManager, UserMixin, login_required, login_user , logout_user , current_user

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
@app.route('/patient_history', methods=['POST'])
def patient_history():
    fhir_queries = FHIRQueries()
    patients_conditions = fhir_queries.get_all_patients_conditions(request.form['pt_id'])
    return render_template('patient_history.html', data=patients_conditions)


@login_required
@app.route('/tests')
def tests():
    output = testing()
    return render_template('tests.html', data=output)


if __name__ == '__main__':
    app.run()
