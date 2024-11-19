from flask import Flask, render_template, request
import mysql.connector
from flask_cors import CORS
from mysql.connector import IntegrityError, Error
import re #for iata validation
from datetime import datetime

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

def is_valid_iata_code(iata_code):
    # A valid IATA code is exactly 2 uppercase letters
    return bool(re.match(r'^[A-Z]{2}$', iata_code))

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

@app.route('/add_airline', methods=['GET', 'POST'])
def add_airline():
    if request.method == 'POST':
        # Retrieve form data
        airline_name = request.form.get('airline_name')
        iata_code = request.form.get('iata_code')
        ceo_name = request.form.get('ceo_name')

        # Validate IATA code format
        if not is_valid_iata_code(iata_code):
            return render_template('add_airline.html', error="Invalid IATA Code. It should be exactly 2 uppercase letters.")

        try:
            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert query
            query = """
            INSERT INTO Airline (Airline_Name,  CEO, IATA_Code)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (airline_name, ceo_name, iata_code))
            conn.commit()

            # Close the connection
            cursor.close()
            conn.close()

            # Success response
            return render_template('add_airline.html', success="Airline added successfully!")

        except IntegrityError:
            return render_template('add_airline.html', error="IATA Code already exists. Please use a unique IATA Code.")
        except Exception as e:
            return render_template('add_airline.html', error=f"An error occurred: {str(e)}")

    # Render form for GET request
    return render_template('add_airline.html')

@app.route('/ADD_FLIGHT_DETAILS')
def ADD_FLIGHT_DETAILS():
    return render_template('add_flight_details.html')

@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if request.method == 'POST':
        # Retrieving the form data
        flight_id = request.form['flight_number']  # Assuming this is the Flight ID, map this if necessary
        airline_name = request.form['airline']
        city = request.form['city']
        flight_status = request.form['flight_status']
        departure_time = request.form['departure_time']
        arrival_time = request.form['arrival_time']
        runway_number = request.form['runway_number']
        gate_number = request.form['gate_number']

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Get AL_ID from airline
            cursor.execute("SELECT Airline_id FROM airline WHERE Airline_name = %s", (airline_name,))
            airline_result = cursor.fetchone()
            if not airline_result:
                raise ValueError(f"Airline '{airline_name}' not found")
            al_id = airline_result['Airline_id']

            # Get AP_ID from airport
            cursor.execute("SELECT Airport_id FROM airport WHERE City = %s", (city,))
            airport_result = cursor.fetchone()
            if not airport_result:
                raise ValueError(f"Airport in city '{city}' not found")
            ap_id = airport_result['Airport_id']

            # Get Runway ID
            cursor.execute("SELECT Runway_No FROM runway WHERE Runway_No = %s", (runway_number,))
            runway_result = cursor.fetchone()
            if not runway_result:
                raise ValueError(f"Runway '{runway_number}' not found")
            runway_n = runway_result['Runway_No']

            # Get Gate ID
            cursor.execute("SELECT Gate_No FROM gate WHERE Gate_No = %s", (gate_number,))
            gate_result = cursor.fetchone()
            if not gate_result:
                raise ValueError(f"Gate '{gate_number}' not found")
            gate_n = gate_result['Gate_No']

            # Calculate wait duration (difference between arrival and departure times)
            # Convert the datetime strings to datetime objects first
            departure_datetime = datetime.strptime(departure_time, "%Y-%m-%dT%H:%M")
            arrival_datetime = datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M")
            wait_duration = arrival_datetime - departure_datetime

            # Insert flight details into flight table
            query = """
            INSERT INTO flight (Flight_id, Arrival_time, Departure_time, Status, Wait_Duration, AP_ID, AL_ID, Runway_N, Gate_N)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (flight_id, arrival_time, departure_time, flight_status, wait_duration, ap_id, al_id, runway_n, gate_n))
            conn.commit()  # Commit the transaction

            # Success message
            success_message = "Flight details added successfully!"
            return render_template('add_flight_details.html', success=success_message)

        except Exception as e:
            # Error handling
            conn.rollback()  # Rollback in case of an error
            error_message = f"An error occurred: {str(e)}"
            return render_template('add_flight_details.html', error=error_message)

        finally:
            cursor.close()
            conn.close()

    return render_template('add_flight_details.html')  # If GET request, just show the form

@app.route('/view_employees')
def view_employees():
    return render_template('view_employee.html')

@app.route('/view_all_employees')
def view_all_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_all_employee.html', employees=employees)


@app.route('/delete_employee', methods=['GET', 'POST'])
def delete_employee():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Check if the employee exists first
            cursor.execute("SELECT * FROM employee WHERE Employee_id = %s", (employee_id,))
            employee = cursor.fetchone()

            if employee is None:
                # Employee does not exist
                error = "Employee ID does not exist."
                cursor.close()
                conn.close()
                return render_template('delete_employee.html', error=error)

            # Employee exists, now delete it
            cursor.execute("DELETE FROM employee WHERE Employee_id = %s", (employee_id,))
            conn.commit()

            success = "Employee deleted successfully."
            cursor.close()
            conn.close()
            return render_template('delete_employee.html', success=success)

        except Exception as e:
            conn.rollback()
            error = f"Error deleting employee: {str(e)}"
            cursor.close()
            conn.close()
            return render_template('delete_employee.html', error=error)

    return render_template('delete_employee.html')



@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        # Get data from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        salary = request.form['salary']
        gate_number = request.form['gate_number']
        runway_number = request.form['runway_number']

        # Validate inputs to adhere to the check constraint
        if gate_number and runway_number:
            error = "You can only provide either Gate Number or Runway Number, not both."
            return render_template('add_employee.html', error=error)
        if not gate_number and not runway_number:
            error = "You must provide either Gate Number or Runway Number."
            return render_template('add_employee.html', error=error)

        # Database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Validate Gate Number or Runway Number exists
        if gate_number:
            cursor.execute("SELECT * FROM gate WHERE Gate_No = %s", (gate_number,))
            gate = cursor.fetchone()
            if not gate:
                error = "Invalid Gate Number."
                cursor.close()
                conn.close()
                return render_template('add_employee.html', error=error)
            runway_number = None  # Ensure runway is NULL if gate is provided
        elif runway_number:
            cursor.execute("SELECT * FROM runway WHERE Runway_No = %s", (runway_number,))
            runway = cursor.fetchone()
            if not runway:
                error = "Invalid Runway Number."
                cursor.close()
                conn.close()
                return render_template('add_employee.html', error=error)
            gate_number = None  # Ensure gate is NULL if runway is provided

        # Insert the employee data into the 'employee' table
        try:
            cursor.execute("""
                INSERT INTO employee (F_Name, L_Name, Salary, G_No, R_No)
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, salary, gate_number, runway_number))
            conn.commit()
            success = "Employee added successfully."
            cursor.close()
            conn.close()
            return render_template('add_employee.html', success=success)

        except Exception as e:
            conn.rollback()
            error = f"Error adding employee: {str(e)}"
            cursor.close()
            conn.close()
            return render_template('add_employee.html', error=error)

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
