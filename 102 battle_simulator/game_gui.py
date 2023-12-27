import tkinter as tk
from Driver import Driver
import winsound
from pathlib import Path
from PIL import Image, ImageTk

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.battle_started = False
        self.title("Battle Game")
        self.geometry("2200x1000")  # Tamaño de la ventana

        # Frame for log and button
        self.text_frame = tk.Frame(self)
        self.text_frame.pack(side="left", fill="both", expand=True)

        self.label = tk.Label(self, text="Let the battle commence!")
        self.label.pack(in_=self.text_frame)

        self.start_button = tk.Button(self, text="Start battle", command=self.toggle_battle)
        self.start_button.pack(in_=self.text_frame)

        self.text_widget = tk.Text(self, height=35, width=95)
        self.text_widget.pack(in_=self.text_frame)
        tk.Label(self, text="Battle log", font=('Verdana', 14)).pack(before=self.text_widget)

        self.driver = Driver(self.update_message)

        # Verdana font for all elements
        font = ('Verdana', 12)
        self.text_widget.config(font=font)
        self.start_button.config(font=font)

        # Padding and margins
        self.text_widget.pack(pady=(10, 10))
        self.text_widget.config(padx=10, pady=10)

        # Colours
        self.text_widget.config(bg="black", fg="white")
        self.start_button.config(bg="gray", fg="black")

        # Button relief/border
        self.start_button.config(relief=tk.RAISED, borderwidth=2)

        # Scrollbar for text widget
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_widget.yview)

        # Frame for the final victory image
        self.image_frame = tk.Frame(self)
        self.image_frame.pack(side="right", fill="y")

    def toggle_battle(self):
        if not self.battle_started:
            self.battle_started = True
            self.start_button.config(text="Restart Battle")
            self.start_battle()
        else:
            self.reset_game()

    def start_battle(self):
        self.driver.startBattle()
        self.play_sound("M1Garand.wav")
        self.show_image("Triumphant.png")

    def update_message(self, message):
        self.text_widget.insert(tk.END, message + "\n")
        self.text_widget.see(tk.END)  # Desplaza automáticamente al final del texto

    def reset_game(self):
        self.text_widget.delete('1.0', tk.END)  # Limpia el text_widget
        self.driver = Driver(self.update_message)  # Reinicia el juego
        self.start_battle()

    def play_sound(self, sound_file):
        sound_path = Path("rsc/sounds") / sound_file
        winsound.PlaySound(str(sound_path), winsound.SND_ASYNC)

    def show_image(self, image_file):
        image_path = Path("rsc/imgs") / image_file
        # Cargar la imagen PNG con Pillow
        self.my_image = Image.open(image_path)
        self.photo_image = ImageTk.PhotoImage(self.my_image)
        # Crear un widget Label para mostrar la imagen
        # Si el widget Label ya existe, actualiza la imagen
        if hasattr(self, 'image_label'):
            self.image_label.config(image=self.photo_image)
        else:
            # De lo contrario, crea el widget Label y muéstralo
            self.image_label = tk.Label(self.image_frame, image=self.photo_image)
            self.image_label.pack(padx=10, pady=10)

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()