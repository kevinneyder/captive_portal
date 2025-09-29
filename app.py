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

# -----------------------
# Rutas
# -----------------------

@app.route('/')
def portal():
    return render_template('portal.html')

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
        
        # Redirección después de guardar
        return '''
        <script>
            // Primero libera el acceso WiFi
            window.location.href = "http://connectivitycheck.gstatic.com/generate_204";
            // Luego redirige a Google
            setTimeout(function() {
                window.location.href = "https://www.google.com";
            }, 100);
        </script>
        '''
    
    except Exception as e:
        return f"Error: {str(e)}", 500

# Ruta para UniFi captive portal
@app.route('/guest/s/default/')
def unifi_guest():
    """
    Simula la ruta que UniFi espera.
    Los parámetros (id, ap, url, ssid) se reciben por querystring.
    """
    client_id = request.args.get("id")
    ap_mac = request.args.get("ap")
    redirect_url = request.args.get("url", "https://www.google.com")
    ssid = request.args.get("ssid")

    # Aquí podrías registrar datos en logs o BD si lo necesitas
    print(f"UniFi request: id={client_id}, ap={ap_mac}, ssid={ssid}, url={redirect_url}")

    # Mostrar portal.html pero manteniendo el redirect_url
    return render_template("portal.html", redirect_url=redirect_url)

# -----------------------
# Inicialización
# -----------------------
if __name__ == '__main__':
    init_excel()
    app.run(host='0.0.0.0', port=5000, debug=True)
