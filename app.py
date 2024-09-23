from datetime import date
from flask import Flask, flash, redirect , render_template, request, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)



#MySQL Conection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'contactos'
mysql = MySQL(app)

#Configuraciones 
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    data = cur.fetchall()
    print(data)
    return render_template('Index.html', contactos = data)



@app.route('/Agregar_Contacto' , methods=['POST'])
def Agregar_Contacto():
    if request.method =='POST':
        NCompleto =   request.form['NCompleto']
        NTelefonico = request.form['NTelefonico']
        Email = request.form['Email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contactos (NCompleto , NTelefonico , Email) VALUES (%s , %s, %s)' ,
        (NCompleto , NTelefonico , Email))
        mysql.connection.commit()

        print(NCompleto)
        print(NTelefonico)
        print(Email)
        flash('El Contacto ha sido Guardado Exitosamente')
        return redirect(url_for('Index')) 

@app.route('/VerContactosGuardados')
def Ver_Contactos_Guardados():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contactos")  # Aquí se asume que tienes una tabla llamada 'contactos'
    contactos = cur.fetchall()  # Obtiene todos los registros de la consulta
    cur.close()
    return render_template('VerContactosGuardados.html', contactos=contactos)


@app.route('/Eliminar_Contacto/<string:id>')
def Eliminar_Contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))  
    mysql.connection.commit()
    flash('Se ha Eliminado el contacto correctamente')
    return redirect(url_for('Ver_Contactos_Guardados'))



@app.route('/Modificar_Contacto/<id>')
def get_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = %s', (id,)) 
    data = cur.fetchall()
    print(data[0])
    return render_template('Modificar_Contacto',contacto = data[0] )

if __name__ == '__main__':
    app.run(port=3000, debug=True)