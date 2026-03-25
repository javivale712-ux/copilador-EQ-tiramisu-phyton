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
        for num_linea, linea in enumerate(líneas, start=1):
            for coincidencia in patron.finditer(linea):
                Tipo - coincidencia. lastgroup
                valor = coincidencia.group(tipo)
                tokens_exp. append(f"Linea {num_linea}: [{valor}] -> {tipo}")
       return "\n".join(tokens_exp)

@staticmethod
def generar_arbol_sintactico(codigo_traducido):
    try:
        arbol = ast.parse(codigo_traducido)
        return ast.dump(arbol, indent-4)
    except SyntaxError as e:
        texto_error = e.text.strip() if e.text else ""
        return f"ERROR_SINTAXIS\nLínea {e.lineno}\n{e.msg}\nColumna {e.offset}\nTexto {texto_error}"
    except Exception as e:
        return f"Error al generar AST:\n{str(e)}"

@staticmethod 
def ejecutar_codigo(codigo_traducido):
    salida_consola - io.StringIO()
    espacio_nombres = {}
    try:
        modulo - ast.parse(codigo_traducido)
        expresion_final = None 

if modulo.body and isinstance(modulo.body[-1], ast.Expr):
    expresion_final = ast.Expression(modulo.body.pop().value)

modulo - ast.fix_missing_locations(modulo)
codigo_principal = compile(modulo, '<chu>', 'exec')
codigo_expresion = None
if expresion_final is not None:
    expresion_final = ast.fix_missing_locations(expresion_final)
codigo_expresion = compile(expresion_final, '<chu>', 'eval')

with contextlib.redirect_stdout(salida_consola):
    exec(codigo_principal, espacio_nombres)
valor_final - eval(codigo_expresion, espacio_nombres) if codigo_expresion else  None

salida_texto = salida_consola.getvalue().strip()
if salida_texto and valor_final is not None:
    return f"{salida_texto}\n{valor_final}"
if salida_texto:
    return salida_consola.getvalue()
if valor_final is not None:
    return str(valor_final)
return "Ejecucion completa sin salida."
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

            if patron_bloque.match(linea) and not stripped.endswith(":"):
                errores.append(f"Línea {num_linea}: falta ':' al final del bloque.")

            # Detecta comillas simples/dobles sin cerrar en la línea.
            if linea.count('"') % 2 != 0:
                errores.append(f"Línea {num_linea}: cadena con comillas dobles sin cerrar.")
            if linea.count("'") % 2 != 0:
                errores.append(f"Línea {num_linea}: cadena con comillas simples sin cerrar.")

        # Balanceo de paréntesis/corchetes/llaves.
        apertura = {"(": ")", "[": "]", "{": "}"}
        cierre_a_apertura = {")": "(", "]": "[", "}": "{"}
        pila = []
        for num_linea, linea in enumerate(lineas, start=1):
            for col, ch in enumerate(linea, start=1):
                if ch in apertura:
                    pila.append((ch, num_linea, col))
                elif ch in cierre_a_apertura:
                    if not pila or pila[-1][0] != cierre_a_apertura[ch]:
                        errores.append(f"Línea {num_linea}, columna {col}: cierre '{ch}' sin apertura correspondiente.")
                    else:
                        pila.pop()
        for ch, num_linea, col in pila:
            errores.append(f"Línea {num_linea}, columna {col}: apertura '{ch}' sin cierre '{apertura[ch]}'.")

        # Validación de sintaxis Python tras traducción de CHU.
        codigo_traducido = MotorCompilador.traducir_codigo(codigo_original)
        try:
            ast.parse(codigo_traducido)
        except SyntaxError as e:
            token = "desconocido"
            if e.text and e.offset:
                texto = e.text.rstrip("\n")
                for m in re.finditer(r'\b\w+\b|\S', texto):

























































