# routes/categorias_routes.py
from flask import render_template, request, redirect, url_for, flash

class CategoriasRoutes:
    def __init__(self, app, mysql):
        self.app = app
        self.mysql = mysql
        self.register_routes()

    def register_routes(self):
        self.app.route('/categorias')(self.categorias)
        self.app.route('/add_categoria', methods=['POST'])(self.add_categoria)
        self.app.route('/edit_categoria/<id>')(self.get_categoria)
        self.app.route('/update_categoria/<id>', methods=['POST'])(self.update_categoria)

    def categorias(self):
        cur = self.mysql.connection.cursor()
        cur.execute('SELECT * FROM categorias')
        data = cur.fetchall()
        return render_template('categorias.html', categorias=data)

    def add_categoria(self):
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            nombre = request.form['nombre']
            cur = self.mysql.connection.cursor()
            cur.execute('INSERT INTO categorias (descripcion, nombre) VALUES (%s, %s)', (descripcion, nombre))
            self.mysql.connection.commit()
            flash('Categoría agregada exitosamente.', 'success')
            return redirect(url_for('categorias'))

    def get_categoria(self, id):
        cur = self.mysql.connection.cursor()
        cur.execute('SELECT * FROM categorias WHERE id_categoria = %s', (id,))
        data = cur.fetchone()
        return render_template('edit_categoria.html', categoria=data)

    def update_categoria(self, id):
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            nombre = request.form['nombre']
            cur = self.mysql.connection.cursor()
            cur.execute('UPDATE categorias SET descripcion = %s, nombre = %s WHERE id_categoria = %s',
                        (descripcion, nombre, id))
            self.mysql.connection.commit()
            flash('Categoría actualizada exitosamente.', 'success')
            return redirect(url_for('categorias'))
