import tkinter as tk
from tkinter import messagebox
import random

# Lista de palabras
PALABRAS = [
    "python", "programacion", "computadora", "teclado", "monitor",
    "algoritmo", "variable", "funcion", "bucle", "clase",
    "internet", "software", "hardware", "archivo", "base",
    "pantalla", "ratón", "impresora", "servidor", "red",
    "chocolate", "mariposa", "elefante", "jirafas", "dinosaurio",
    "aventura", "musica", "pelicula", "viaje", "cocinero"
]

PISTAS = {
    "python": "Lenguaje de programación",
    "programacion": "Actividad de escribir código",
    "computadora": "Máquina electrónica",
    "teclado": "Dispositivo de entrada",
    "monitor": "Pantalla del PC",
    "algoritmo": "Conjunto de instrucciones lógicas",
    "variable": "Contenedor de datos en código",
    "funcion": "Bloque reutilizable de código",
    "bucle": "Repetición en programación",
    "clase": "Plantilla de objetos en OOP",
    "internet": "Red mundial de computadoras",
    "software": "Programas de computadora",
    "hardware": "Componentes físicos del PC",
    "archivo": "Documento digital",
    "base": "Fundamento o cimientos",
    "pantalla": "Superficie de visualización",
    "ratón": "Dispositivo señalador",
    "impresora": "Máquina que imprime",
    "servidor": "Computadora que provee servicios",
    "red": "Conexión de dispositivos",
    "chocolate": "Dulce de cacao",
    "mariposa": "Insecto con alas coloridas",
    "elefante": "Animal grande con trompa",
    "jirafas": "Animal de cuello largo",
    "dinosaurio": "Reptil prehistórico",
    "aventura": "Experiencia emocionante",
    "musica": "Arte de los sonidos",
    "pelicula": "Obra cinematográfica",
    "viaje": "Desplazamiento a otro lugar",
    "cocinero": "Persona que cocina",
}

# Partes del ahorcado (canvas drawings)
PASOS_AHORCADO = 6  # número de errores antes de perder

COLORES = {
    "fondo": "#1a1a2e",
    "panel": "#16213e",
    "acento": "#e94560",
    "texto": "#eaeaea",
    "letra_ok": "#4ecca3",
    "letra_mal": "#e94560",
    "boton": "#0f3460",
    "boton_hover": "#e94560",
    "gallows": "#eaeaea",
    "hombre": "#4ecca3",
}


