from flask import Flask,render_template,request,redirect,url_for,session
import pymysql
import db
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key="123456"

@app.route('/')
def home():
    return render_template('login_restaurant.html')

@app.route('/dashboard')
def dashboard():
    return "Bienvenido al dashboard"

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            sql = "SELECT * FROM restaurant WHERE email=%s"
            cursor.execute(sql, (email,))
            restaurant = cursor.fetchone()
            conexion.close()

        if restaurant and check_password_hash(restaurant['password'], password):
            session['restaurant_id'] = restaurant['restaurant_id']
            session['restaurant_name'] = restaurant['name']
            return redirect(url_for('dashboard'))
        else:
            return "Credenciales inválidas. Por favor, revisa tu correo y contraseña."
    except Exception as e:
            return f"Ha ocurrido un error en la base de datos: {e}" 
 
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        capacity = int(request.form['capacity'])
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        phone = request.form['phone']
        address = request.form['address']
        
        try:
            conexion = db.get_connection()
            with conexion.cursor() as cursor:
                sql = "INSERT INTO restaurant (name, email, password,address,capacity, phone_number) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, email, hashed_password, address, capacity, phone))
                conexion.commit()
            conexion.close()
            return redirect(url_for('home'))
        except Exception as e:
            return f"Ha ocurrido un error en la base de datos: {e}"
    return render_template('register_restaurant.html')

if __name__ == '__main__':
    app.run(debug=True,port=80)

