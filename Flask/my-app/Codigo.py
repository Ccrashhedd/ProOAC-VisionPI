from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd

app = Flask(__name__)

# Ruta principal y página de asistencia
@app.route('/')
@app.route('/asistencia')
def asistencia():
    return render_template('asistencia.html')

# Página para editar la lista
@app.route('/editar_lista')
def editar():
    return render_template('editar_lista.html')
# Ruta para obtener la lista de estudiantes
@app.route('/obtener_lista', methods=['GET'])
def obtener_lista():
    excel_path = 'Lista1.xlsx'
    try:
        df = pd.read_excel(excel_path)

        # Validar que las columnas requeridas existan
        columnas_requeridas = ['Apellido', 'Nombre', 'Cedula']
        if not all(column in df.columns for column in columnas_requeridas):
            return jsonify({'error': 'El archivo Excel no contiene las columnas necesarias (Apellido, Nombre, Cedula).'}), 400

        # Reemplazar valores NaN con cadenas vacías
        df[columnas_requeridas] = df[columnas_requeridas].fillna('')

        # Convertir las columnas requeridas a JSON
        lista = df[columnas_requeridas].to_dict(orient='records')

        return jsonify(lista), 200
    except FileNotFoundError:
        return jsonify({'error': 'Archivo Excel no encontrado.'}), 404
    except Exception as e:
        print(f"Error al obtener la lista: {e}")  # Log para depuración
        return jsonify({'error': f"Error al obtener la lista: {e}"}), 500

#Descargar el excel desde edita_lista
@app.route('/descargar_excel', methods=['GET'])
def descargar_excel():
    # Ruta del archivo Excel
    excel_path = 'Lista1.xlsx'

    try:
        # Enviar el archivo al cliente
        return send_file(excel_path, as_attachment=True, download_name='Lista1.xlsx')
    except Exception as e:
        return f"Error al descargar el archivo: {e}", 500

# Ruta para buscar un estudiante en el Excel
@app.route('/buscar_estudiante', methods=['POST'])
def buscar_estudiante():
    student_cedula = request.json.get('student_cedula')  # Cédula del estudiante

    # Validar que se haya proporcionado la cédula
    if not student_cedula:
        return jsonify({'error': 'Cédula no proporcionada'}), 400

    # Ruta del archivo Excel
    excel_path = 'Lista1.xlsx'

    try:
        # Leer el archivo Excel
        df = pd.read_excel(excel_path)

        # Buscar al estudiante por cédula
        estudiante_encontrado = df[df['Cedula'] == student_cedula]

        if not estudiante_encontrado.empty:
            # Obtener los datos del estudiante
            estudiante = estudiante_encontrado.iloc[0]
            nombre_completo = f"{estudiante['Apellido']} {estudiante['Nombre']}"

            # Retornar el nombre completo del estudiante
            return jsonify({'nombre': nombre_completo}), 200
        else:
            return jsonify({'error': f"Estudiante con cédula {student_cedula} no encontrado."}), 404
    except Exception as e:
        return jsonify({'error': f"Error al buscar el estudiante: {e}"}), 500

# Ruta para actualizar el estado de un estudiante en el Excel
@app.route('/editar_estado', methods=['POST'])
def editar_estado():
    data = request.json  # Obtener los datos enviados como JSON
    student_cedula = data.get('student_cedula')  # Cédula del estudiante
    status = data.get('status')  # Estado: Presente, Ausente, Tardanza, Fuga

    if not student_cedula or not status:
        return "Cédula o estado no proporcionado.", 400

    # Ruta del archivo Excel
    excel_path = 'Lista1.xlsx'

    try:
        # Leer el archivo Excel
        df = pd.read_excel(excel_path)

        # Identificar la columna correspondiente al estado (fecha actual)
        fecha_columna = df.columns[4]  # La columna E contiene las fechas

        # Buscar al estudiante por cédula
        estudiante_encontrado = df[df['Cedula'] == student_cedula]

        if not estudiante_encontrado.empty:
            # Actualizar el estado en la columna correspondiente
            df.loc[estudiante_encontrado.index, fecha_columna] = status

            # Guardar los cambios en el archivo Excel
            df.to_excel(excel_path, index=False)

            return f"Estado del estudiante con cédula {student_cedula} actualizado a {status}.", 200
        else:
            return f"Estudiante con cédula {student_cedula} no encontrado.", 404
    except Exception as e:
        return f"Error al editar el archivo Excel: {e}", 500


# Página para generar QR
@app.route('/QRgenerador')
def generar_qr():
    return render_template('QRgenerador.html')

# Página para crear un Excel
@app.route('/crear_excel')
def crear_excel():
    return render_template('crear_excel.html')

# Corre el sitio mientras el archivo se está ejecutando
if __name__ == '__main__':
    app.run(debug=True)
