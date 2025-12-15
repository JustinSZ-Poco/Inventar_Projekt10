import tkinter as tk
from tkinter import PhotoImage


def beim_klicken_passiert_das():
    print("Das Projekt startet")
# 1. Hauptfenster erstellen
root = tk.Tk()
root.title("Meine erste GUI")
root.geometry("1000x500") # Fenstergröße festlegen


img = tk.PhotoImage (file = "Screenshot 2025-12-15 130309.png")
# 2. Widgets hinzufügen (z.B. ein Label)
label = tk.Label(root, text="Hallo Welt!")
#label.pack(pady=20) # Widget im Fenster platzieren
label_mit_Bild= tk.Label(root, image=img)
#button = tk.Button(root, text="Start", command=beim_klicken_passiert_das)
label_mit_Bild.pack(pady=20)
#button.pack(pady=40)
# 3. Hauptschleife starten (hält das Fenster offen)
root.mainloop()


