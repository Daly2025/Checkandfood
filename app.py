from flask import Flask,render_template,request,redirect,url_for,session
import pymysql
import db


app = Flask(__name__)
app.secret_key="123456"

@app.route('/')
def home():
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            consulta = "SELECT * FROM customer"
            cursor.execute(consulta)
            resultados = cursor.fetchall()

            nombres_restaurantes = [registro['name'] for registro in resultados]
            id_restaurantes = [registro['customer_id'] for registro in resultados]
            
            return render_template("cliente_elegir.html", restaurantes=resultados)
            #return render_template("cliente_elegir.html", restaurantes=nombres_restaurantes,  IDrestaurantes=id_restaurantes)
            #return render_template("cliente_elegir.html", restaurantes=nombres_restaurantes)
            #return render_template("cliente_elegir.html",restaurantes=resultados)
    except Exception as e:  
        print("Ocurrió un error al conectar a la bbdd: ", e)
    finally:    
        conexion.close()
        print("Conexión cerrada")   


# @app.route('/', methods=['GET', 'POST'])
# def home():
#     return "hola mundo"



if __name__ == '__main__':    
    app.run(debug=True,port=5000)