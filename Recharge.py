from flask import Flask, render_template, request
import pyodbc
import datetime

app = Flask(__name__)

# ... (other configurations remain unchanged)
# Configure the database connection
server = 'DESKTOP-4GHHQSA\SQLEXPRESS1'
database = 'transit_1'
username = 'kimmy'
password = 'kimmy'
driver = 'ODBC Driver 17 for SQL Server'
# Establish the database connection
conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server +
                      ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transit_1', methods=['GET', 'POST'])
def transit_1():
    expiry = None  # Default expiry value
    if request.method == 'POST':
        serial_no = request.form['serial_no']
        recharge_amount = request.form['recharge_amount']
        monthly_pass = request.form.get('monthly_pass')  # Get pass status from form (assuming checkbox or radio button)
        
        cursor = conn.cursor()
        cursor.execute("SELECT balance, expiry FROM transit_1 WHERE serial_no = ?", serial_no)
        row = cursor.fetchone()
        
        if row:
            balance, expiry = row[0], row[1]
            new_balance = balance + float(recharge_amount) if recharge_amount else balance  # Keep the existing balance if no recharge amount specified
            
            cursor.execute("UPDATE transit_1 SET balance = ? WHERE serial_no = ?", new_balance, serial_no)
            
            if monthly_pass == '1':  # If pass is enabled
                expiry = datetime.datetime.now() + datetime.timedelta(days=30)  # Set expiry to 30 days from now
                cursor.execute("UPDATE transit_1 SET monthly_pass = 1, expiry = ? WHERE serial_no = ?", expiry, serial_no)
            
            conn.commit()
            return render_template('transit_1.html', serial_no=serial_no, balance=new_balance, 
                                   monthly_pass=monthly_pass, expiry=expiry)
        else:
            return "Serial number not found!"

    from flask import Flask, render_template, request
import pyodbc
import datetime

app = Flask(__name__)

# ... (other configurations remain unchanged)
# Configure the database connection
server = 'DESKTOP-4GHHQSA\SQLEXPRESS1'
database = 'transit_1'
username = 'kimmy'
password = 'kimmy'
driver = 'ODBC Driver 17 for SQL Server'
# Establish the database connection
conn = pyodbc.connect('DRIVER=' + driver +
                      ';SERVER=' + server +
                      ';DATABASE=' + database +
                      ';UID=' + username +
                      ';PWD=' + password)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/transit_1', methods=['GET', 'POST'])
def transit_1():
    expiry = None  # Default expiry value
    if request.method == 'POST':
        serial_no = request.form['serial_no']
        recharge_amount = request.form['recharge_amount']
        monthly_pass = request.form.get('monthly_pass')  # Get pass status from form (assuming checkbox or radio button)
        
        cursor = conn.cursor()
        cursor.execute("SELECT balance, expiry FROM transit_1 WHERE serial_no = ?", serial_no)
        row = cursor.fetchone()
        
        if row:
            balance, expiry = row[0], row[1]
            new_balance = balance + float(recharge_amount) if recharge_amount else balance  # Keep the existing balance if no recharge amount specified
            
            cursor.execute("UPDATE transit_1 SET balance = ? WHERE serial_no = ?", new_balance, serial_no)
            
            if monthly_pass == '1':  # If pass is enabled
                expiry = datetime.datetime.now() + datetime.timedelta(days=30)  # Set expiry to 30 days from now
                cursor.execute("UPDATE transit_1 SET monthly_pass = 1, expiry = ? WHERE serial_no = ?", expiry, serial_no)
            
            conn.commit()
            # Pass recharge details to the HTML template after a successful recharge
            return render_template('transit_1.html', serial_no=serial_no, balance=new_balance, 
                                   monthly_pass=monthly_pass, expiry=expiry)
        else:
            return "Serial number not found!"

    return render_template('transit_1.html')

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
