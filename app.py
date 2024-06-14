from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import MySQLdb.cursors
import re
from routes import CategoriasRoutes, ComprasRoutes, ClientesRoutes, ProveedoresRoutes, EmpleadosRoutes, InventarioRoutes, VentasRoutes, UsuariosRoutes, ProductosRoutes

app = Flask(__name__)
app.config.from_object('config.Config')

mysql = MySQL(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# Registro de las rutas
categorias_routes = CategoriasRoutes(app, mysql)
compras_routes = ComprasRoutes(app, mysql)
clientes_routes = ClientesRoutes(app, mysql)
proveedores_routes = ProveedoresRoutes(app, mysql)
empleados_routes = EmpleadosRoutes(app, mysql)
inventario_routes = InventarioRoutes(app, mysql)
ventas_routes = VentasRoutes(app, mysql)
usuarios_routes = UsuariosRoutes(app, mysql)
productos_Routes = ProductosRoutes(app, mysql)



@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'correo' in request.form and 'contraseña' in request.form:
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            flash('Correo electrónico inválido', 'danger')
            return render_template('login.html')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s', (correo,))
        usuario = cursor.fetchone()

        if usuario and bcrypt.check_password_hash(usuario['contraseña'], contraseña):
            flash('Has iniciado sesión con éxito', 'success')
            if usuario['id_rol'] == 1:  # Administrador
                return redirect(url_for('index'))
            elif usuario['id_rol'] == 2:  # EmpleadoCompras
                return redirect(url_for('indexCompras'))
            
            elif usuario['id_rol'] == 3: #EmpleadoVentas
                return redirect(url_for('indexVentas'))
            
            elif usuario['id_rol'] == 4: #EmpleadoInventario
                return redirect(url_for('indexInventario'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'correo' in request.form and 'contraseña' in request.form and 'nombre_usuario' in request.form and 'jefe_contraseña' in request.form:
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        nombre_usuario = request.form['nombre_usuario']
        jefe_contraseña = request.form['jefe_contraseña']

        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            flash('Correo electrónico inválido', 'danger')
            return render_template('login.html')

        if jefe_contraseña != 'Bryan1234':
            flash('Contraseña del jefe incorrecta', 'danger')
            return redirect(url_for('register'))

        if not validate_password(contraseña):
            flash('La contraseña debe tener entre 8 y 12 caracteres y contener al menos una letra mayúscula', 'danger')
        else:
            id_estado_usuario = 1
            id_rol = 4

            contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')

            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO usuarios (contraseña, correo, fecha_registro, nombre_usuario, id_estado_usuario, id_rol) VALUES (%s, %s, NOW(), %s, %s, %s)', 
                           (contraseña_hash, correo, nombre_usuario, id_estado_usuario, id_rol))
            mysql.connection.commit()
            flash('Usuario registrado con éxito', 'success')
            return redirect(url_for('login'))

    return render_template('login.html')

def validate_password(password):
    if len(password) < 8 or len(password) > 12:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    return True

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/error400')
def error400():
    return render_template('error400.html')

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST' and 'correo' in request.form:
        correo = request.form['correo']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s', (correo,))
        usuario = cursor.fetchone()

        if usuario:
            return render_template('login.html', show_reset_password_modal=True, correo=correo)
        else:
            flash('No se encontró una cuenta con ese correo electrónico', 'danger')

    return render_template('login.html')

@app.route('/reset_password/<correo>', methods=['GET', 'POST'])
def reset_password(correo):
    if request.method == 'POST' and 'contraseña' in request.form:
        contraseña = request.form['contraseña']
        if not validate_password(contraseña):
            flash('La contraseña debe tener entre 8 y 12 caracteres y contener al menos una letra mayúscula', 'danger')
        else:
            contraseña_hash = bcrypt.generate_password_hash(contraseña).decode('utf-8')
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE usuarios SET contraseña = %s WHERE correo = %s', (contraseña_hash, correo))
            mysql.connection.commit()
            flash('Tu contraseña ha sido actualizada', 'success')
            return redirect(url_for('login'))

    return render_template('login.html', show_reset_password_modal=True, correo=correo)

if __name__ == '__main__':
    app.run(debug=True)
