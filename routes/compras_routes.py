from flask import render_template, request, redirect, url_for, flash

class ComprasRoutes:
    def __init__(self, app, mysql):
        self.app = app
        self.mysql = mysql
        self.register_routes()

    def register_routes(self):
        self.app.route('/compras')(self.compras)
        self.app.route('/add_compra', methods=['POST'])(self.add_compra)
        self.app.route('/update_compra/<id_compra>', methods=['POST'])(self.update_compra)
        self.app.route('/indexCompras')(self.indexCompras)  # Asegúrate de registrar esta ruta

    def compras(self):
        cur = self.mysql.connection.cursor()
        cur.execute("""SELECT comp.id_compra, comp.fecha_Compra, comp.total_compra, p.nombre as nombre
                    FROM compras comp 
                    JOIN proveedores p ON comp.proveedor = p.id_proveedor """)
        data = cur.fetchall()

        cur.execute("SELECT id_proveedor, nombre FROM proveedores")
        proveedor = cur.fetchall()
        return render_template('compras.html', compras=data, proveedor=proveedor)

    def add_compra(self):
        if request.method == 'POST':
            fecha_compra = request.form['fecha_compra']
            total_compra = request.form['total_compra']
            id_proveedor = request.form['proveedor']

            cur = self.mysql.connection.cursor()
            cur.execute('INSERT INTO compras (fecha_compra, total_compra, proveedor) VALUES (%s, %s, %s)', 
                        (fecha_compra, total_compra, id_proveedor))
            self.mysql.connection.commit()
            flash('Compra agregada exitosamente.', 'success')
            return redirect(url_for('compras'))

    def update_compra(self, id_compra):
        if request.method == 'POST':
            fecha_compra = request.form['fecha_compra']
            total_compra = request.form['total_compra']
            proveedor = request.form['proveedor']

            cur = self.mysql.connection.cursor()
            cur.execute("""
                UPDATE compras
                SET fecha_compra = %s,
                    total_compra = %s,
                    proveedor = (SELECT id_proveedor FROM proveedores WHERE nombre = %s)
                WHERE id_compra = %s
            """, (fecha_compra, total_compra, proveedor, id_compra))
            self.mysql.connection.commit()
            flash('Compra actualizada exitosamente.', 'success')
            return redirect(url_for('compras'))
        
    def indexCompras(self):
        return render_template('indexCompras.html')