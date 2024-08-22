"""
Flask: Es la clase principal que usamos para crear la aplicación web.

render_template: Lo usamos para renderizar archivos HTML. En este proyecto lo vamos a usar 
para mostrar la página principal de la calculadora.

request: Permite acceder a los datos enviados por el usuario usando POST Y GET. Lo vamos a usar 
para recibir la expresión matemática que el usuario quiere calcular.

jsonify: Convierte Python a JSON, que es un formato de datos ligero que podemos enviar como 
respuesta a solicitudes web.

"""

from flask import Flask, render_template, request, jsonify
from modelos.modelos import SuggestionModel, ErrorCorrectionModel

app = Flask(__name__, static_folder = 'app/static', template_folder = 'app/templates') # Creamos una isntacia Flask para la app web.

# Historial de cálculos.
historial_calculos = []

# Inicializamos los modelos.
modelo_sugerencias = SuggestionModel()
modelo_correccion = ErrorCorrectionModel()

# Definimos la ruta para la página principal ('/')
@app.route('/')
def index():

    # Renderizamos el archivo 'index.html'
    return render_template('index.html', historial = historial_calculos)

# Definimos la ruta '/calcular' que va a recibir solicitudes POST.
@app.route('/calcular', methods = ['POST'])
def calcular():

    datos = request.get_json() # Extraemos los datos en formato JSON enviados por el usuario.

    # Obtenemos la expresión matemática del JSON, o una cadena vacía si no se proporciona.
    expresion = datos.get('expresion', '')

    error = modelo_correccion.corregir_expresion(expresion)
    if error:
        return jsonify({'resultado': error}), 400

    try:

        resultado = eval(expresion, {"__builtins__": None}, {}) # Evaluamos la expresión matemática.
        historial_calculos.append({'expresion': expresion, 'resultado': resultado}) # Almacenamos el cálculo en el historial.

        #limitamos el historial a los últimos 10 cálculos.
        if len(historial_calculos) > 10:
            historial_calculos.pop(0)

        modelo_sugerencias.agregar_calculo(expresion, resultado)

        return jsonify({'resultado': resultado, 'historial': historial_calculos}) # Devolvemos el resultado en formato JSON.
    
    except Exception as e:
        # Si obtenemos un error lo capturamos y devolvemos un mensaje de error.
        return jsonify({'resultado': f"Error inesperado: {str(e)}"}), 400

# Definimos la ruta para sugerir un cálculo.
@app.route('/sugerir', methods = ['GET'])
def sugerir():
    
    sugerencia = modelo_sugerencias.sugerir_calculo()
    return jsonify({'sugerencia': sugerencia})

# Este bloque se asegura que el servidor se ejecute solo si el archivo se ejecuta directamente.
if __name__ == '__main__':
    # Iniciamos el servidor Flask en modo de depuración (debug mode).
    app.run(debug = True)