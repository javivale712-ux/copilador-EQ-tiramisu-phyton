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
