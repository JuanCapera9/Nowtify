from flask import render_template, request, redirect, url_for, flash

class VentasRoutes:
    def __init__(self, app, mysql):
        self.app = app
        self.mysql = mysql
        self.add_routes()
    
    def add_routes(self):
        @self.app.route('/ventas')
        def ventas():
            cur = self.mysql.connection.cursor()
            cur.execute("""SELECT ven.id_venta,
                            ven.fecha_venta,
                            ven.total,
                            CONCAT(cli.nombres, ' ', cli.apellidos) AS nombrecliente
                        FROM ventas ven
                        INNER JOIN clientes cli ON ven.id_cliente = cli.id_cliente""")
            data = cur.fetchall()
            cur.execute('SELECT id_cliente, CONCAT(nombres, " ", apellidos) AS nombre_cliente FROM clientes')
            cliente = cur.fetchall()
            return render_template('indexVentas.html', ventas=data, cliente = cliente)
        @self.app.route('/add_venta', methods=['POST'])
        def add_venta():
            if request.method == 'POST':
                id_cliente = request.form['id_cliente']
                fecha_venta = request.form['fecha_venta']
                total = request.form['total']

                cur = self.mysql.connection.cursor()
                cur.execute('INSERT INTO ventas (id_cliente, fecha_venta, total) VALUES (%s, %s, %s)', 
                            (id_cliente, fecha_venta, total))
                self.mysql.connection.commit()
                flash('Venta agregada exitosamente.', 'success')
                return redirect(url_for('ventas'))

        @self.app.route('/edit_venta/<id_venta>')
        def edit_venta(id_venta):
            cur = self.mysql.connection.cursor()
            cur.execute('SELECT * FROM ventas WHERE id_venta = %s', (id_venta,))
            data = cur.fetchone()

            cur.execute("SELECT CONCAT(nombres, ' ', apellidos) AS nombre_cliente FROM clientes")
            cliente = cur.fetchall()
            return render_template('edit_venta.html', venta=data, cliente=cliente)

        @self.app.route('/update_venta/<id_venta>', methods=['POST'])
        def update_venta(id_venta):
            if request.method == 'POST':
                id_cliente = request.form['id_cliente']
                fecha_venta = request.form['fecha_venta']
                total = request.form['total']

                cur = self.mysql.connection.cursor()
                cur.execute("""
                    UPDATE ventas
                    SET id_cliente = %s,
                        fecha_venta = %s,
                        total = %s
                    WHERE id_venta = %s
                """, (id_cliente, fecha_venta, total, id_venta))
                self.mysql.connection.commit()
                flash('Venta actualizada exitosamente.', 'success')
                return redirect(url_for('ventas'))
            
        @self.app.route('/indexVentas')
        def indexVentas():
            return render_template('indexVentas.html')    