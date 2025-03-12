from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "123456"

# Ruta principal (Home)
@app.route('/')
def home():
    return render_template('home.html')

# Ruta para registro de clientes
@app.route('/registro_clientes', methods=['GET', 'POST'])
def registro_clientes():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        password = request.form['password']
        repetir_password = request.form['repetir_password']

        if password == repetir_password:
            hashed_password = generate_password_hash(password)

            try:
                conexion = db.get_connection()
                with conexion.cursor() as cursor:
                    sql = "INSERT INTO customer (name, email, password, phone_number) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (nombre, email, hashed_password, telefono))
                    conexion.commit()
                conexion.close()
                return redirect(url_for('login_clientes'))
            except Exception as e:
                return f"Ha ocurrido un error en la base de datos: {e}"
        else:
            return "Las contraseñas no coinciden"
    return render_template('registro_clientes.html')

# Ruta para login de clientes
@app.route('/login_clientes', methods=['GET', 'POST'])
def login_clientes():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conexion = db.get_connection()
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM customer WHERE email=%s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()
                conexion.close()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['customer_id']
                session['user_name'] = user['name']
                return redirect(url_for('dashboard'))
            else:
                return "Credenciales inválidas. Por favor, revisa tu correo y contraseña."
        except Exception as e:
            return f"Ha ocurrido un error en la base de datos: {e}"
    return render_template('login_clientes.html')

# Ruta para el dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f"¡Bienvenido, {session['user_name']}!"
    else:
        return redirect(url_for('login_clientes'))

# Ruta para logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=80)




