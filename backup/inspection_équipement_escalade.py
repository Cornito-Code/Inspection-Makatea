import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os
from tkinter import messagebox
from fpdf import FPDF

class InspectionApp:
    def __init__(self, master):
        self.master = master
        master.title("Inspection de site d'escalade")
        self.dernier_site = None
        self.derniere_roche = None
        self.dernier_ancrage = None
        self.derniere_date = None
        script_dir = os.path.dirname(__file__)
        self.rapport_filename = os.path.join(script_dir, "rapport_inspection.txt")        
        self.derniere_date = None
        
        # Vérifier si un rapport existe déjà
        if not os.path.exists(self.rapport_filename):
            with open(self.rapport_filename, "w") as f:
                f.write("Rapport d'inspection\n\n")
                
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

        # Zone de texte pour le rapport
        self.rapport_text = tk.Text(self.tab_rapport, height=20, width=80)
        self.rapport_text.pack(pady=10)

        # Formulaire d'inspection
        self.create_inspection_form()
      
        # Bouton pour visualiser et exporter en PDF
        self.export_button = ttk.Button(self.tab_rapport, text="Exporter en PDF", command=self.export_to_pdf)
        self.export_button.pack(pady=10)

    def create_inspection_form(self):
        # Type de roche
        ttk.Label(self.tab_inspection, text="Type de roche:").grid(column=0, row=0, sticky=tk.W)
        self.type_roche = ttk.Combobox(self.tab_inspection, values=["Calcaire", "Granit", "Grès"])
        self.type_roche.grid(column=1, row=0)

        # Points d'ancrage
        ttk.Label(self.tab_inspection, text="Type d’ancrage:").grid(column=0, row=1, sticky=tk.W)
        self.type_ancrage = ttk.Combobox(self.tab_inspection, values=["Spit", "Broche", "Pitons"])
        self.type_ancrage.grid(column=1, row=1)

        # Nom du site
        ttk.Label(self.tab_inspection, text="Nom du site:").grid(column=0, row=2, sticky=tk.W)
        self.nom_site = tk.Entry(self.tab_inspection)
        self.nom_site.grid(column=1, row=2)

        # Nom de la voie
        ttk.Label(self.tab_inspection, text="Nom de la voie:").grid(column=0, row=3, sticky=tk.W)
        self.nom_voie = tk.Entry(self.tab_inspection)
        self.nom_voie.grid(column=1, row=3)

        # Nombre de points d'ancrage
        ttk.Label(self.tab_inspection, text="Nombre de points d'ancrage:").grid(column=0, row=4, sticky=tk.W)
        self.nombre_points = tk.Entry(self.tab_inspection)
        self.nombre_points.grid(column=1, row=4)

        # Section des ancrages dynamiques
        self.ancrages_frame = ttk.Frame(self.tab_inspection)
        self.ancrages_frame.grid(column=0, row=5, columnspan=2, pady=10)
        
        self.ancrage_entries = []
        self.add_ancrage_button = ttk.Button(self.tab_inspection, text="Ajouter un ancrage", command=self.add_ancrage)
        self.add_ancrage_button.grid(column=0, row=6, columnspan=2, pady=5)

        # Relais 
        relais_frame = ttk.Frame(self.tab_inspection)
        relais_frame.grid(column=0, row=7, columnspan=2, sticky=tk.W, pady=2)

        ttk.Label(relais_frame, text="Relais:").grid(column=0, row=0, sticky=tk.W, padx=(0, 5))

        self.relais_chaine = tk.BooleanVar()
        self.relais_anneau = tk.BooleanVar()
        self.relais_maillon = tk.BooleanVar()

        ttk.Checkbutton(relais_frame, text="Chaîne", variable=self.relais_chaine).grid(column=1, row=0, sticky=tk.W, padx=2)
        ttk.Checkbutton(relais_frame, text="Anneau", variable=self.relais_anneau).grid(column=2, row=0, sticky=tk.W, padx=2)
        ttk.Checkbutton(relais_frame, text="Maillon rapide", variable=self.relais_maillon).grid(column=3, row=0, sticky=tk.W, padx=2)

        ttk.Label(relais_frame, text="Autre:").grid(column=4, row=0, sticky=tk.W, padx=(10, 2))
        self.relais_autre = tk.Entry(relais_frame, width=12)
        self.relais_autre.grid(column=5, row=0, sticky=tk.W)

        # Stabilité générale du site
        ttk.Label(self.tab_inspection, text="Stabilité générale du site").grid(column=0, row=8, sticky=tk.W)

        self.fissures = tk.BooleanVar()
        ttk.Checkbutton(self.tab_inspection, text="Fissures visibles", variable=self.fissures).grid(column=0, row=9, sticky=tk.W)

        self.roches_instables = tk.BooleanVar()
        ttk.Checkbutton(self.tab_inspection, text="Roches instables", variable=self.roches_instables).grid(column=0, row=10, sticky=tk.W)
       
        # Ajout au rapport
        self.add_to_report_button = ttk.Button(self.tab_inspection, text="Ajouter au rapport", command=self.add_to_report)
        self.add_to_report_button.grid(column=0, row=12, columnspan=2, pady=5)

    def add_ancrage(self):
        row = len(self.ancrage_entries)
        frame = ttk.Frame(self.ancrages_frame)
        frame.grid(column=0, row=row, pady=2, sticky=tk.W)

        ttk.Label(frame, text=f"Ancrage numéro:").pack(side=tk.LEFT)
        ancrage_num = tk.Entry(frame, width=5)
        ancrage_num.pack(side=tk.LEFT, padx=5)

        corrosion_var = tk.BooleanVar()
        corrosion_cb = ttk.Checkbutton(frame, text="Corrosion", variable=corrosion_var)
        corrosion_cb.pack(side=tk.LEFT)

        instable_var = tk.BooleanVar()
        instable_cb = ttk.Checkbutton(frame, text="Instable", variable=instable_var)
        instable_cb.pack(side=tk.LEFT)

        usure_var = tk.BooleanVar()
        usure_cb = ttk.Checkbutton(frame, text="Usure", variable=usure_var)
        usure_cb.pack(side=tk.LEFT)

        surveiller_var = tk.BooleanVar()
        surveiller_cb = ttk.Checkbutton(frame, text="À surveiller", variable=surveiller_var)
        surveiller_cb.pack(side=tk.LEFT)

        remplacer_var = tk.BooleanVar()
        remplacer_cb = ttk.Checkbutton(frame, text="À remplacer", variable=remplacer_var)
        remplacer_cb.pack(side=tk.LEFT)

        # Stocker tous les éléments dans la liste (y compris le frame entier)
        self.ancrage_entries.append((frame, ancrage_num, corrosion_var, instable_var, usure_var, surveiller_var, remplacer_var))

    def add_to_report(self):
        site = self.nom_site.get()
        roche = self.type_roche.get()
        ancrage = self.type_ancrage.get()
        voie = self.nom_voie.get()
        nb_ancrages = self.nombre_points.get()

        from datetime import datetime

        # Obtenir la date du jour au format JJ/MM/AAAA
        date_du_jour = datetime.now().strftime("%d/%m/%Y")

        # Vérifier si on doit ajouter la date (uniquement si elle change)
        try:
            with open(self.rapport_filename, "r", encoding="utf-8") as f:
                contenu = f.read()
        except FileNotFoundError:
            contenu = ""

        if f"--- Rapport du {date_du_jour} ---" not in contenu:
            self.rapport_text.insert(tk.END, f"\n--- Rapport du {date_du_jour} ---\n")
            self.append_to_file(f"\n--- Rapport du {date_du_jour} ---\n")
            self.derniere_date = date_du_jour 

        # Ajouter les informations générales dans le rapport texte et fichier
        if (self.dernier_site is None or site != self.dernier_site or
            self.derniere_roche is None or roche != self.derniere_roche or
            self.derniere_ancrage is None or ancrage != self.derniere_ancrage):
            
            header = f"Site: {site}, Roche: {roche}, Ancrage: {ancrage}\n"
            self.append_to_file(header)
            self.rapport_text.insert(tk.END, header)  # Ajout dans la zone de texte
            self.dernier_site = site
            self.derniere_roche = roche
            self.derniere_ancrage = ancrage
        
        self.append_to_file(f"Voie: {voie}, Nombre d'ancrages: {nb_ancrages}\n")

        for entry in self.ancrage_entries:
            num = entry[1].get()
            conditions = [var.get() for var in entry[2:]] 
            labels = ["Corrosion", "Instable", "Usure", "À surveiller", "À remplacer"]
            conditions_str = ", ".join([labels[i] for i, val in enumerate(conditions[:len(labels)]) if val])
            self.append_to_file(f"  - Ancrage {num}: {conditions_str}\n")

        # Ajouter les infos de la voie et des ancrages au rapport
        voie = self.nom_voie.get()
        nb_ancrages = self.nombre_points.get()
        self.rapport_text.insert(tk.END, f"Voie: {voie}, Nombre d'ancrages: {nb_ancrages}\n")

        for entry in self.ancrage_entries:
            frame, ancrage_num, corrosion_var, instable_var, usure_var, surveiller_var, remplacer_var = entry
            
            num = ancrage_num.get()  # Récupération correcte du numéro d'ancrage
            conditions = [
                corrosion_var.get(),
                instable_var.get(),
                usure_var.get(),
                surveiller_var.get(),
                remplacer_var.get(),
            ]
            
            labels = ["Corrosion", "Instable", "Usure", "À surveiller", "À remplacer"]
            conditions_str = ", ".join([labels[i] for i, val in enumerate(conditions) if val])
            
            self.rapport_text.insert(tk.END, f"  - Ancrage {num}: {conditions_str}\n")

        # Ajouter les infos du relais
        relais_options = []
        if self.relais_chaine.get():
            relais_options.append("Chaîne")
        if self.relais_anneau.get():
            relais_options.append("Anneau")
        if self.relais_maillon.get():
            relais_options.append("Maillon rapide")

        relais_autre_val = self.relais_autre.get().strip()
        if relais_autre_val:
            relais_options.append(relais_autre_val)

        if relais_options:
            self.rapport_text.insert(tk.END, f"Relais: {', '.join(relais_options)}\n")
        else:
            self.rapport_text.insert(tk.END, "Relais: Absence de relais\n")
        self.append_to_file(f"Relais: {', '.join(relais_options)}\n" if relais_options else "Relais: Absence de relais\n")

        # Ajouter les infos sur la stabilité générale du site
        self.rapport_text.insert(tk.END, "Stabilité générale du site:\n")
        self.append_to_file("Stabilité générale du site:\n")

        stabilite_conditions = [
            (self.fissures.get(), "Fissures visibles"),
            (self.roches_instables.get(), "Roches instables"),
        ]
        
        for condition, label in stabilite_conditions:
            if condition:
                self.rapport_text.insert(tk.END, f"  - {label}\n")
                self.append_to_file(f"  - {label}\n")

        self.rapport_text.insert(tk.END, "\n")
        self.append_to_file("\n")

        # # Réinitialisation des champs après ajout
        self.nom_voie.delete(0, tk.END)
        self.nombre_points.delete(0, tk.END)
        self.fissures.set(False)
        self.roches_instables.set(False)
        self.relais_chaine.set(False)
        self.relais_anneau.set(False)
        self.relais_maillon.set(False)
        self.relais_autre.delete(0, tk.END)


        # Supprimer les entrées d'ancrage dynamiques de l'interface et de la liste
        for entry in self.ancrage_entries:
            frame = entry[0]  # Récupère le frame contenant l'ancrage
            frame.destroy()  # Détruit complètement l'affichage de l'ancrage (cases + champ)

        self.ancrage_entries.clear()  # Vide la liste après suppression
        
    def append_to_file(self, text):
        with open(self.rapport_filename, "a", encoding="utf-8") as f:
            f.write(text)

    def increment_report_file(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"rapport_inspection_{timestamp}.txt"
        script_dir = os.path.dirname(__file__)  
        backup_filepath = os.path.join(script_dir, backup_filename)
        with open(self.rapport_filename, "r", encoding="utf-8") as f:
            content = f.read()
        with open(backup_filepath, "w", encoding="utf-8") as f:
            f.write(content)
    
    def export_to_pdf(self):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        with open(self.rapport_filename, "r", encoding="utf-8") as f:
            for line in f:
                pdf.cell(0, 10, line.strip(), ln=True)
        
        pdf_filename = os.path.join(os.path.dirname(__file__), "rapport_inspection.pdf")
        pdf.output(pdf_filename)
        print(f"PDF enregistré sous : {pdf_filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InspectionApp(root)
    root.mainloop()
