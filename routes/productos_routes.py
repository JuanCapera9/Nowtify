from flask import render_template, request, redirect, url_for, flash

class ProductosRoutes:
    def __init__(self, app, mysql):
        self.app = app
        self.mysql = mysql
        self.add_routes()

    def add_routes(self):
        @self.app.route('/productos')
        def productos():
            cur = self.mysql.connection.cursor()
            cur.execute("""SELECT prod.referencia, 
                            prod.nombre,
                            prod.cantidad, 
                            prod.descripcion, 
                            prod.diametro, 
                            prod.largo, 
                            prod.medida, 
                            prod.precio, 
                            cat.nombre AS Categoria, 
                            p.nombre AS Proveedor
                        FROM producto prod
                        JOIN proveedores p ON prod.proveedor = p.id_proveedor 
                        JOIN categorias cat ON prod.categoria = cat.id_categoria""")
            data = cur.fetchall()
            cur.execute('SELECT id_categoria, nombre FROM categorias')
            categorias = cur.fetchall()
            cur.execute('SELECT id_proveedor, nombre FROM proveedores')
            proveedores = cur.fetchall()
            return render_template('productos.html', productos=data, categorias=categorias, proveedores=proveedores)

        @self.app.route('/add_productos', methods=['GET', 'POST'])
        def add_productos():
            if request.method == "POST":
                referencia = request.form['referencia']
                nombre = request.form['nombre']
                cantidad = request.form['cantidad']
                descripcion = request.form['descripcion']
                diametro = request.form['diametro']
                largo = request.form['largo']
                medida = request.form['medida']
                precio = request.form['precio']
                categoria_id = request.form['categoria']
                proveedor_id = request.form['proveedor']

                cur = self.mysql.connection.cursor()
                cur.execute('SELECT * FROM producto WHERE referencia = %s', (referencia,))
                existing_producto = cur.fetchone()
                if existing_producto:
                    flash('La referencia del producto ya existe. Intente con otro.', 'warning')
                    return redirect(url_for('productos'))

                cur.execute(
                    'INSERT INTO producto (referencia, nombre, cantidad, descripcion, diametro, largo, medida, precio, categoria, proveedor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (referencia, nombre, cantidad, descripcion, diametro, largo, medida, precio, categoria_id, proveedor_id))
                self.mysql.connection.commit()
                flash('Producto agregado exitosamente.', 'success')
                return redirect(url_for('productos'))
            else:
                cur = self.mysql.connection.cursor()
                cur.execute('SELECT * FROM categorias')
                categorias = cur.fetchall()
                cur.execute('SELECT * FROM proveedores')
                proveedores = cur.fetchall()
                return render_template('producto.html', categorias=categorias, proveedores=proveedores)

        @self.app.route('/edit/<referencia>')
        def get_producto(referencia):
            cur = self.mysql.connection.cursor()
            cur.execute('SELECT * FROM producto WHERE referencia = %s', (referencia,))
            data = cur.fetchone()
            return render_template('edit_producto.html', producto=data)

        @self.app.route('/update/<referencia>', methods=['POST'])
        def update_producto(referencia):
            if request.method == 'POST':
                nombre = request.form['nombre']
                cantidad = request.form['cantidad']
                descripcion = request.form['descripcion']
                diametro = request.form['diametro']
                largo = request.form['largo']
                medida = request.form['medida']
                precio = request.form['precio']
                categoria_id = request.form['categoria']
                proveedor_id = request.form['proveedor']

                cur = self.mysql.connection.cursor()
                cur.execute('SELECT * FROM categorias WHERE id_categoria = %s', (categoria_id,))
                existing_categoria = cur.fetchone()
                if not existing_categoria:
                    flash('La categoría especificada no existe. Por favor, seleccione una categoría válida.', 'warning')
                    return redirect(url_for('productos'))

                cur.execute('SELECT * FROM proveedores WHERE id_proveedor = %s', (proveedor_id,))
                existing_proveedor = cur.fetchone()
                if not existing_proveedor:
                    flash('El proveedor especificado no existe. Por favor, seleccione un proveedor válido.', 'warning')
                    return redirect(url_for('productos'))

                cur.execute(
                    'UPDATE producto SET nombre = %s, cantidad = %s, descripcion = %s, diametro = %s, largo = %s, medida = %s, precio = %s, categoria = %s, proveedor = %s WHERE referencia = %s',
                    (nombre, cantidad, descripcion, diametro, largo, medida, precio, categoria_id, proveedor_id, referencia))
                self.mysql.connection.commit()
                flash('Producto actualizado exitosamente.', 'success')
            return redirect(url_for('productos'))
