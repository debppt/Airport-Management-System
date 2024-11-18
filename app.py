from flask import Flask, render_template, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__, template_folder='.')
CORS(app) 

# Connect to MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='local_host@12',
        database='airport'
    )
@app.route('/')
def home():
    return render_template('main.html')   

#main page
@app.route('/login_passenger')
def about_page():
    return render_template('pass_sign_in.html')

#admin sign in
@app.route('/login_as_admin')
def login_as_admin():
    return render_template('admin_sign_in.html')

#employee login in
@app.route('/login_as_employee')
def login_as_employee():
    return render_template('employee_sign_in.html')

#pass sign in
@app.route('/sign_up_pass')
def sign_up_pass():
    return render_template('pass_sign_up.html')

#employee sign up
@app.route('/sign_up_employee')
def sign_up_employee():
    return render_template('employee_sign_up.html')

#admin landing page
@app.route('/admin_landing_page')
def admin_landing_page():
    return render_template('admin_landing_page.html')

#add airline page
@app.route('/add_airline_page')
def add_airline_page():
    return render_template('add_airline.html')

#taking input for add airline

#add flight details
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




















@app.route('/see_tickets')
def see_ticket():
    return render_template('see_ticket.html')

@app.route('/view_tickets_action', methods=['GET', 'POST'])
def view_tickets_form():
    if request.method == 'POST':
        passenger_id = request.form['passenger-id']
        
        # Get tickets for the given Passenger ID
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

if __name__ == '__main__':
    app.run(debug=True)
