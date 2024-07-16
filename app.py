from flask import Flask, render_template, g, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', name = 'home')



#conexion hacia la DB.

DATABASE_CONFIG = {
    'user':'root',
    'password':'123456',
    'host':'localhost',
    'database':'usuarios_crud'
}

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**DATABASE_CONFIG)
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        

@app.route('/users')
def users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    return ', '.join([user[0] for user in users])


#Operaciones CRUD

#Agregar usuario.
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO user (nombre, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        db.commit()
        return redirect(url_for('user'))

    return render_template('add_user.html')


#listar usuarios:

@app.route('/usuarios')
def user():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT iduser ,nombre ,email  FROM user")
    users_list = cursor.fetchall()
    return render_template('usuarioslist.html', users=users_list, name='user')


if __name__ == '__main__':
    app.run(debug=True)