self.consola.config(state="disabled")

    def _crear_menu(self):
        barra_menu = tk.Menu(self.ventana)
        self.ventana.config(menu=barra_menu)
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nuevo", command=self.nuevo_archivo)
        menu_archivo.add_command(label="Abrir", command=self.abrir_archivo)
        menu_archivo.add_command(label="Guardar", command=self.guardar)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.salir)

        menu_ejecutar = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Ejecutar", menu=menu_ejecutar)
        menu_ejecutar.add_command(label="Arbol Sintactico", command=self.mostrar_arbol_sintactico)
        menu_ejecutar.add_command(label="Analisis Lexico", command=self.mostrar_analisis_lexico)
        menu_ejecutar.add_command(label="Compilar", command=self.compilar)
        menu_ejecutar.add_command(label="Derivacion", command=self.mostrar_derivacion)
        menu_ejecutar.add_separator()
        menu_ejecutar.add_checkbutton(
            label="Autoactualizar salida",
            variable=self.auto_actualizar_var,
            command=self._al_cambiar_autoactualizacion
        )

    def _on_codigo_modificado(self, _evento=None):
        if not self.texto.edit_modified():
            return

        self.texto.edit_modified(False)
        if self.auto_actualizar_var.get():
            self._programar_actualizacion()

    def _programar_actualizacion(self):
        if self._id_actualizacion is not None:
            self.ventana.after_cancel(self._id_actualizacion)
        # Debounce para evitar compilar en cada tecla sin pausa.
        self._id_actualizacion = self.ventana.after(450, self._actualizar_desde_codigo)

    def _actualizar_desde_codigo(self):
        self._id_actualizacion = None
        self._compilar_codigo(incluir_derivacion=False)

    def _al_cambiar_autoactualizacion(self):
        if self.auto_actualizar_var.get():
            self._programar_actualizacion()
            self._escribir_consola("Autoactualizacion activada. La salida se refresca segun cambie el codigo.")
            return

        if self._id_actualizacion is not None:
            self.ventana.after_cancel(self._id_actualizacion)
            self._id_actualizacion = None
        self._escribir_consola("Autoactualizacion desactivada.")






















































        if errores:
            resultado = (
                f"Se detectaron {len(errores)} errores de compilacion:\n"
                + "\n".join(f"- {e}" for e in errores)
            )
            if incluir_derivacion:
                resultado += "\n\n" + MotorCompilador.generar_derivacion(codigo_original)
            self._escribir_consola(resultado)
            return

        resultado_ejecucion = MotorCompilador.ejecutar_codigo(codigo_traducido)
        resultado = "Compilacion exitosa.\n\n=== RESULTADO ===\n" + resultado_ejecucion
        if incluir_derivacion:
            resultado += "\n\n" + MotorCompilador.generar_derivacion(codigo_original)
        self._escribir_consola(resultado)

    def _escribir_consola(self, texto):
        self.consola.config(state="normal")
        self.consola.delete(1.0, tk.END)
        self.consola.insert(tk.END, "=== TERMINAL ===\n\n")
        self.consola.insert(tk.END, texto)
        self.consola.config(state="disabled")

    def _mostrar_panel_analisis(self, titulo, contenido):
        if self.ventana_analisis is None or not self.ventana_analisis.winfo_exists():
            self.ventana_analisis = tk.Toplevel(self.ventana)
            self.ventana_analisis.geometry("750x600")
            self.texto_analisis = tk.Text(self.ventana_analisis, bg="#0d1117", fg="#58a6ff", font=("Consolas", 10))
            self.texto_analisis.pack(fill="both", expand=True)
        self.ventana_analisis.title(titulo)
        self.texto_analisis.config(state="normal")
        self.texto_analisis.delete(1.0, tk.END)
        self.texto_analisis.insert(tk.END, contenido)
        self.texto_analisis.config(state="disabled")

    def nuevo_archivo(self):
        self.texto.delete(1.0, tk.END)
        self.archivo_actual = None

    def abrir_archivo(self):
        archivo = filedialog.askopenfilename(title="Abrir archivo .chu", filetypes=[("Archivos Chu", "*.chu")])
        if archivo:
            with open(archivo, "r", encoding="utf-8") as f:
                self.texto.delete(1.0, tk.END)
                self.texto.insert(tk.END, f.read())
            self.archivo_actual = archivo
            self.ventana.title(f"Compilador Chu - {archivo}")

    def guardar(self):
        if self.archivo_actual:
            with open(self.archivo_actual, "w", encoding="utf-8") as f:
                f.write(self.texto.get(1.0, tk.END))
            messagebox.showinfo("Guardar", "Guardado con éxito")
        else:
            self.guardar_como()
                def _escribir_consola(self, texto):
        self.consola.config(state="normal")
        self.consola.delete(1.0, tk.END)
        self.consola.insert(tk.END, "=== TERMINAL ===\n\n")
        self.consola.insert(tk.END, texto)
        self.consola.config(state="disabled")

    def _mostrar_panel_analisis(self, titulo, contenido):
        if self.ventana_analisis is None or not self.ventana_analisis.winfo_exists():
            self.ventana_analisis = tk.Toplevel(self.ventana)
            self.ventana_analisis.geometry("750x600")
            self.texto_analisis = tk.Text(self.ventana_analisis, bg="#0d1117", fg="#58a6ff", font=("Consolas", 10))
            self.texto_analisis.pack(fill="both", expand=True)
        self.ventana_analisis.title(titulo)
        self.texto_analisis.config(state="normal")
        self.texto_analisis.delete(1.0, tk.END)
        self.texto_analisis.insert(tk.END, contenido)
        self.texto_analisis.config(state="disabled")

    def nuevo_archivo(self):
        self.texto.delete(1.0, tk.END)
        self.archivo_actual = None

    def abrir_archivo(self):
        archivo = filedialog.askopenfilename(title="Abrir archivo .chu", filetypes=[("Archivos Chu", "*.chu")])
        if archivo:
            with open(archivo, "r", encoding="utf-8") as f:
                self.texto.delete(1.0, tk.END)
                self.texto.insert(tk.END, f.read())
            self.archivo_actual = archivo
            self.ventana.title(f"Compilador Chu - {archivo}")

    def guardar(self):
        if self.archivo_actual:
            with open(self.archivo_actual, "w", encoding="utf-8") as f:
                f.write(self.texto.get(1.0, tk.END))
            messagebox.showinfo("Guardar", "Guardado con éxito")
        else:
            self.guardar_como()

    def guardar_como(self):
        archivo = filedialog.asksaveasfilename(title="Guardar como", defaultextension=".chu", filetypes=[("Archivos Chu", "*.chu")])
        if archivo:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(self.texto.get(1.0, tk.END))
            self.archivo_actual = archivo
            self.ventana.title(f"Compilador Chu - {archivo}")

    def salir(self):
        if messagebox.askokcancel("Salir", "¿Deseas salir?"):
            self.ventana.destroy()

if __name__ == "__main__":
    raiz = tk.Tk()
    app = IDEChu(raiz)
    raiz.mainloop()
