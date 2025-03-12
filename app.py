from flask import Flask,render_template,request,redirect,url_for,session
import pymysql
import db


app = Flask(__name__)
app.secret_key="123456"

@app.route('/')
def home():
    return render_template('home.html')

    # Ruta para gestionar las reservas y asignar mesas
@app.route('/manage_reservations', methods=['GET', 'POST'])
def manage_reservations():
    #if 'restaurant_id' not in session:
    #    return redirect(url_for('login'))
    
    
    #restaurant_id = session['restaurant_id']
    connection = db.get_connection()
    cursor = connection.cursor()

    # Si el formulario se envía (para confirmar o rechazar la reserva)
    if request.method == 'POST':
        reserve_id = request.form['reserve_id']
        action = request.form['action']
        table_id = request.form.get('table_id', None)  # Mesa asignada (puede ser opcional en algunos casos)
        
        if action == 'confirm':
            cursor.execute('''
                UPDATE reserve
                SET table_id = %s, status = 'confirmed'
                WHERE reserve_id = %s AND restaurant_id = %s
            ''', (table_id, reserve_id, restaurant_id))
        elif action == 'reject':
            cursor.execute('''
                UPDATE reserve
                SET status = 'rejected'
                WHERE reserve_id = %s AND restaurant_id = %s
            ''', (reserve_id, restaurant_id))
        
        connection.commit()

    # Obtener todas las reservas del restaurante
    cursor.execute('''
        SELECT r.reserve_id, r.date, r.address, r.diner, r.reviews, r.status, c.name as customer_name, r.table_id
        FROM reserve r
        JOIN customer c ON r.customer_id = c.customer_id
        WHERE r.restaurant_id = %s
    ''', (1,))
    reservations = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('manage_reservations.html', reservations=reservations)
if __name__ == '__main__':    
    app.run(debug=True,port=80)