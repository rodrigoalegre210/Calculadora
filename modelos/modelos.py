import random
import re

class SuggestionModel:

    def __init__(self):
        self.historial = []

    def agregar_calculo(self, expresion, resultado):
        self.historial.append({'expresion': expresion, 'resultado': resultado})

    def sugerir_calculo(self):
        # Si el historial está vacío o tiene solo una operación, no puede sugerir nada.
        if len(self.historial) < 3:
            return "No hay suficientes cálculos en el historial para hacer una sugerencia."
        
        ultimo = self.historial[-1]['expresion'] # Último cálculo realizado.

        # Extraemos las operaciones y números usados.
        operaciones = ['+', '-', '*', '/']
        numeros = [int(num) for num in ultimo if num.isdigit()]

        # Generamos sugerencias basada en operaciones y números previos.
        if len(numeros) > 1:
            operacion = random.choice(operaciones)
            nuevo_calculo = f"{numeros[-1]} {operacion} {random.choice(numeros)}"

        else:
            nuevo_calculo = f"{random.choice(numeros)} + {random.randint(1, 10)}"

        return nuevo_calculo
    
class ErrorCorrectionModel:

    def __init__(self):
        pass

    def corregir_expresion(self, expresion):

        if re.search(r'/\s*0', expresion):
            return "Error: División por cero detectada."
        
        expresion_limpia = re.sub(r'[^0-9+\-*/().]', '', expresion)
        
        try:
            eval(expresion_limpia, {"__builtins__": None}, {})
            return None
        except (SyntaxError, ZeroDivisionError):
            return "Error: Expresión matemática mal formada."
        except Exception as e:
            return f"Error: {str(e)}"