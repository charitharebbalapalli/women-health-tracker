from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
<<<<<<< HEAD
import os

from datetime import datetime, date, timedelta

from werkzeug.security import generate_password_hash, check_password_hash



=======
from werkzeug.security import generate_password_hash, check_password_hash
import os
>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531

app = Flask(__name__)

# Secret key for sessions
app.secret_key = 'your_secret_key_here_change_in_production'

<<<<<<< HEAD


=======
# MySQL Configuration
>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'women_health'

mysql = MySQL(app)
<<<<<<< HEAD
#  AUTHENTICATION ROUTES
=======

# ================ AUTHENTICATION ROUTES ================
>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531

@app.route('/')
def index():
    if 'loggedin' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate inputs
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            msg = 'Invalid email address!'
        elif password != confirm_password:
            msg = 'Passwords do not match!'
        elif not name or not email or not password:
            msg = 'Please fill out all fields!'
        else:
            # Check if email already exists
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                msg = 'Email already registered!'
            else:
                # Insert new user with hashed password
                hashed_password = generate_password_hash(password)
                cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', 
                             (name, email, hashed_password))
                mysql.connection.commit()
                msg = 'Registration successful! Please login.'
                return redirect(url_for('login'))
            cursor.close()

    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password):
            session['loggedin'] = True
            session['id'] = user['id']
            session['name'] = user['name']
            session['email'] = user['email']
            msg = 'Login successful!'
            return redirect(url_for('dashboard'))
        else:
            msg = 'Invalid email or password!'

    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

<<<<<<< HEAD
# DASHBOARD ROUTE 
=======
# ================ DASHBOARD ROUTE ================
>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531

@app.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = session['id']

<<<<<<< HEAD
    # PERIOD
    cursor.execute('SELECT * FROM periods WHERE user_id = %s ORDER BY id DESC LIMIT 1', (user_id,))
    period = cursor.fetchone()

    # SYMPTOMS
    cursor.execute('SELECT * FROM symptoms WHERE user_id = %s ORDER BY id DESC LIMIT 1', (user_id,))
    symptoms = cursor.fetchone()

    # PREGNANCY
    cursor.execute('SELECT * FROM pregnancy WHERE user_id = %s ORDER BY id DESC LIMIT 1', (user_id,))
    pregnancy = cursor.fetchone()

    # ================= SAFE DEFAULTS =================
    is_pregnant = False
    active_mode = "period"
    pcos_risk = "No Data"

    # ================= PREGNANCY LOGIC =================
    if pregnancy:
        try:
            week = int(pregnancy.get('week', 0))
            is_pregnant = 1 <= week <= 40
            active_mode = "pregnancy" if is_pregnant else "period"
        except:
            is_pregnant = False

    # ================= PCOS LOGIC =================
    if symptoms:
        score = (
            (symptoms.get('weight_gain') or 0) +
            (symptoms.get('acne') or 0) +
            (symptoms.get('irregular_cycle') or 0)
        )

        if score >= 2:
            pcos_risk = "High"
        elif score == 1:
            pcos_risk = "Moderate"
        else:
            pcos_risk = "Low"

    # ================= IMPORTANT RETURN =================
    return render_template(
        'dashboard.html',
        name=session['name'],
        period=period,
        pregnancy=pregnancy,
        symptoms=symptoms,
        active_mode=active_mode,
        pcos_risk=pcos_risk
    )
#  PERIOD TRACKER 
=======
    # Get latest period data
    cursor.execute('SELECT * FROM periods WHERE user_id = %s ORDER BY id DESC LIMIT 1', (user_id,))
    period = cursor.fetchone()

    # Get latest pregnancy data
    cursor.execute('SELECT * FROM pregnancy WHERE user_id = %s ORDER BY id DESC LIMIT 1', (user_id,))
    pregnancy = cursor.fetchone()

    # Get latest symptoms
    cursor.execute('SELECT * FROM symptoms WHERE user_id = %s ORDER BY recorded_at DESC LIMIT 1', (user_id,))
    symptoms = cursor.fetchone()

    cursor.close()

    return render_template('dashboard.html', 
                         name=session['name'],
                         period=period,
                         pregnancy=pregnancy,
                         symptoms=symptoms)

# ================ PERIOD TRACKER ================
>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531

