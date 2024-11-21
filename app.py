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

@app.route('/sign_up_employee')
def sign_up_employee():
    return render_template('employee_sign_up.html')

@app.route('/sign_up_pass')
def sign_up_pass():
    return render_template('pass_sign_up.html')

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
        phone_numbers = request.form.getlist('phone_number')  # Get multiple phone numbers as a list

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Insert passenger details
            query = """
            INSERT INTO passenger (F_Name, L_Name, Gender, Nationality, Passport_No)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (first_name, last_name, gender, nationality, passport_number))
            conn.commit()

            # Get the auto-generated passenger ID
            passenger_id = cursor.lastrowid

            # Insert each contact into the passenger-contacts table
            phone_query = """
            INSERT INTO `passenger-contacts` (Passenger_id, Contact)
            VALUES (%s, %s)
            """
            for phone_number in phone_numbers:
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
        SELECT Flight_Date, Booking_Status, Flight_id, Airline_id, Passenger_id
        FROM tickets
        WHERE Passenger_id = %s
        """

        #In the query it should be Flight_instance_id instead of Flight_id
        #add changes to mysql tables accordingly

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
            wait_duration =  departure_datetime - arrival_datetime

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
        phone_numbers = request.form.getlist('phone_number')  # Get multiple phone numbers as a list

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

        try:
            # Validate Gate or Runway
            if gate_number:
                cursor.execute("SELECT * FROM gate WHERE Gate_No = %s", (gate_number,))
                if not cursor.fetchone():
                    raise ValueError("Invalid Gate Number.")
                runway_number = None  # Ensure runway is NULL if gate is provided
            elif runway_number:
                cursor.execute("SELECT * FROM runway WHERE Runway_No = %s", (runway_number,))
                if not cursor.fetchone():
                    raise ValueError("Invalid Runway Number.")
                gate_number = None  # Ensure gate is NULL if runway is provided

            # Insert employee data
            cursor.execute("""
                INSERT INTO employee (F_Name, L_Name, Salary, G_No, R_No)
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, salary, gate_number, runway_number))
            conn.commit()

            # Get the generated Employee ID
            employee_id = cursor.lastrowid

            # Insert each contact into the employee-contacts table
            contact_query = """
            INSERT INTO `employee-contacts` (Employee_id, Contact)
            VALUES (%s, %s)
            """
            for phone_number in phone_numbers:
                cursor.execute(contact_query, (employee_id, phone_number))
            conn.commit()

            success = "Employee added successfully."
            cursor.close()
            conn.close()
            return render_template('add_employee.html', success=success)

        except ValueError as ve:
            conn.rollback()
            error = str(ve)
            cursor.close()
            conn.close()
            return render_template('add_employee.html', error=error)

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

@app.route('/update_gate_runway', methods=['GET', 'POST'])
def update_gate_runway():
    if request.method == 'POST':
        # Get data from the form
        employee_id = request.form['employee-id']
        update_type = request.form['update-type']
        new_number = request.form['new-number']

        # Validate inputs
        if not employee_id.isdigit() or not new_number.isdigit():
            error = "Employee ID and Gate/Runway Number must be numeric."
            return render_template('update_gate_runway.html', error=error)

        employee_id = int(employee_id)
        new_number = int(new_number)

        if update_type not in ['gate', 'runway']:
            error = "Invalid update type. Please select 'Gate' or 'Runway'."
            return render_template('update_gate_runway.html', error=error)

        # Database connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Call the stored procedure
            cursor.callproc('UpdateEmployeeGateRunway', (employee_id, update_type, new_number))
            conn.commit()

            # Success message
            success = "Employee record updated successfully."
            cursor.close()
            conn.close()
            return render_template('update_gate_runway.html', success=success)

        except mysql.connector.Error as err:
            # Rollback and handle errors
            conn.rollback()
            error = f"{err.msg}"
            cursor.close()
            conn.close()
            return render_template('update_gate_runway.html', error=error)

    return render_template('update_gate_runway.html')



@app.route('/view_reports')
def view_reports():
    return render_template('View_Report.html')

@app.route('/top_employees')
def top_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT F_name, L_name, salary FROM employee ORDER BY salary DESC LIMIT 10")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('top_employees.html', employees=employees)

@app.route('/top_airlines')
def top_airlines():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("CALL GetTopAirlines()")  # Use `execute()` for SELECT-producing procedures
        result = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        result = []
    finally:
        cursor.close()
        conn.close()
    return render_template('top_airlines.html', airlines=result)


@app.route('/top_passengers')
def top_passengers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("CALL GetTopPassengers()")  # Use execute for procedures with SELECT
        result = cursor.fetchall()
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        result = []
    finally:
        cursor.close()
        conn.close()
    return render_template('top_passengers.html', passengers=result)


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


@app.route('/book_ticket')
def book_ticket():
    return render_template('book_ticket.html')

@app.route('/check_flights', methods=['POST'])
def check_available_flights():
    flight_date = request.form.get('flight-date')
    destination_city = request.form.get('destination-id')

    if not flight_date or not destination_city:
        return render_template('available_flights.html', error="Please provide both date and destination.")

    full_datetime = f"{flight_date} 00:00:00"
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.callproc('GetAvailableFlights', (full_datetime, destination_city))
        for result in cursor.stored_results():
            flights = result.fetchall()

        if not flights:
            return render_template(
                'available_flights.html',
                error="No flights found for the selected date and destination."
            )

        return render_template(
            'available_flights.html',
            flights=flights,
            flight_date=flight_date,
            destination_city=destination_city
        )

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('available_flights.html', error="An error occurred while fetching flights.")

    finally:
        cursor.close()
        conn.close()


@app.route('/book_tickets', methods=['POST'])
def book_tickets():
    # Extract form data
    passenger_id = request.form.get('passenger-id')
    flight_instance_id = request.form.get('flight-instance-id')

    if not passenger_id or not flight_instance_id:
        return render_template(
            'available_flights.html',
            flights=[],
            error="Both Passenger ID and Flight Instance ID are required."
        )

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Call the stored procedure
        cursor.callproc('BookTicket', (int(passenger_id), int(flight_instance_id)))
        conn.commit()

        success = "Ticket successfully booked!"
        return render_template('available_flights.html', success=success, flights=[])

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        error = f"An error occurred while booking the ticket: {err}"
        return render_template('available_flights.html', error=error, flights=[])

    finally:
        cursor.close()
        conn.close()





# =======================
# App Entry Point
# =======================

if __name__ == '__main__':
    app.run(debug=True)
