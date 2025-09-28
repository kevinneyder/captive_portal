from flask import Flask, request, render_template
from openpyxl import Workbook, load_workbook
from datetime import datetime
import os

app = Flask(__name__)

EXCEL_FILE = "happy_tea_captive_portal.xlsx"

def init_excel():
    if not os.path.exists(EXCEL_FILE):
        wb = Workbook()
        ws = wb.active
        ws.append(["Full Name", "Birthdate", "Phone Number", "Favorite Drink", "Register Date"])
        wb.save(EXCEL_FILE)

@app.route('/')
def portal():
    return render_template('portal.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/save', methods=['POST'])
def save():
    try:
        name = request.form['name']
        birthdate = request.form['birthdate']
        phoneNumber = request.form['phone']
        favoriteDrink = request.form['drink']
        
        if os.path.exists(EXCEL_FILE):
            wb = load_workbook(EXCEL_FILE)
            ws = wb.active
        else:
            wb = Workbook()
            ws = wb.active
            ws.append(["Full Name", "Birthdate", "Phone Number", "Favorite Drink", "Register Date"])
        
        ws.append([name, birthdate, phoneNumber, favoriteDrink, datetime.now().strftime("%Y-%m-%d %H:%M")])
        
        wb.save(EXCEL_FILE)
        
        return '''
        <script>
            // Primero libera el acceso WiFi
            window.location.href = "http://connectivitycheck.gstatic.com/generate_204";
            // Luego redirige a Google (se ejecutará después de la liberación)
            setTimeout(function() {
                window.location.href = "https://www.google.com";
            }, 100);
        </script>
        '''
    
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    init_excel()
    app.run(host='0.0.0.0', port=5000, debug=True)