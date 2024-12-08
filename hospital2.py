from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page route
@app.route('/')
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Doctors')
    doctors = cursor.fetchall()
    conn.close()
    return render_template('home.html', doctors=doctors)

# Book appointment route
@app.route('/book_appointment/<int:doctor_id>', methods=['GET', 'POST'])
def book_appointment(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Doctors WHERE id = ?', (doctor_id,))
    doctor = cursor.fetchone()

    if request.method == 'POST':
        patient_name = request.form['name']
        patient_age = request.form['age']
        patient_contact = request.form['contact']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']  # Added time field

        cursor.execute('INSERT INTO Appointments (doctor_id, patient_name, patient_age, patient_contact, appointment_date, appointment_time) VALUES (?, ?, ?, ?, ?, ?)',
                       (doctor_id, patient_name, patient_age, patient_contact, appointment_date, appointment_time))
        conn.commit()

        # Get the ID of the inserted appointment
        appointment_id = cursor.lastrowid
        conn.close()

        # Redirect to view the specific appointment details
        return redirect(url_for('view_appointment', appointment_id=appointment_id))

    conn.close()
    return render_template('book_appointment.html', doctor=doctor)

# View all appointments route
@app.route('/view_appointments')
def view_appointments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
        SELECT Appointments.*, Doctors.first_name, Doctors.last_name, Doctors.specialization 
        FROM Appointments
        JOIN Doctors ON Appointments.doctor_id = Doctors.id
    ''')
    appointments = cursor.fetchall()
    conn.close()
    return render_template('view_appointments.html', appointments=appointments)

# View a single appointment details route
@app.route('/view_appointment/<int:appointment_id>')
def view_appointment(appointment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Appointments.*, Doctors.first_name, Doctors.last_name, Doctors.specialization 
        FROM Appointments
        JOIN Doctors ON Appointments.doctor_id = Doctors.id
        WHERE Appointments.id = ?
    ''', (appointment_id,))
    appointment = cursor.fetchone()
    conn.close()
    return render_template('view_appointment.html', appointment=appointment)

# Initialize database
def init_db():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    # Drop existing Appointments table (if schema issue exists)
    cursor.execute('DROP TABLE IF EXISTS Appointments')

    # Create Doctors table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Doctors (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        education TEXT NOT NULL,
                        department TEXT NOT NULL,
                        specialization TEXT NOT NULL)''')

    # Create Appointments table (added appointment_time field)
    cursor.execute('''CREATE TABLE Appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        doctor_id INTEGER NOT NULL,
                        patient_name TEXT NOT NULL,
                        patient_age INTEGER NOT NULL,
                        patient_contact TEXT NOT NULL,
                        appointment_date TEXT NOT NULL,
                        appointment_time TEXT NOT NULL,
                        FOREIGN KEY (doctor_id) REFERENCES Doctors (id))''')

    # Insert sample doctors if none exist
    cursor.execute('SELECT COUNT(*) FROM Doctors')
    if cursor.fetchone()[0] == 0:
        sample_doctors = [
            ('John', 'Doe', 'MD, Harvard University', 'Cardiology', 'Heart Surgery'),
            ('Jane', 'Smith', 'MBBS, Oxford University', 'Neurology', 'Brain Surgery'),
            ('Alan', 'Turing', 'MD, Stanford University', 'Pediatrics', 'Child Care'),
            ('Emily', 'Davis', 'MBBS, Yale University', 'Orthopedics', 'Bone and Joint Surgery'),
            ('Michael', 'Johnson', 'MD, Johns Hopkins University', 'Oncology', 'Cancer Treatment')
        ]
        cursor.executemany('INSERT INTO Doctors (first_name, last_name, education, department, specialization) VALUES (?, ?, ?, ?, ?)', sample_doctors)
        conn.commit()

    conn.close()

# Initialize the database
init_db()

if __name__ == '__main__':
    app.run(debug=True)
