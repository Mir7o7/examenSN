from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL') or 'postgresql://personas_db_user:SyF2QnzxumA5j9qm6nx2xmzNNsQVPATt@dpg-d01ctpadbo4c73cedskg-a.oregon-postgres.render.com/personas_db'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        cur = conn.cursor()
        cur.execute("INSERT INTO personas (dni, nombre, apellido, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
                    (dni, nombre, apellido, direccion, telefono))
        conn.commit()
        cur.close()
        return redirect('/')
    return render_template('index.html')

@app.route('/administrar')
def administrar():
    cur = conn.cursor()
    cur.execute("SELECT * FROM personas")
    rows = cur.fetchall()
    cur.close()
    personas = [
        {
            'id': row[0],
            'dni': row[1],
            'nombre': row[2],
            'apellido': row[3],
            'direccion': row[4],
            'telefono': row[5]
        }
        for row in rows
    ]
    return render_template('administrar.html', personas=personas)

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM personas WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    return redirect('/administrar')

if __name__ == '__main__':
    app.run(debug=True)
