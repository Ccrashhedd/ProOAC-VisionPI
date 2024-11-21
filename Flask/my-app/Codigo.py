from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/asistencia')
def asistencia():
    return render_template('asistencia.html')

@app.route('/editar_lista')
def editar():
    return render_template('editar_lista.html')

@app.route('/QRgenerador')
def generar_qr():
    return render_template('QRgenerador.html')

@app.route('/crear_excel')
def crear_excel():
    return render_template('crear_excel.html')

# Corre el sitio mientras el archivo se está ejecutando
if __name__ == '__main__':
    app.run(debug=True)