import tkinter as tk
from tkinter import filedialog, messagebox
import re
import io
import contextlib
import ast

class LenguajeChu:
    PALABRAS_RESERVADAS = {
        "y": "and", "o": "or", "nel": "not", "mentira": "False",
        "verdad": "True", "nada": "None", "mientras": "while",
        "para": "for", "en": "in", "rango": "range",
        "rotos": "break", "reanuda": "continue",
        "Si": "if", "Tons": "elif", "Tonses": "else",
        "definir": "def", "regresar": "return", "pasar": "pass",
        "clase": "class", "de": "from", "importar": "import",
        "afuera": "print", "adentro": "input",
        "Suma": "+", "Resta": "-", "Multiplicacion": "*",
        "Divicion": "/", "poto": "//"
    }

class MotorCompilador:

    @staticmethod
    def traducir_codigo(contenido):
        """ Traduce Chu a Python respetando la indentación original """
        # Reemplazar declaraciones de tipo
        patron_declaracion = re.compile(r'\b(entero|Flota|Texto|Siono)\s+([a-zA-Z_]\w*)\s*=')
        contenido = patron_declaracion.sub(r'\2 =', contenido)

        # Separar strings para no modificarlas
        partes = re.split(r'(".*?"|\'.*?\')', contenido)

        diccionario = sorted(
            LenguajeChu.PALABRAS_RESERVADAS.items(),
            key=lambda x: len(x[0]), reverse=True
        )

        for i in range(len(partes)):
            if not (partes[i].startswith('"') or partes[i].startswith("'")):
                for creada, original in diccionario:
                    if creada.isalpha():
                        patron = rf'\b{creada}\b'
                        partes[i] = re.sub(patron, original, partes[i])
                    else:
                        partes[i] = partes[i].replace(creada, original)

        return "".join(partes)

    @staticmethod
    def analizar_tokens(codigo):
        tokens_exp = []
        lineas = codigo.split("\n")
        patron = re.compile(
            r'(?P<CADENA>".*?"|\'.*?\')|'
            r'(?P<NUMERO>\b\d+(\.\d+)?\b)|'
            r'(?P<ASIGNACION>=)|'
            r'(?P<PALABRA>[a-zA-Z_]\w*)'
        )
        for num_linea, linea in enumerate(lineas, start=1):
            for coincidencia in patron.finditer(linea):
                tipo = coincidencia.lastgroup
                valor = coincidencia.group(tipo)
                tokens_exp.append(f"Línea {num_linea}: [{valor}] → {tipo}")
        return "\n".join(tokens_exp)
@staticmethod
    def generar_arbol_sintactico(codigo_traducido):
        try:
            arbol = ast.parse(codigo_traducido)
            return ast.dump(arbol, indent=4)
        except SyntaxError as e:
            texto_error = e.text.strip() if e.text else ""
            return f"ERROR_SINTAXIS\nLínea {e.lineno}\n{e.msg}\nColumna {e.offset}\nTexto {texto_error}"
        except Exception as e:
            return f"Error al generar AST:\n{str(e)}"

    @staticmethod
    def ejecutar_codigo(codigo_traducido):
        salida_consola = io.StringIO()
        espacio_nombres = {}
        try:
            modulo = ast.parse(codigo_traducido)
            expresion_final = None

            if modulo.body and isinstance(modulo.body[-1], ast.Expr):
                expresion_final = ast.Expression(modulo.body.pop().value)

            modulo = ast.fix_missing_locations(modulo)
            codigo_principal = compile(modulo, "<chu>", "exec")
            codigo_expresion = None
            if expresion_final is not None:
                expresion_final = ast.fix_missing_locations(expresion_final)
                codigo_expresion = compile(expresion_final, "<chu>", "eval")

            with contextlib.redirect_stdout(salida_consola):
                exec(codigo_principal, espacio_nombres)
                valor_final = eval(codigo_expresion, espacio_nombres) if codigo_expresion else None

            salida_texto = salida_consola.getvalue().strip()
            if salida_texto and valor_final is not None:
                return f"{salida_texto}\n{valor_final}"
            if salida_texto:
                return salida_consola.getvalue()
            if valor_final is not None:
                return str(valor_final)
            return "Ejecucion completada sin salida."
        except Exception as e:
            return f"Error de ejecución:\n{type(e).__name__}: {str(e)}"

    @staticmethod
    def detectar_errores(codigo_original):
        errores = []
        lineas = codigo_original.split("\n")

        # Reglas estructurales del lenguaje CHU (permite encontrar varios errores en una sola pasada).
        patron_bloque = re.compile(r'^\s*(Si|Tons|Tonses|mientras|para|definir|clase)\b')
        for num_linea, linea in enumerate(lineas, start=1):
            if not linea:
                continue

            indent_texto = re.match(r'^\s*', linea).group(0)
            if "\t" in indent_texto:
                errores.append(f"Línea {num_linea}: no uses tabulaciones; usa espacios.")
            if "\t" not in indent_texto and (len(indent_texto) % 4 != 0):
                errores.append(f"Línea {num_linea}: la indentación debe ser múltiplo de 4 espacios.")

            stripped = linea.strip()
            if not stripped or stripped.startswith("#"):
                continue
