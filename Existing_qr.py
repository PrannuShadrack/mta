from flask import Flask, render_template, request,jsonify
import pyodbc
import qrcode
from io import BytesIO
import datetime
import base64


app = Flask(__name__)

# SSMS database connection details
server = 'DESKTOP-4GHHQSA\SQLEXPRESS1'
database = 'existing_t'
username = 'kimmy'
password = 'kimmy'
driver = 'ODBC Driver 17 for SQL Server'

# Establishing the database connection
conn = pyodbc.connect(
    'DRIVER=' + driver +
    ';SERVER=' + server +
    ';DATABASE=' + database +
    ';UID=' + username +
    ';PWD=' + password
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert_qr', methods=['POST'])
def insert_qr():
    qr_data = request.form.get('qr_data')
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO QR_Tickets (QRCode) VALUES (?)", img_bytes)
    conn.commit()
 
    display_button = '<a href="/display_qr"><button>Display QR Code</button></a>'
    
    return "QR code inserted successfully! " + display_button
    
@app.route('/display_qr')
def display_qr():
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 QRCode FROM QR_Tickets ORDER BY TicketID DESC;")
    qr_image = cursor.fetchone()[0]
    
    return render_template('display_qr.html', qr_image=qr_image)

@app.route('/fetch_qr_code', methods=['GET'])
def fetch_qr_code():
    cursor = conn.cursor()
    cursor.execute ("SELECT TOP 1 QRCode FROM QR_Tickets ORDER BY TicketID DESC;")
    qr_info = cursor.fetchone()
    
    if qr_info:
        generated_time = qr_info[1]
        current_time = datetime.datetime.now()
        time_difference = current_time - generated_time
        
        if time_difference.total_seconds() < 90 * 60:  # Check if within 90 minutes
            return render_template('display_qr.html', qr_info=qr_info)
        else:
            return "QR code has expired."
    else:
        return "No QR code found."



if __name__ == '__main__':
    app.run(debug=True)



