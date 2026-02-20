import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import secrets
import string
import shutil
import sys

def generar_contrasena_fuerte(longitud=16):
    """Genera una contraseña segura con letras, números y símbolos"""
    caracteres = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    while True:
        password = ''.join(secrets.choice(caracteres) for _ in range(longitud))
        # Aseguramos que tenga al menos un número, una mayúscula, minúscula y símbolo
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)):
            return password

def seleccionar_pdf():
    archivo = filedialog.askopenfilename(
        title="Selecciona el PDF a proteger",
        filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        entrada_var.set(archivo)
        salida_sugerida = os.path.splitext(archivo)[0] + "_Secure.pdf"
        salida_var.set(salida_sugerida)

def proteger_pdf():
    entrada = entrada_var.get().strip()
    salida = salida_var.get().strip()
    password = password_var.get().strip()

    if not entrada or not os.path.isfile(entrada):
        messagebox.showerror("Error", "Selecciona un archivo PDF válido")
        return

    if not salida:
        messagebox.showerror("Error", "Indica dónde guardar el PDF protegido")
        return

    if not password:
        messagebox.showerror("Error", "La contraseña no puede estar vacía")
        return

    try:
        # Llamamos a qpdf para encriptar (AES-256 por defecto en versiones modernas)
        # user password = abrir, owner password = permisos (aquí usamos la misma)
        resultado = subprocess.run([
            "qpdf",
            "--encrypt", password, password, "256",
            "--", entrada, salida
        ], capture_output=True, text=True)

        stderr_lower = (resultado.stderr or "").lower()
        # qpdf a veces devuelve texto de advertencia y puede devolver un código distinto de cero
        # cuando dice "operation succeeded with warnings" — tratamos ese caso como éxito pero avisamos.
        if resultado.returncode == 0 or "operation succeeded with warnings" in stderr_lower:
            msg = (
                f"PDF protegido creado correctamente:\n\n{salida}\n\n"
                f"Contraseña (cópiala ya):\n{password}\n\n"
                "Guárdala en un lugar seguro. Si la pierdes, no podrás abrir el archivo."
            )
            if resultado.stderr:
                msg += f"\n\nAdvertencias de qpdf:\n{resultado.stderr}"

            messagebox.showinfo("¡Éxito!", msg)

            # Cambiar texto del botón a indicación de éxito
            try:
                global btn_proteger
                if btn_proteger is not None:
                    btn_proteger.config(text="creado pdf seguro")
            except Exception:
                pass

            # Opcional: abrir la carpeta donde se guardó (cross-platform)
            def abrir_carpeta(path):
                try:
                    if os.name == 'nt':
                        os.startfile(path)
                    elif sys.platform == 'darwin':
                        subprocess.run(["open", path])
                    else:
                        subprocess.run(["xdg-open", path])
                except Exception:
                    pass

            abrir_carpeta(os.path.dirname(salida))
        else:
            # qpdf falló realmente
            messagebox.showerror("Error al encriptar", f"qpdf falló:\n{resultado.stderr}")

    except FileNotFoundError:
        messagebox.showerror("Error", "No se encuentra 'qpdf'.\nInstálalo con: choco install qpdf\ny asegúrate de que esté en el PATH.")
    except Exception as e:
        messagebox.showerror("Error inesperado", str(e))

# ────────────────────────────────────────────────
#          Interfaz gráfica
# ────────────────────────────────────────────────

ventana = tk.Tk()
ventana.title("Protector de PDF - con contraseña segura")
ventana.geometry("620x380")
ventana.resizable(False, False)

# Estilo básico
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10))

# Variables
entrada_var = tk.StringVar()
salida_var   = tk.StringVar()
password_var = tk.StringVar(value=generar_contrasena_fuerte(16))
# variable para referenciar el botón principal y actualizar su texto desde la función
btn_proteger = None

# ── Contenido ───────────────────────────────────

ttk.Label(ventana, text="PDF original:", font=("Segoe UI", 11, "bold")).pack(pady=(20,5), anchor="w", padx=20)

frame1 = ttk.Frame(ventana)
frame1.pack(fill="x", padx=20)
ttk.Entry(frame1, textvariable=entrada_var, width=60).pack(side="left", padx=(0,10))
ttk.Button(frame1, text=" Examinar...", command=seleccionar_pdf).pack(side="left")

ttk.Label(ventana, text="Guardar como:", font=("Segoe UI", 11, "bold")).pack(pady=(15,5), anchor="w", padx=20)

frame2 = ttk.Frame(ventana)
frame2.pack(fill="x", padx=20)
ttk.Entry(frame2, textvariable=salida_var, width=60).pack(side="left", padx=(0,10))
ttk.Button(frame2, text=" Examinar...", command=lambda: salida_var.set(
    filedialog.asksaveasfilename(
        title="Guardar PDF protegido como...",
        defaultextension=".pdf",
        filetypes=[("PDF", "*.pdf")],
        initialfile=os.path.splitext(entrada_var.get() or "documento")[0] + "_Secure.pdf"
    )
)).pack(side="left")

ttk.Label(ventana, text="Contraseña generada (cópiala ahora):", font=("Segoe UI", 11, "bold")).pack(pady=(25,5), anchor="w", padx=20)

frame_pass = ttk.Frame(ventana)
frame_pass.pack(fill="x", padx=20)
ttk.Entry(frame_pass, textvariable=password_var, width=40, show="•", font=("Consolas", 12)).pack(side="left", padx=(0,10))

ttk.Button(frame_pass, text="Nueva contraseña", command=lambda: password_var.set(generar_contrasena_fuerte(16))).pack(side="left")
ttk.Button(frame_pass, text="Copiar", command=lambda: ventana.clipboard_clear() or ventana.clipboard_append(password_var.get()) or messagebox.showinfo("Copiado", "Contraseña copiada al portapapeles")).pack(side="left", padx=10)

# Reemplazamos la creación del botón por una asignación a la variable global
btn_proteger = ttk.Button(ventana, text="PROTEGER PDF AHORA", command=proteger_pdf,
           style="Accent.TButton")
btn_proteger.pack(pady=30)

# Botón de estilo acentuado (opcional, requiere tema)
style.configure("Accent.TButton", font=("Segoe UI", 12, "bold"))

ventana.mainloop()