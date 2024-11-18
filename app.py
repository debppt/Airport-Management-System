from flask import Flask, render_template, request
import mysql.connector
from flask_cors import CORS
from mysql.connector import IntegrityError

app = Flask(__name__, template_folder='.')
CORS(app)

# =======================
# Database Configuration
# =======================

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='namanmysql@1',
        database='airport'
    )

# =======================
# Homepage and Navigation
# =======================

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/login_passenger')
def about_page():
    return render_template('pass_sign_in.html')

@app.route('/login_as_admin')
def login_as_admin():
    return render_template('admin_sign_in.html')

@app.route('/login_as_employee')
def login_as_employee():
    return render_template('employee_sign_in.html')

@app.route('/sign_up_pass')
def sign_up_pass():
    return render_template('pass_sign_up.html')

@app.route('/sign_up_employee')
def sign_up_employee():
    return render_template('employee_sign_up.html')

@app.route('/sign_in_after_sign_up')
def sign_in_after_sign_up():
    return render_template('pass_sign_in.html')

# =======================
# Passenger Routes
# =======================

#sign-in passenger
@app.route('/check_passenger_id', methods=['POST'])
def check_passenger_id():
    passenger_id = request.form['passenger_id']
    message = None
    message_type = None

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Define the output variable
        is_valid = None
        passenger_id = int(passenger_id)
        
        # Call the stored procedure
        cursor.callproc('CheckPassengerID', (passenger_id,))
        
        # Fetch the output parameter
        for result in cursor.stored_results():
            is_valid = result.fetchone()['is_valid']  # Fetch the first (and only) result

        # Determine the message based on the result
        if is_valid:
            message = f"Passenger ID {passenger_id} exists."
            message_type = "success"
        else:
            message = f"Passenger ID {passenger_id} does not exist."
            message_type = "error"
    except Exception as e:
        message = f"Error checking Passenger ID: {str(e)}"
        message_type = "error"
    finally:
        cursor.close()
        conn.close()

    return render_template('pass_sign_in.html', message=message, message_type=message_type)

#sign-up passenger
@app.route('/register_passenger', methods=['GET', 'POST'])
def register_passenger():
    passenger_id = None
    error_message = None

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        nationality = request.form['nationality']
        passport_number = request.form['passport_number']
        phone_number = request.form['phone_number']

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query = """
            INSERT INTO passenger (F_Name, L_Name, Gender, Nationality, Passport_No)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (first_name, last_name, gender, nationality, passport_number))
            conn.commit()

            passenger_id = cursor.lastrowid

            phone_query = """
            INSERT INTO `passenger-contacts` (Passenger_id, Contact)
            VALUES (%s, %s)
            """
            cursor.execute(phone_query, (passenger_id, phone_number))
            conn.commit()
        except IntegrityError as e:
            conn.rollback()
            if "Duplicate entry" in str(e):
                error_message = f"Passport number '{passport_number}' is already registered. Please use a different one."
            else:
                error_message = "An error occurred while processing your request. Please try again."
        except Exception as e:
            conn.rollback()
            error_message = f"Unexpected error: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    return render_template('pass_sign_up.html', passenger_id=passenger_id, error_message=error_message)

@app.route('/book_ticket')
def book_ticket():
    return render_template('book_ticket.html')

@app.route('/see_tickets')
def see_ticket():
    return render_template('see_ticket.html')

@app.route('/view_tickets_action', methods=['GET', 'POST'])
def view_tickets_form():
    if request.method == 'POST':
        passenger_id = request.form['passenger-id']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT Seat_No, Booking_Date, Booking_Status, Flight_id, Airline_id, Passenger_id, ticketscol
        FROM tickets
        WHERE Passenger_id = %s
        """
        cursor.execute(query, (passenger_id,))
        tickets = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('view_tickets_action.html', tickets=tickets)

    return render_template('see_ticket.html')

# =======================
# Admin Routes
# =======================

@app.route('/admin_landing_page')
def admin_landing_page():
    return render_template('admin_landing_page.html')

@app.route('/add_airline_page')
def add_airline_page():
    return render_template('add_airline.html')

@app.route('/ADD_FLIGHT_DETAILS')
def ADD_FLIGHT_DETAILS():
    return render_template('add_flight_details.html')

@app.route('/view_employees')
def view_employees():
    return render_template('view_employee.html')

@app.route('/delete_employee')
def delete_employees():
    return render_template('delete_employee.html')

@app.route('/add_employee')
def add_employee():
    return render_template('add_employee.html')

@app.route('/update_g_r')
def update_g_r():
    return render_template('update_gate_runway.html')

@app.route('/view_reports')
def view_reports():
    return render_template('View_Report.html')

# =======================
# Baggage Routes
# =======================

@app.route('/baggage_status')
def baggage_status():
    return render_template('Baggage.html')

@app.route('/view_baggage_status_action', methods=['GET', 'POST'])
def view_baggage_status_action():
    if request.method == 'POST':
        passenger_id = request.form['passenger-id']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT Baggage_No, P_id, Status
        FROM Baggage
        WHERE P_id = %s
        """
        cursor.execute(query, (passenger_id,))
        baggage = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('view_baggage_status_action.html', baggage=baggage)

    return render_template('Baggage.html')



# EMPLOYEE
# Route to view the employee details
@app.route('/check_employee_id', methods=['POST'])
def employee_dashboard():
    employee_id = request.form['employee_id']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query to fetch employee data
    query = """
    SELECT 
        employee_id, f_name, l_name, salary, g_no, r_no
    FROM employee
    WHERE employee_id = %s
    """
    cursor.execute(query, (employee_id,))
    employee_data = cursor.fetchone()  # Fetch one employee's details

    cursor.close()
    conn.close()

    if employee_data:
        return render_template('employee_dashboard.html', employee=employee_data)
    else:
        return render_template('employee_sign_in.html', error_message="Invalid Employee ID")


if __name__ == '__main__':
    app.run(debug=True)



# =======================
# App Entry Point
# =======================

if __name__ == '__main__':
    app.run(debug=True)
