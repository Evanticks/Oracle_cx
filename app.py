
# Importamos las funciones del sistema, el módulo que conecta python con oracle y flask para la aplicación en cuestión.
import os
import sys
import cx_Oracle
from flask import Flask, render_template, abort, request, redirect, url_for, abort
from flask import Flask

################################################################################
# Esta parte del código es por si se inicia en otro sistema operativo.

if sys.platform.startswith("darwin"):
    cx_Oracle.init_oracle_client(lib_dir=os.environ.get("HOME")+"/instantclient_19_3")
elif sys.platform.startswith("win32"):
    cx_Oracle.init_oracle_client(lib_dir=r"c:\oracle\instantclient_19_8")


# Init_session es una función para una llamada de sesión eficiente.

def init_session(connection, requestedTag_ignored):
    cursor = connection.cursor()
    cursor.execute("""
        ALTER SESSION SET
          TIME_ZONE = 'UTC'
          NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI'""")


def start_pool():

    pool_min = 4
    pool_max = 4
    pool_inc = 0
    pool_gmd = cx_Oracle.SPOOL_ATTRVAL_WAIT

    print("Connecting to", os.environ.get("PYTHON_CONNECTSTRING"))

    pool = cx_Oracle.SessionPool(user='antonio',
                                 password='antonio',
                                 dsn=os.environ.get('192.168.122.20:1521/ORCLCDB'),
                                 min=pool_min,
                                 max=pool_max,
                                 increment=pool_inc,
                                 threaded=True,
                                 getmode=pool_gmd,
                                 sessionCallback=init_session)

    return pool

################################################################################

# Definimos el nombre de la aplicación para flask
app = Flask(__name__)


#Ruta raíz, redigirá al login
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        texto=request.form.get("user")
        print ('texto=',texto)
        texto2=request.form.get("pass")
        print ('texto2=',texto2)
        if texto=='antonio' and texto2=='antonio':
            connection=cx_Oracle.connect(
	        user='antonio',
	        password='antonio',
	        dsn='192.168.122.20:1521/ORCLCDB',
	        encoding='UTF-8')
            cursor = connection.cursor()
            cursor.execute("select * from personaje")
            resultado = cursor.fetchall()
            cursor.execute("select nombre from armas")
            resultado2 = cursor.fetchall()
            cursor.execute("select nombre from tesoro")
            resultado3 = cursor.fetchall()
            return render_template("datos.html",resultado=resultado,resultado2=resultado2,resultado3=resultado3)
        else:
            return redirect(url_for('login'))
    else:
        return render_template("login.html")

#@app.route('/',methods=["GET","POST"])
#def inicio():
#    connection = pool.acquire()
#    cursor = connection.cursor()
#    cursor.execute("select nombre from armas")
#    res = cursor.fetchall()
#    return render_template("index.html",tablas=[res])




### -Programa principal:


if __name__ == '__main__':

 
    pool = start_pool()
    #app.run(port=int(os.environ.get('PORT', '8080')))
    app.run("0.0.0.0",5000,debug=True)