@app.route('/periods', methods=['GET', 'POST'])
def periods():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    msg = ''
    if request.method == 'POST':
        last_period = request.form.get('last_period')
        cycle_length = request.form.get('cycle_length')

        if last_period and cycle_length:
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO periods (user_id, last_period, cycle_length) VALUES (%s, %s, %s)',
                             (session['id'], last_period, int(cycle_length)))
                mysql.connection.commit()
                cursor.close()
                msg = 'Period data saved successfully!'
            except Exception as e:
                msg = f'Error saving data: {str(e)}'
        else:
            msg = 'Please fill in all fields!'

    # Get user's period history
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM periods WHERE user_id = %s ORDER BY id DESC', (session['id'],))
    history = cursor.fetchall()
    cursor.close()

    return render_template('periods.html', msg=msg, history=history)

<<<<<<< HEAD
#  PREGNANCY TRACKER 
=======
# ================ PREGNANCY TRACKER ================
>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531

@app.route('/pregnancy', methods=['GET', 'POST'])
def pregnancy():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    msg = ''
    if request.method == 'POST':
        last_period = request.form.get('last_period')
<<<<<<< HEAD
        

        if last_period :
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO pregnancy (user_id, last_period) VALUES (%s, %s)',
                             (session['id'], last_period))
=======
        due_date = request.form.get('due_date')
        week = request.form.get('week')

        if last_period and due_date and week:
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO pregnancy (user_id, last_period, due_date, week) VALUES (%s, %s, %s, %s)',
                             (session['id'], last_period, due_date, int(week)))
>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531
                mysql.connection.commit()
                cursor.close()
                msg = 'Pregnancy data saved successfully!'
            except Exception as e:
                msg = f'Error saving data: {str(e)}'
        else:
            msg = 'Please fill in all fields!'

    # Get user's pregnancy history
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM pregnancy WHERE user_id = %s ORDER BY id DESC', (session['id'],))
    history = cursor.fetchall()
    cursor.close()

    return render_template('pregnancy.html', msg=msg, history=history)

<<<<<<< HEAD
#  SYMPTOMS TRACKER 
=======
# ================ SYMPTOMS TRACKER ================
>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531

@app.route('/symptoms', methods=['GET', 'POST'])
def symptoms():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    msg = ''
<<<<<<< HEAD
    history = []

    if request.method == 'POST':
        try:
            weight_gain = 1 if request.form.get('weight_gain') else 0
            acne = 1 if request.form.get('acne') else 0
            irregular_cycle = 1 if request.form.get('irregular_cycle') else 0
            cursor = mysql.connection.cursor()
            cursor.execute(
                'INSERT INTO symptoms (user_id, weight_gain, acne, irregular_cycle) VALUES (%s, %s, %s, %s)',
                (session['id'], weight_gain, acne, irregular_cycle)
            )
            mysql.connection.commit()
            cursor.close()

            msg = 'Symptoms recorded successfully!'

        except Exception as e:
            msg = f'Error saving data: {str(e)}'

    # ALWAYS FETCH HISTORY (outside POST block)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT * FROM symptoms WHERE user_id = %s ORDER BY id DESC LIMIT 10',
        (session['id'],)
    )
=======
    if request.method == 'POST':
        weight_gain = 1 if request.form.get('weight_gain') else 0
        acne = 1 if request.form.get('acne') else 0
        irregular_cycle = 1 if request.form.get('irregular_cycle') else 0

        try:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO symptoms (user_id, weight_gain, acne, irregular_cycle) VALUES (%s, %s, %s, %s)',
                         (session['id'], weight_gain, acne, irregular_cycle))
            mysql.connection.commit()
            cursor.close()
            msg = 'Symptoms recorded successfully!'
        except Exception as e:
            msg = f'Error saving data: {str(e)}'

    # Get user's symptoms history
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM symptoms WHERE user_id = %s ORDER BY recorded_at DESC LIMIT 10', (session['id'],))
>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531
    history = cursor.fetchall()
    cursor.close()

    return render_template('symptoms.html', msg=msg, history=history)

<<<<<<< HEAD
=======
# ================ REPORTS ================

>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531
@app.route('/reports')
def reports():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    user_id = session['id']

