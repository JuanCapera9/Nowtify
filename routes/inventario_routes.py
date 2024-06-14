from flask import render_template, request, redirect, url_for, flash

class InventarioRoutes:
    def __init__(self, app, mysql):
        self.app = app
        self.mysql = mysql
        self.add_routes()
        self.app.route('/indexInventario')(self.indexInventario)
    def add_routes(self):
        @self.app.route('/inventario')
        def inventario():
            cur = self.mysql.connection.cursor()
            cur.execute("""SELECT inv.id_inventario,
                        inv.cantidad,
                        inv.estado,
                        inv.fecha_adquisicion,
                        inv.notas,
                        prod.nombre AS NombreProducto
                        FROM inventario inv 
                        JOIN producto prod ON inv.referencia = prod.referencia""")
            data = cur.fetchall()
            cur.execute('SELECT referencia, nombre FROM producto')
            producto = cur.fetchall()
            return render_template('inventario.html', inventario=data, producto = producto)

        @self.app.route('/add_inventario', methods=['POST'])
        def add_inventario():
            if request.method == 'POST':
                cantidad = request.form['cantidad']
                estado = request.form['estado']
                fecha_adquisicion = request.form['fecha_adquisicion']
                notas = request.form['notas']
                referencia = request.form['referencia']

                cur = self.mysql.connection.cursor()
                cur.execute('INSERT INTO inventario (cantidad, estado, fecha_adquisicion, notas, referencia) VALUES (%s, %s, %s, %s, %s)', 
                            (cantidad, estado, fecha_adquisicion, notas, referencia))
                self.mysql.connection.commit()
                flash('Registro de inventario agregado exitosamente.', 'success')
                return redirect(url_for('inventario'))

        @self.app.route('/edit_inventario/<id_inventario>')
        def edit_inventario(id_inventario):
            cur = self.mysql.connection.cursor()
            cur.execute('SELECT * FROM inventario WHERE id_inventario = %s', (id_inventario,))
            data = cur.fetchone()
            return render_template('edit_inventario.html', inventario=data)

        @self.app.route('/update_inventario/<id_inventario>', methods=['POST'])
        def update_inventario(id_inventario):
            if request.method == 'POST':
                cantidad = request.form['cantidad']
                estado = request.form['estado']
                fecha_adquisicion = request.form['fecha_adquisicion']
                notas = request.form['notas']
                referencia = request.form['referencia']

                cur = self.mysql.connection.cursor()
                cur.execute("""
                    UPDATE inventario
                    SET cantidad = %s,
                        estado = %s,
                        fecha_adquisicion = %s,
                        notas = %s,
                        referencia = %s
                    WHERE id_inventario = %s
                """, (cantidad, estado, fecha_adquisicion, notas, referencia, id_inventario))
                self.mysql.connection.commit()
                flash('Registro de inventario actualizado exitosamente.', 'success')
                return redirect(url_for('inventario'))
        
    def indexInventario(self):
        return render_template('indexInventario.html')