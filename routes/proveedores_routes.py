from flask import render_template, request, redirect, url_for, flash

class ProveedoresRoutes:
    def __init__(self, app, mysql):
        self.app = app
        self.mysql = mysql
        self.add_routes()

    def add_routes(self):
        @self.app.route('/proveedores')
        def proveedores():
            cur = self.mysql.connection.cursor()
            cur.execute('SELECT * FROM proveedores')
            data = cur.fetchall()
            return render_template('proveedores.html', proveedores=data)

        @self.app.route('/add_proveedor', methods=['POST'])
        def add_proveedor():
            if request.method == 'POST':
                apellido = request.form['apellido']
                ciudad = request.form['ciudad']
                contacto = request.form['contacto']
                direccion = request.form['direccion']
                email = request.form['email']
                nombre = request.form['nombre']
                pais = request.form['pais']
                telefono = request.form['telefono']
                cur = self.mysql.connection.cursor()
                cur.execute(
                    'INSERT INTO proveedores (apellido, ciudad, contacto, direccion, email, nombre, pais, telefono) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    (apellido, ciudad, contacto, direccion, email, nombre, pais, telefono))
                self.mysql.connection.commit()
                flash('Proveedor agregado exitosamente.', 'success')
            return redirect(url_for('proveedores'))

        @self.app.route('/edit_proveedor/<id_proveedor>')
        def get_proveedor(id_proveedor):
            cur = self.mysql.connection.cursor()
            cur.execute('SELECT * FROM proveedores WHERE id_proveedor = %s', (id_proveedor,))
            data = cur.fetchone()
            return render_template('edit_proveedor.html', proveedor=data)

        @self.app.route('/update_proveedor/<id_proveedor>', methods=['POST'])
        def update_proveedor(id_proveedor):
            if request.method == 'POST':
                apellido = request.form['apellido']
                ciudad = request.form['ciudad']
                contacto = request.form['contacto']
                direccion = request.form['direccion']
                email = request.form['email']
                nombre = request.form['nombre']
                pais = request.form['pais']
                telefono = request.form['telefono']

                cur = self.mysql.connection.cursor()
                cur.execute("""
                    UPDATE proveedores
                    SET apellido = %s,
                        ciudad = %s,
                        contacto = %s,
                        direccion = %s,
                        email = %s,
                        nombre = %s,
                        pais = %s,
                        telefono = %s
                    WHERE id_proveedor = %s
                """, (apellido, ciudad, contacto, direccion, email, nombre, pais, telefono, id_proveedor))
                self.mysql.connection.commit()
                flash('Proveedor actualizado exitosamente.', 'success')
            return redirect(url_for('proveedores'))