<<<<<<< HEAD
    # ================= PERIOD DATA =================
    cursor.execute(
        'SELECT * FROM periods WHERE user_id = %s ORDER BY id DESC',
        (user_id,)
    )
    periods_data = cursor.fetchall()


    # ================= PREGNANCY DATA =================
    cursor.execute(
    'SELECT * FROM pregnancy WHERE user_id = %s ORDER BY id DESC',
    (user_id,)
)

    pregnancy_data = cursor.fetchall()

    latest_pregnancy = pregnancy_data[0] if pregnancy_data else None

    is_pregnant = latest_pregnancy is not None

    # ================= SYMPTOMS DATA =================
    cursor.execute(
        'SELECT * FROM symptoms WHERE user_id = %s ORDER BY id DESC',
        (user_id,)
    )
=======
    # Get all periods
    cursor.execute('SELECT * FROM periods WHERE user_id = %s ORDER BY id DESC', (user_id,))
    periods_data = cursor.fetchall()

    # Get all pregnancy records
    cursor.execute('SELECT * FROM pregnancy WHERE user_id = %s ORDER BY id DESC', (user_id,))
    pregnancy_data = cursor.fetchall()

    # Get all symptoms
    cursor.execute('SELECT * FROM symptoms WHERE user_id = %s ORDER BY recorded_at DESC', (user_id,))
>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531
    symptoms_data = cursor.fetchall()

    cursor.close()

<<<<<<< HEAD
   
    # ================= PREGNANCY CALCULATION =================
    pregnancy_week = "No Data"
    due_date = "No Data"

    if latest_pregnancy:

        last_period = latest_pregnancy.get('last_period')

        if isinstance(last_period, str):
            last_period = datetime.strptime(last_period, "%Y-%m-%d").date()

        if last_period:
            due_date = last_period + timedelta(days=280)
            pregnancy_week = (date.today() - last_period).days // 7

    # ================= PERIOD STATUS =================
    if is_pregnant:
        period_status = "Pregnant - Period tracking disabled"
    elif periods_data:
        cycle_length = periods_data[0]['cycle_length']

        if 21 <= cycle_length <= 35:
            period_status = "Regular"
        else:
            period_status = "Irregular"
    else:
        period_status = "No Data"

    
    # ================= PCOS RISK =================
    pcos_risk = "No Data"

    if is_pregnant:
       pcos_risk = "Not applicable during pregnancy"

    elif symptoms_data:
       latest = symptoms_data[0]

       score = (
          latest.get('weight_gain', 0) +
          latest.get('acne', 0) +
          latest.get('irregular_cycle', 0)
        )

       if score >= 2:
          pcos_risk = "High"
       elif score == 1:
          pcos_risk = "Moderate"
       else:
        pcos_risk = "Low"

    # ================= TIPS =================
    tips = []

    if symptoms_data and not is_pregnant:
        latest_symptom = symptoms_data[0]

        if latest_symptom.get('weight_gain') == 1:
            tips.append("Maintain a balanced diet and exercise regularly.")
        if latest_symptom.get('acne') == 1:
            tips.append("Drink more water and reduce oily foods.")
        if latest_symptom.get('irregular_cycle') == 1:
            tips.append("Track your cycle regularly.")

    if is_pregnant:
        week = 0

        if latest_pregnancy:
            try:
                week = int(latest_pregnancy.get('week', 0))
            except:
                week = 0

        if week <= 12:
            tips.append("Take folic acid and attend prenatal checkups.")
        elif week <= 28:
            tips.append("Maintain a healthy diet rich in iron and calcium.")
        else:
            tips.append("Monitor fetal movements and prepare for delivery.")

    if not tips:
        tips.append("Keep maintaining a healthy lifestyle.")

    # ================= RENDER =================
    return render_template(
        'reports.html',
        periods=periods_data,
        pregnancies=pregnancy_data,
        symptoms=symptoms_data,
        period_status=period_status,
        pcos_risk=pcos_risk,
        tips=tips,
        pregnancy_week=pregnancy_week,
        due_date=due_date,
        active_mode="pregnancy" if is_pregnant else "period"
    )
    

#  ERROR HANDLERS 
=======
    return render_template('reports.html', 
                         periods=periods_data,
                         pregnancies=pregnancy_data,
                         symptoms=symptoms_data)

# ================ ERROR HANDLERS ================
>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531

@app.errorhandler(404)
def page_not_found(error):
    return "Page not found", 404

@app.errorhandler(500)
def server_error(error):
    return "Server error", 500

if __name__ == '__main__':
<<<<<<< HEAD
    app.run(debug=True, host='localhost', port=5000)  
=======
    app.run(debug=True, host='localhost', port=5000)
>>>>>>> 56dab72efd3c75dfc876bdec4523a5b77689f531