class Ahorcado:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 El Ahorcado")
        self.root.configure(bg=COLORES["fondo"])
        self.root.resizable(False, False)

        self.palabra = ""
        self.pista = ""
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.errores = 0
        self.jugando = False

        self._construir_ui()
        self._nueva_partida()

    def _construir_ui(self):
        # Título
        titulo = tk.Label(
            self.root, text="⚰️  EL AHORCADO  ⚰️",
            font=("Courier New", 20, "bold"),
            fg=COLORES["acento"], bg=COLORES["fondo"]
        )
        titulo.pack(pady=(18, 0))

        # Marco principal
        main = tk.Frame(self.root, bg=COLORES["fondo"])
        main.pack(padx=20, pady=10)

        # Panel izquierdo — dibujo
        left = tk.Frame(main, bg=COLORES["panel"], bd=0,
                        highlightthickness=2, highlightbackground=COLORES["acento"])
        left.grid(row=0, column=0, padx=(0, 14), pady=4)

        self.canvas = tk.Canvas(
            left, width=200, height=230,
            bg=COLORES["panel"], highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        self._dibujar_horca()

        # Panel derecho — juego
        right = tk.Frame(main, bg=COLORES["fondo"])
        right.grid(row=0, column=1, sticky="n")

        # Pista
        self.lbl_pista = tk.Label(
            right, text="", font=("Courier New", 11),
            fg="#aaa", bg=COLORES["fondo"], wraplength=280, justify="center"
        )
        self.lbl_pista.pack(pady=(4, 0))

        # Palabra (guiones)
        self.lbl_palabra = tk.Label(
            right, text="", font=("Courier New", 28, "bold"),
            fg=COLORES["letra_ok"], bg=COLORES["fondo"]
        )
        self.lbl_palabra.pack(pady=(12, 4))

        # Errores
        self.lbl_errores = tk.Label(
            right, text="", font=("Courier New", 12),
            fg=COLORES["acento"], bg=COLORES["fondo"]
        )
        self.lbl_errores.pack()

        # Letras incorrectas
        self.lbl_incorrectas = tk.Label(
            right, text="", font=("Courier New", 12),
            fg=COLORES["letra_mal"], bg=COLORES["fondo"]
        )
        self.lbl_incorrectas.pack(pady=(2, 8))

        # Teclado
        self.frame_teclado = tk.Frame(right, bg=COLORES["fondo"])
        self.frame_teclado.pack()
        self.botones = {}
        filas = ["qwertyuiop", "asdfghjklñ", "zxcvbnm"]
        for fila in filas:
            f = tk.Frame(self.frame_teclado, bg=COLORES["fondo"])
            f.pack(pady=2)
            for letra in fila:
                btn = tk.Button(
                    f, text=letra.upper(),
                    width=3, height=1,
                    font=("Courier New", 9, "bold"),
                    bg=COLORES["boton"], fg=COLORES["texto"],
                    activebackground=COLORES["boton_hover"],
                    relief="flat", bd=0, cursor="hand2",
                    command=lambda l=letra: self._adivinar(l)
                )
                btn.pack(side="left", padx=1)
                self.botones[letra] = btn

        # Botón nueva partida
        self.btn_nuevo = tk.Button(
            right, text="🔄  Nueva Partida",
            font=("Courier New", 11, "bold"),
            bg=COLORES["acento"], fg="white",
            activebackground="#c73652",
            relief="flat", bd=0, padx=14, pady=6,
            cursor="hand2",
            command=self._nueva_partida
        )
        self.btn_nuevo.pack(pady=(10, 4))

        # Bind teclado físico
        self.root.bind("<Key>", self._tecla_presionada)

    def _nueva_partida(self):
        self.palabra = random.choice(PALABRAS)
        self.pista = PISTAS.get(self.palabra, "")
        self.letras_adivinadas = set()
        self.letras_incorrectas = set()
        self.errores = 0
        self.jugando = True

        # Reset botones
        for letra, btn in self.botones.items():
            btn.config(bg=COLORES["boton"], fg=COLORES["texto"],
                       state="normal", relief="flat")

        self._actualizar_ui()
        self._dibujar_horca()

    def _adivinar(self, letra):
        letra = letra.lower()
        if not self.jugando:
            return
        if letra in self.letras_adivinadas or letra in self.letras_incorrectas:
            return

        btn = self.botones.get(letra)

        if letra in self.palabra:
            self.letras_adivinadas.add(letra)
            if btn:
                btn.config(bg=COLORES["letra_ok"], fg=COLORES["panel"],
                           state="disabled")
        else:
            self.letras_incorrectas.add(letra)
            self.errores += 1
            if btn:
                btn.config(bg=COLORES["letra_mal"], fg="white",
                           state="disabled")
            self._dibujar_parte_hombre()

        self._actualizar_ui()
        self._verificar_fin()

    def _tecla_presionada(self, event):
        letra = event.char.lower()
        if letra.isalpha():
            self._adivinar(letra)

    def _actualizar_ui(self):
        # Palabra
        mostrar = " ".join(
            l if l in self.letras_adivinadas else "_"
            for l in self.palabra
        )
        self.lbl_palabra.config(text=mostrar)

        # Pista
        self.lbl_pista.config(text=f"💡 Pista: {self.pista}")

        # Errores
        self.lbl_errores.config(
            text=f"Errores: {self.errores} / {PASOS_AHORCADO}"
        )

        # Letras incorrectas
        inc = "  ".join(sorted(l.upper() for l in self.letras_incorrectas))
        self.lbl_incorrectas.config(
            text=f"Incorrectas: {inc}" if inc else ""
        )

    def _verificar_fin(self):
        # Ganó
        if all(l in self.letras_adivinadas for l in self.palabra):
            self.jugando = False
            self.lbl_palabra.config(fg="#ffd700")
            messagebox.showinfo(
                "🎉 ¡Ganaste!",
                f"¡Excelente! La palabra era:\n\n« {self.palabra.upper()} »\n\n¡Lo lograste con {self.errores} error(es)!"
            )
        # Perdió
        elif self.errores >= PASOS_AHORCADO:
            self.jugando = False
            self.lbl_palabra.config(
                text=" ".join(self.palabra),
                fg=COLORES["acento"]
            )
            messagebox.showinfo(
                "💀 ¡Perdiste!",
                f"¡Oh no! La palabra era:\n\n« {self.palabra.upper()} »\n\n¡Inténtalo de nuevo!"
            )

    # ── Dibujo del ahorcado ──────────────────────────────────────────────

    def _dibujar_horca(self):
        self.canvas.delete("all")
        c = self.canvas
        g = COLORES["gallows"]

        # Base
        c.create_line(20, 220, 180, 220, fill=g, width=4)
        # Poste vertical
        c.create_line(60, 220, 60, 20, fill=g, width=4)
        # Viga horizontal
        c.create_line(60, 20, 140, 20, fill=g, width=4)
        # Cuerda
        c.create_line(140, 20, 140, 45, fill=g, width=3)

        # Redibujar partes según errores actuales
        self._partes = []
        for i in range(self.errores):
            self._agregar_parte(i)

    def _dibujar_parte_hombre(self):
        self._agregar_parte(self.errores - 1)

    def _agregar_parte(self, indice):
        c = self.canvas
        h = COLORES["hombre"]
        partes = [
            # 0: Cabeza
            lambda: c.create_oval(118, 45, 162, 85, outline=h, width=3),
            # 1: Cuerpo
            lambda: c.create_line(140, 85, 140, 150, fill=h, width=3),
            # 2: Brazo izquierdo
            lambda: c.create_line(140, 100, 110, 130, fill=h, width=3),
            # 3: Brazo derecho
            lambda: c.create_line(140, 100, 170, 130, fill=h, width=3),
            # 4: Pierna izquierda
            lambda: c.create_line(140, 150, 110, 185, fill=h, width=3),
            # 5: Pierna derecha
            lambda: c.create_line(140, 150, 170, 185, fill=h, width=3),
        ]
        if 0 <= indice < len(partes):
            partes[indice]()


# ── Main ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("620x520")
    app = Ahorcado(root)
    root.mainloop()