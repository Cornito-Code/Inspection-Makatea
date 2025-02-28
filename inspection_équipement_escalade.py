import tkinter as tk
from tkinter import ttk

class InspectionApp:
    def __init__(self, master):
        self.master = master
        master.title("Inspection de site d'escalade")

        # Onglets
        self.tab_control = ttk.Notebook(master)
        self.tab_inspection = ttk.Frame(self.tab_control)
        self.tab_photos = ttk.Frame(self.tab_control)
        self.tab_rapport = ttk.Frame(self.tab_control)
        self.tab_comments = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_inspection, text='Inspection')
        self.tab_control.add(self.tab_photos, text='Photos')
        self.tab_control.add(self.tab_rapport, text='Rapport')
        self.tab_control.add(self.tab_comments, text='Commentaires')
        self.tab_control.pack(expand=1, fill='both')

        # Formulaire d'inspection
        self.create_inspection_form()

    def create_inspection_form(self):
        # Type de roche
        ttk.Label(self.tab_inspection, text="Type de roche:").grid(column=0, row=0, sticky=tk.W)
        self.type_roche = ttk.Combobox(self.tab_inspection, values=["Calcaire", "Granit", "Grès"])
        self.type_roche.grid(column=1, row=0)

        # Points d'ancrage
        ttk.Label(self.tab_inspection, text="Type d’ancrage:").grid(column=0, row=1, sticky=tk.W)
        self.type_ancrage = ttk.Combobox(self.tab_inspection, values=["Spit", "Broche", "Pitons"])
        self.type_ancrage.grid(column=1, row=1)

        ttk.Label(self.tab_inspection, text="Nombre de points d'ancrage:").grid(column=0, row=2, sticky=tk.W)
        self.nombre_points = tk.Entry(self.tab_inspection)
        self.nombre_points.grid(column=1, row=2)

        # Section des ancrages dynamiques
        self.ancrages_frame = ttk.Frame(self.tab_inspection)
        self.ancrages_frame.grid(column=0, row=3, columnspan=2, pady=10)

        self.ancrage_entries = []
        self.add_ancrage_button = ttk.Button(self.tab_inspection, text="Ajouter un ancrage", command=self.add_ancrage)
        self.add_ancrage_button.grid(column=0, row=4, columnspan=2, pady=5)

        # Stabilité générale du site
        ttk.Label(self.tab_inspection, text="Stabilité générale du site").grid(column=0, row=5, sticky=tk.W)

        self.fissures = tk.BooleanVar()
        ttk.Checkbutton(self.tab_inspection, text="Fissures visibles", variable=self.fissures).grid(column=0, row=7, sticky=tk.W)

        self.roches_instables = tk.BooleanVar()
        ttk.Checkbutton(self.tab_inspection, text="Roches instables", variable=self.roches_instables).grid(column=0, row=8, sticky=tk.W)

  #detail remarque ancrage
    def add_ancrage(self):
        row = len(self.ancrage_entries)
        frame = ttk.Frame(self.ancrages_frame)
        frame.grid(column=0, row=row, pady=2, sticky=tk.W)

        ttk.Label(frame, text=f"Ancrage numéro:").pack(side=tk.LEFT)
        ancrage_num = tk.Entry(frame, width=5)
        ancrage_num.pack(side=tk.LEFT, padx=5)

        corrosion_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Corrosion", variable=corrosion_var).pack(side=tk.LEFT)
        instable_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Instable", variable=instable_var).pack(side=tk.LEFT)
        usure_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Usure", variable=usure_var).pack(side=tk.LEFT)
        surveiller_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="A surveiller", variable=surveiller_var).pack(side=tk.LEFT)
        remplacer_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="A remplacer", variable=remplacer_var).pack(side=tk.LEFT)

        self.ancrage_entries.append((ancrage_num, corrosion_var, instable_var, usure_var))

if __name__ == "__main__":
    root = tk.Tk()
    app = InspectionApp(root)
    root.mainloop()