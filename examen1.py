from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bdexamen"
    )

@app.route('/')
def index():
    return redirect(url_for('principal'))

@app.route('/principal', methods=['GET', 'POST'])
def principal():
    return render_template('principal.html')

@app.route('/GrabarCartera', methods=['GET', 'POST'])
def InsertarCartera():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tipocartera")
    tipos = cursor.fetchall()
    mensaje = None

    if request.method == 'POST':
        descripcion = request.form['txtdescription']
        tipo = request.form['txttipocartera']
        precio = request.form['txtprecio']
        fecha = request.form['fecha']

        cursor.execute("""
            INSERT INTO cartera
            (descripcar, codtipcar, preciocar, fechacar)
            VALUES (%s, %s, %s, %s)
        """, (descripcion, tipo, precio, fecha))
        conn.commit()
        mensaje = "¡Se grabó el registro satisfactoriamente!"

    conn.close()
    return render_template('RegistrarCartera.html', tipos=tipos, mensaje=mensaje)

@app.route('/BuscarCartera', methods=['GET', 'POST'])
def ConsultarCartera():
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tipocartera")
    tipos = cursor.fetchall()
    cartera = []

    if request.method == 'POST':
        tipo = request.form['txttipocartera']
        cursor.execute("""
            SELECT c.codcar, c.descripcar, t.nombtipcar, c.preciocar, c.fechacar
            FROM cartera c
            JOIN tipocartera t ON c.codtipcar = t.codtipcar
            WHERE c.codtipcar = %s
        """, (tipo,))
        cartera = cursor.fetchall()

    conn.close()
    return render_template('ConsultarCartera.html', tipos=tipos, cartera=cartera)

if __name__ == '__main__':
    app.run(debug=True)




import os

if __name__ == '__main__':
    if not os.path.exists(app.config ['UPLOAD_FOLDER']):
        os.makedirs(app.config [ 'UPLOAD_FOLDER'])
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5000))
