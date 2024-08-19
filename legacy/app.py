from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

# Database setup
def init_db():
    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS departments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS tokens (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            department_id INTEGER,
                            patient_name TEXT,
                            appointment_date TEXT,
                            issue_time TEXT,
                            start_time TEXT,
                            end_time TEXT,
                            status TEXT,
                            FOREIGN KEY(department_id) REFERENCES departments(id))""")
        conn.commit()

# Initialize the database
init_db()

@app.route('/')
def index():
    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()
    return render_template('index.html', departments=departments)

@app.route('/generate_token', methods=['POST'])
def generate_token():
    department_id = request.form.get('department_id')
    patient_name = request.form.get('patient_name')
    appointment_date = request.form.get('appointment_date')

    if not department_id or not appointment_date:
        flash('Please select a department and appointment date.')
        return redirect(url_for('index'))

    issue_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        # Insert the new token and retrieve the token ID
        cursor.execute("INSERT INTO tokens (department_id, patient_name, appointment_date, issue_time, status) VALUES (?, ?, ?, ?, ?)",
                       (department_id, patient_name, appointment_date, issue_time, 'waiting'))
        conn.commit()
        token_id = cursor.lastrowid  # Get the last inserted row ID (token number)

    # Redirect to a page that shows the token number
    return redirect(url_for('display_token', token_id=token_id))

@app.route('/display_token/<int:token_id>')
def display_token(token_id):
    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT tokens.id, departments.name, tokens.patient_name, tokens.appointment_date 
                          FROM tokens JOIN departments ON tokens.department_id = departments.id 
                          WHERE tokens.id = ?""", (token_id,))
        token = cursor.fetchone()
    
    return render_template('display_token.html', token=token)

@app.route('/admin')
def admin():
    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments")
        departments = cursor.fetchall()
        cursor.execute("""SELECT tokens.id, departments.name,tokens.appointment_date, tokens.patient_name, tokens.issue_time, tokens.status 
                          FROM tokens JOIN departments ON tokens.department_id = departments.id""")
        tokens = cursor.fetchall()
    return render_template('admin.html', departments=departments, tokens=tokens)

@app.route('/add_department', methods=['POST'])
def add_department():
    department_name = request.form['department_name']

    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO departments (name) VALUES (?)", (department_name,))
        conn.commit()

    flash('Department added successfully.')
    return redirect(url_for('admin'))

@app.route('/delete_token/<int:token_id>')
def delete_token(token_id):
    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tokens WHERE id = ?", (token_id,))
        conn.commit()
    
    flash('Token deleted successfully.')
    return redirect(url_for('admin'))

@app.route('/current_progress')
def current_progress():
    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT departments.name, tokens.patient_name, tokens.appointment_date, tokens.issue_time, tokens.start_time, tokens.end_time, tokens.status,tokens.id
                          FROM tokens JOIN departments ON tokens.department_id = departments.id WHERE tokens.status = 'in_progress'""")
        current_tokens = cursor.fetchall()
        
        cursor = conn.cursor()
        cursor.execute("""SELECT departments.name, tokens.patient_name, tokens.appointment_date, tokens.issue_time, tokens.start_time, tokens.end_time, tokens.status,tokens.id
                          FROM tokens JOIN departments ON tokens.department_id = departments.id WHERE tokens.status = 'waiting'""")
        next_tokens = cursor.fetchall()
        
    return render_template('current_progress.html', current_tokens=current_tokens,next_tokens=next_tokens)

@app.route("/next")
def next():
    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT departments.name, tokens.patient_name, tokens.appointment_date, tokens.issue_time, tokens.start_time, tokens.end_time, tokens.status,tokens.id
                        FROM tokens JOIN departments ON tokens.department_id = departments.id WHERE tokens.status = 'waiting'""")
        next_tokens = cursor.fetchall()
        
    return render_template('next.html',next_tokens=next_tokens)

@app.route('/doctor_terminal/<int:department_id>')
def doctor_terminal(department_id):
    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments WHERE id = ?", (department_id,))
        department = cursor.fetchone()
        cursor.execute("""SELECT * FROM tokens WHERE department_id = ? AND status = 'waiting' 
                          ORDER BY id LIMIT 1""", (department_id,))
        next_token = cursor.fetchone()
        cursor.execute("""SELECT * FROM tokens WHERE department_id = ? AND status = 'in_progress' 
                          ORDER BY id LIMIT 1""", (department_id,))
        current_token = cursor.fetchone()
    return render_template('doctor_terminal.html', department=department, next_token=next_token, current_token=current_token)

@app.route('/start_token/<int:token_id>')
def start_token(token_id):
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tokens SET status = 'in_progress', start_time = ? WHERE id = ?", (start_time, token_id))
        conn.commit()

    return redirect(url_for('doctor_terminal', department_id=request.args.get('department_id')))

@app.route('/close_token/<int:token_id>')
def close_token(token_id):
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with sqlite3.connect("hospital.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tokens SET status = 'completed', end_time = ? WHERE id = ?", (end_time, token_id))
        conn.commit()

    return redirect(url_for('doctor_terminal', department_id=request.args.get('department_id')))

if __name__ == '__main__':
    app.run(debug=True)
