from flask import Flask,render_template,request,redirect,url_for,session
import pymysql
import db


app = Flask(__name__)
app.secret_key="123456"

@app.route('/')
def elegir():
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            consulta = "SELECT * FROM restaurant"
            cursor.execute(consulta)
            resultados = cursor.fetchall()

            #nombres_restaurantes = [registro['name'] for registro in resultados]
            #id_restaurantes = [registro['customer_id'] for registro in resultados]
            session['ID_restaurante'] = 


            return render_template("cliente_elegir02.html", restaurantes=resultados)
            #return render_template("cliente_elegir.html", restaurantes=nombres_restaurantes,  IDrestaurantes=id_restaurantes)
            #return render_template("cliente_elegir.html", restaurantes=nombres_restaurantes)
            #return render_template("cliente_elegir.html",restaurantes=resultados)
    except Exception as e:  
        print("Ocurrió un error al conectar a la bbdd: ", e)
    finally:    
        conexion.close()
        print("Conexión cerrada")   


@app.route('/elegido',methods=['POST'])
def login():
    #obtener los datos del formulario
    id_restaurante = request.form['restaurante'] 
    fecha = request.form['fecha']
    numero_comensales = request.form['comensales']
    cliente = request.form['id_cliente']
    #creamos la conexion
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            #creamos la consulta
            consulta = "SELECT * FROM restaurant WHERE restaurant_id = %s" # AND password = %s"
            datos = (id_restaurante)  #username,password)
            cursor.execute(consulta,datos)
            resultados = cursor.fetchone()
            if(resultados['stock'] - int(numero_comensales) >= 0):
                a = "habían " + str(resultados['stock'])
                b = "restando " + numero_comensales
                c = "quedan " + str(resultados['stock'] - int(numero_comensales))
                print("habían " + str(resultados['stock']))
                print("restando " + numero_comensales)
                print("quedan " + str(resultados['stock'] - int(numero_comensales)))






                #guardar datos en session
                #session['username'] = username
                return a + b + c #render_template("cliente_elegir02.html",mensaje="Si que hay")
            else:
                return render_template("cliente_elegir02.html",mensaje="solo hay " + str(resultados['stock']) + "de esa verga")
    except Exception as e:
        print("Ocurrió un error al conectar a la bbdd: ", e)
    finally:    
        conexion.close()
        print("Conexión cerrada") 
          
    
@app.route('/elegido02',methods=['POST'])
def login666():
    print("Conexión cerrada")  
    #obtener los datos del formulario
    username = request.form['restaurante'] 
    password = request.form['fecha']
    password000 = request.form['comensales']
    #creamos la conexion
    #conexion = db.get_connection()
    #print (username) #, password, password000) 
    #exit()
    return username + " --- " + password + " --- " + password000 

@app.route('/elegido03',methods=['POST'])
def login777():
    #obtener los datos del formulario
    id_restaurante = request.form['restaurante'] 
    fecha = request.form['fecha']
    numero_comensales = request.form['comensales']
    #creamos la conexion
    conexion = db.get_connection()
    try:
        with conexion.cursor() as cursor:
            #creamos la consulta
            consulta = "SELECT * FROM product WHERE product_id = %s" # AND password = %s"
            datos = (id_restaurante)  #username,password)
            cursor.execute(consulta,datos)
            resultados = cursor.fetchone()
            if(resultados):
                #guardar datos en session
                #session['username'] = username
                
                return resultados['name'] + " --- " + str(resultados['stock'])

                


            else:
                return "Usuario o contraseña incorrecta"
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