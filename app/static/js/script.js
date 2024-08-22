// Función que agrega un valor (número u operador) al display de la calculadora.
let primerNumero = '';
let operador = '';
let resultadoMostrado = false;

function agregarAPantalla(valor) {
    const pantalla = document.getElementById('pantalla');
    const operacion = document.getElementById('operacion');

    if (pantalla.value.includes('Error')) {
        pantalla.value = '';
        operacion.textContent = '';
        primerNumero = '';
        operador = '';
        resultadoMostrado = false;
    }

    // Si el valor es un operador, actualiza la pantalla y el operador
    if (['+', '-', '*', '/'].includes(valor)) {
        if (pantalla.value !== '') {
            primerNumero = pantalla.value;
            operador = valor;
            operacion.textContent = primerNumero + ' ' + operador;
            pantalla.value = '';
            resultadoMostrado = false;
        }
    } else {
        if (resultadoMostrado) {
            pantalla.value = '';
            primerNumero = '';
            operador = '';
            resultadoMostrado = false;
        }
        pantalla.value += valor;
    }
}

// Función que limpia el display de la calculadora.
function limpiarPantalla() {
    document.getElementById('pantalla').value = '';
}

// Función que envía la expresión matemática al servidor para su evaluación.
function calcular() {
    const pantalla = document.getElementById('pantalla');
    const operacion = document.getElementById('operacion');

    if (primerNumero !== '' && operador !== '') {
        const segundoNumero = pantalla.value;
        const expresion = primerNumero + operador + segundoNumero;

        fetch('/calcular', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ expresion: expresion })
        })
        .then(response => response.json())
        .then(data => {
            if (data.resultado === 'Error') {
                pantalla.value = 'Error';
            } else {
                pantalla.value = data.resultado;
                actualizarHistorial(data.historial);
                operacion.textContent = '';
                primerNumero = '';
                operador = '';
                resultadoMostrado = true;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            pantalla.value = 'Error';
        });
    }
}

// Función para actualizar el historial en el frontend.
function actualizarHistorial(historial) {
    const historialUl = document.getElementById('historial');
    historialUl.innerHTML = ''; // Limpiar el historial actual

    historial.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.expresion} = ${item.resultado}`;
        historialUl.appendChild(li);
    });
}

// Función para mostrar una sugerencia.
function mostrarSugerencia() {
    fetch('/sugerir', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        const sugerenciaTexto = document.getElementById('sugerencia-texto');
        sugerenciaTexto.textContent = data.sugerencia;
    })
    .catch(error => {
        console.error('Error al obtener la sugerencia:', error);
    });
}

// Función para alternar entre modo claro y oscuro.
function toggleModoOscuro() {
    const currentTheme = document.body.getAttribute('data-theme');

    if (currentTheme === 'dark') {
        document.body.setAttribute('data-theme', 'light');
    } else {
        document.body.setAttribute('data-theme', 'dark');
    }
}

document.getElementById('toggle-tema').addEventListener('click', toggleModoOscuro);

function addNewRecord(recordContent) {
    // Crear un nuevo elemento de registro
    const newRecord = document.createElement('div');
    newRecord.className = 'record new-record'; // Clase para el nuevo registro
    newRecord.textContent = recordContent;
    
    // Agregar el nuevo registro al contenedor de registros
    const container = document.getElementById('record-container');
    
    // Aplicar animación a los registros existentes
    Array.from(container.children).forEach(child => {
      child.classList.add('existing-record');
    });
    
    // Insertar el nuevo registro antes del primero
    container.insertBefore(newRecord, container.firstChild);
    
    // Asegúrate de eliminar la animación después de que termine para evitar efectos no deseados
    newRecord.addEventListener('animationend', () => {
      newRecord.classList.remove('new-record');
    });
    
    // Limpiar animación de los registros antiguos
    container.querySelectorAll('.existing-record').forEach(record => {
      record.addEventListener('animationend', () => {
        record.classList.remove('existing-record');
        record.style.opacity = ''; // Limpiar el estilo de opacidad
      });
    });
  }