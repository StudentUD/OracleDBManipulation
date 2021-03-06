from flask import Flask,render_template, request, redirect, url_for, session 
from flask import  session # debo indicar app.secret_key ="bases2"

from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from forms import SignupForm, PostForm
#from flask_login import login_required, current_user
import manager

# oracle nombre de host localhost 
# pprt 1521
# sid xe

app = Flask(__name__)
api = Api(app)
app.secret_key ="bases2"
#app.permanent_session_lifetime = timedelta(minutes=5)

# Ruta inicial
@app.route("/")
def index():
    return render_template("index.html")

# Verifica el estado actual de la  BD
@app.route("/status")
def conexion():
    return manager.verify_satus() 

# Gestiona el login y genera URL de los diferentes cargos
@app.route("/login", methods=["POST"])
def login():
    error = None
    manager.test(request)
    if request.method == 'POST': 
        d = manager.verify_login(request.form['user'], request.form['password'])

        session['id']=request.form['password']
        session['user']=request.form['user']
        session['password']=request.form['password']
        if d['rows']!=[]:
            user = d['rows'][0]

            first_name,last_name,title=user   
            session['first_name']=first_name
            session['last_name']=last_name


            page = generate_route(title)
            manager.create_user_db(session['id'],session['password'],page)

            page = generate_route(title)
            return redirect(url_for(page))
        else:
            error = 'Verifique usuario o contrasenia '
    return render_template('/index.html',error=error)

# Cargos
## Representante de ventas
@app.route("/sales_representative", methods=["GET"])
def sales_representative():
    data =  manager.get_list_of_products(get_credential())
    sales_rep = {"id":session["id"],"first_name":session["first_name"], "last_name": session["last_name"]}
    return render_template('/roles/sales_representative.html', page_name='Lista de poductos',table = data, sales_rep = sales_rep)

## Administrador de bodega
@app.route("/warehouse_manager")
def warehouse_manager():
    data = manager.get_inventary(get_credential())
    return render_template('/roles/warehouse_manager.html', table = data)

## Administrador de usuario
@app.route("/user_administrator", methods = ['GET', 'POST'])
def user_administrator():
    rv = []
    if request.method == 'POST':
        rv = [request.form.getlist('rv')]
        rv.append(request.form.getlist('ab'))
        rv.append(request.form.getlist('vprh'))
        manager.asignar_rol(rv)
    return render_template('/roles/user_administrator.html', rol1 = rv  )

## Vicepresidente de recursos Humanos
@app.route("/vprh", methods=["GET"])
def vprh():
    return render_template('.html')
  
# Registro
@app.route("/registro")
def registro():
    return render_template('/registro.html')


#@app.route('/list_clients',methods=["POST","GET"])
#@app.route('/list_clients/<int:phone>',methods=["POST","GET"])
#def list_clients():
#    data = manager.get_client_by_phone(phone)
#    return render_template('/roles/sales_clients.html',table= data )


@app.route('/list_clients',methods=["POST","GET"])
def list_clients():
    data = manager.get_clients_lists(get_credential())
    return render_template('/roles/sales_clients.html', page_name = 'Lista de clientes',table= data )

# Funciones
def generate_route(u):
    return u.lower().strip().replace(" ","_")

def get_credential():
    return session["user"]+"/"+session["password"]
    # return {"userdb":session["user"],"password": session["password"]}

# Main
if __name__ == '__main__':
    app.run(debug = True, port =8000)

