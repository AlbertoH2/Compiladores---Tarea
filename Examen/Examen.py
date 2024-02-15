import ply.lex as lex
import tkinter as tk
from tkinter import ttk

# Palabras reservadas
palabras_reservadas = ["programa", "public", "static", "void", "main", "int", "printf", "end", "read"]

# Tokens
tokens = [
    'RESERVADA',
    'DELIMITADOR',
    'OPERADOR',
    'NUMERO_ENTERO',
    'PUNTO',
    'NUMERO_DECIMAL',
    'PARENTESIS_ABRIR',
    'PARENTESIS_CERRAR',
    'LLAVE_ABRIR',
    'LLAVE_CERRAR',
    'PUNTO_COMA',
    'IDENTIFICADOR',
    'ERROR_LEXICO'
]

# Regla para palabras reservadas
@lex.TOKEN(r'\b(?:' + '|'.join(palabras_reservadas) + r')\b')
def t_RESERVADA(t):
    return t

# Regla para identificador
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Regla para delimitador
t_DELIMITADOR = r','

# Regla para operador
t_OPERADOR = r'='

# Regla para números enteros
def t_NUMERO_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para el punto decimal
t_PUNTO = r'\.'

# Regla para números decimales
def t_NUMERO_DECIMAL(t):
    r'\d+'
    t.value = float(t.value)
    return t

# TOKENS DE PARENTESIS, LLAVES Y PUNTO Y COMA
t_PARENTESIS_ABRIR = r'\('
t_PARENTESIS_CERRAR = r'\)'
t_LLAVE_ABRIR = r'\{'
t_LLAVE_CERRAR = r'\}'
t_PUNTO_COMA = r';'

# ERRORES LEXICOS
def t_ERROR_LEXICO(t):
    r'[^a-zA-Z0-9_\(\)\{\}\=\,\;\.]'
    t.type = 'ERROR_LEXICO'
    return t

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Analizador léxico
analizador_lexico = lex.lex()

# Ventana principal
ventana = tk.Tk()
ventana.geometry("800x600")
ventana.title("Analizador Léxico")
ventana.config(bg="#f1f1f1")

# Etiqueta y entrada para el código fuente
etiqueta_entrada = tk.Label(ventana, text="Ingrese el código:", font=("Arial", 12), bg="#f1f1f1", fg="#333333")
etiqueta_entrada.pack(pady=5)

entrada_texto = tk.Text(ventana, font=("Arial", 12), bg="white", fg="#333333", height=10, width=100)
entrada_texto.pack(pady=5)
entrada_texto.configure(insertbackground="#333333")

# Etiqueta para mostrar los resultados
etiqueta_resultados = tk.Label(ventana, text="", font=("Arial", 12), bg="#f1f1f1", fg="#333333")
etiqueta_resultados.pack(pady=5)

# Botón de análisis
boton_analizar = tk.Button(ventana, text="Analizar", font=("Arial", 12), bg="#3498db", fg="white")
boton_analizar.pack(pady=5)

# Botón de limpieza
boton_limpiar = tk.Button(ventana, text="Limpiar", font=("Arial", 12), bg="#e74c3c", fg="white")
boton_limpiar.pack(pady=5)

# Ventana de resultados
frame_resultado = ttk.Treeview(ventana, columns=("Token", "Palabra Reservada", "Identificador", "Cadena", "Número", "Símbolo", "Tipo", "Línea"), show="headings")
frame_resultado.heading("Token", text="Token")
frame_resultado.heading("Palabra Reservada", text="Palabra Reservada")
frame_resultado.heading("Identificador", text="Identificador")
frame_resultado.heading("Cadena", text="Cadena")
frame_resultado.heading("Número", text="Número")
frame_resultado.heading("Símbolo", text="Símbolo")
frame_resultado.heading("Tipo", text="Tipo")
frame_resultado.heading("Línea", text="Línea")
frame_resultado.pack(pady=5, fill="both", expand=True)

# Configurar redimensionamiento de columnas
for column in frame_resultado["columns"]:
    frame_resultado.column(column, anchor="center", width=1)  # Establecer ancho mínimo inicial
    frame_resultado.heading(column, text=column, anchor="center")

def resize_columns(event):
    width = event.width
    for column in frame_resultado["columns"]:
        frame_resultado.column(column, width=width//len(frame_resultado["columns"]))

# Asociar el evento de redimensionamiento a la ventana principal
ventana.bind("<Configure>", resize_columns)

# Función de análisis de código
def analizar_codigo(event=None):
    codigo = entrada_texto.get("1.0", tk.END)
    entrada = codigo.split("\n")
    lexemas = []

    # Contadores
    contador_palabras_reservadas = 0
    contador_identificadores = 0
    contador_cadenas = 0
    contador_numeros = 0
    contador_simbolos = 0

    # Analiza cada línea del código y recopila los lexemas identificados.
    for i, entrada_linea in enumerate(entrada):
        analizador_lexico.input(entrada_linea)
        while True:
            token = analizador_lexico.token()
            if not token:
                break
            tipo = ""
            if token.type.startswith("RESERVADA"):
                tipo = "Palabra Reservada"
                contador_palabras_reservadas += 1
            elif token.type == "IDENTIFICADOR":
                tipo = "Identificador"
                contador_identificadores += 1
            elif token.type == "NUMERO_ENTERO" or token.type == "NUMERO_DECIMAL":
                tipo = "Número"
                contador_numeros += 1
            elif token.type == "ERROR_LEXICO":
                tipo = "Error Léxico"
            else:
                tipo = "Símbolo"
                contador_simbolos += 1
            lexemas.append((i + 1, token.value, tipo))

    # Actualizar la etiqueta con los resultados
    etiqueta_resultados.config(text=f"Palabras reservadas: {contador_palabras_reservadas}, Identificadores: {contador_identificadores}, Números: {contador_numeros}, Símbolos: {contador_simbolos}")

    # Limpia el contenido de la ventana de resultados
    for widget in frame_resultado.get_children():
        frame_resultado.delete(widget)

    # Muestra los lexemas identificados y sus números de línea en la ventana de resultados.
    for linea, lexema, tipo in lexemas:
        # Insertar "x" en la columna correspondiente y dejar las demás vacías
        values = [""] * 8
        if tipo == "Palabra Reservada":
            values[1] = "x"
        elif tipo == "Identificador":
            values[2] = "x"
        elif tipo == "Número":
            values[4] = "x"
        elif tipo == "Símbolo":
            values[5] = "x"
        elif tipo == "Error Léxico":
            values[6] = "x"
        values[0] = lexema  # Insertar el lexema en la columna "Token"
        values[7] = linea  # Insertar el número de línea
        frame_resultado.insert("", "end", values=values)

# Función de limpieza de ventanas
def limpiar_ventanas():
    entrada_texto.delete("1.0", tk.END)
    for widget in frame_resultado.get_children():
        frame_resultado.delete(widget)

# Configurar eventos de botones
boton_analizar.config(command=analizar_codigo)
boton_limpiar.config(command=limpiar_ventanas)

ventana.mainloop()
