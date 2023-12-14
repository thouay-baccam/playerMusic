import os
import pygame
from tkinter import Tk, Frame, Label, Button, Listbox, filedialog, ttk, Menu, END, ACTIVE

class LecteurMusique:
    def __init__(self, maitre):
        # Initialisation de l'interface
        self.maitre = maitre
        maitre.title("LMPLV")  # LMPLV : Lecteur Musique Pour Les Vieux 
        maitre.geometry("600x375")
        maitre.configure(bg='light gray') # L'interface en mode Windows 95/98, old school. 

        # Initialisation de Pygame et Pygame.mixer
        pygame.init()
        pygame.mixer.init()

        # Liste des chansons à lire
        self.liste_lecture = Listbox(maitre, bg='white', fg='black', selectbackground='blue', selectforeground='white', width=50)
        self.liste_lecture.pack(pady=10)

        # Boutons Lecture/Arrêt
        self.boutons_lire_arreter = self.creer_boutons_lire_arreter(maitre)
        self.boutons_lire_arreter.pack(pady=5)

        # Barre de progression
        self.barre_progression = ttk.Scale(maitre, orient='horizontal', length=400, from_=0, to=100, value=0, command=self.definir_progression)
        self.barre_progression.pack(pady=10)

        # Boutons Pause/Reprendre/Suivant/Précédent
        self.boutons = self.creer_boutons(maitre)
        self.etiquette_etat = Label(maitre, text="", bg='light gray', fg='black')
        self.etiquette_etat.pack(pady=5)

        # Slider de volume
        self.slider_volume = ttk.Scale(maitre, orient='horizontal', length=100, from_=0, to=1, command=self.regler_volume)
        self.slider_volume.set(pygame.mixer.music.get_volume())
        self.slider_volume.place(relx=0.7, rely=0.54, anchor="center")

        # Barre de menu
        self.barre_menu = self.creer_barre_menu()

        # Listes des chemins de chansons et dossier de musique
        self.chemins_liste_lecture = []
        self.dossier_musique = ""

    def creer_boutons_lire_arreter(self, cadre):
        # Création des boutons Lecture et Arrêt
        cadre_boutons = Frame(cadre, bg='light gray')
        cadre_boutons.pack(pady=10)

        bouton_lire = Button(cadre_boutons, text="Lire", command=self.lire_musique, bg='gray', fg='black')
        bouton_lire.grid(row=0, column=0, padx=5)

        bouton_arreter = Button(cadre_boutons, text="Arrêter", command=self.arret_musique, bg='gray', fg='black')
        bouton_arreter.grid(row=0, column=1, padx=5)

        return cadre_boutons

    def creer_boutons(self, cadre):
        # Création des boutons Pause/Reprendre/Suivant/Précédent
        noms_boutons = ["Pause", "Reprendre", "Suivant", "Précédent"]
        commandes_boutons = [self.pause_musique, self.reprise_musique, self.suivant_musique, self.precedent_musique]

        cadre_boutons = Frame(cadre, bg='light gray')
        cadre_boutons.pack(pady=10)

        boutons = {}
        for index, (nom, commande) in enumerate(zip(noms_boutons, commandes_boutons)):
            bouton = Button(cadre_boutons, text=nom, command=commande, bg='gray', fg='black')
            bouton.grid(row=0, column=index, padx=5)
            boutons[nom] = bouton

        return boutons

    def creer_barre_menu(self):
        # Création de la barre de menu
        barre_menu = Menu(self.maitre)
        self.maitre.config(menu=barre_menu)

        menu_fichier = Menu(barre_menu, tearoff=0)
        barre_menu.add_cascade(label="Fichier", menu=menu_fichier)
        menu_fichier.add_command(label="Ouvrir", command=self.ajouter_chanson)

        return barre_menu

    def ajouter_chanson(self):
        # Ajout d'une chanson à la liste de lecture
        chanson = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("Fichiers MP3", "*.mp3")])
        if chanson:
            nom_chanson, extension = os.path.splitext(os.path.basename(chanson))
            if extension.lower() == ".mp3":
                self.liste_lecture.insert(END, nom_chanson)
                self.chemins_liste_lecture.append(chanson)
                self.definir_dossier_musique(os.path.dirname(chanson))

    def definir_dossier_musique(self, dossier):
        # Définition du dossier de musique
        self.dossier_musique = dossier

    def lire_musique(self):
        # Lecture de la musique sélectionnée
        chanson_selectionnee = self.liste_lecture.get(ACTIVE)
        chemin_chanson = os.path.join(self.dossier_musique, chanson_selectionnee)

        try:
            pygame.mixer.music.load(chemin_chanson)
            pygame.mixer.music.play(loops=0)
            self.etiquette_etat.config(text=f"En cours de lecture : {chanson_selectionnee}")
            self.mise_a_jour_barre_progression()
        except pygame.error as e:
            self.etiquette_etat.config(text=f"Erreur lors de la lecture : {e}")

    def arret_musique(self):
        # Arrêt de la musique
        pygame.mixer.music.stop()
        self.etiquette_etat.config(text="Musique arrêtée")
        self.barre_progression.set(0)
        self.slider_volume.place_forget()

    def pause_musique(self):
        # Pause de la musique
        pygame.mixer.music.pause()
        self.etiquette_etat.config(text="Musique en pause")

    def reprise_musique(self):
        # Reprise de la musique
        pygame.mixer.music.unpause()
        self.etiquette_etat.config(text="Musique reprise")

    def suivant_musique(self):
        # Lecture de la chanson suivante dans la liste
        chanson_suivante = self.liste_lecture.curselection()[0] + 1
        if chanson_suivante < len(self.chemins_liste_lecture):
            self.liste_lecture.selection_clear(0, END)
            self.liste_lecture.activate(chanson_suivante)
            self.liste_lecture.selection_set(chanson_suivante)
            self.lire_musique()

    def precedent_musique(self):
        # Lecture de la chanson précédente dans la liste
        chanson_precedente = self.liste_lecture.curselection()[0] - 1
        if chanson_precedente >= 0:
            self.liste_lecture.selection_clear(0, END)
            self.liste_lecture.activate(chanson_precedente)
            self.liste_lecture.selection_set(chanson_precedente)
            self.lire_musique()

    def mise_a_jour_barre_progression(self):
        # Mise à jour de la barre de progression en fonction de la durée de la chanson
        duree = pygame.mixer.Sound(os.path.join(self.dossier_musique, self.liste_lecture.get(ACTIVE))).get_length()
        self.barre_progression.config(to=duree)

    def definir_progression(self, valeur):
        # Définition de la progression de la musique
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_pos(float(valeur))

    def regler_volume(self, valeur):
        # Réglage du volume de la musique
        pygame.mixer.music.set_volume(float(valeur))

if __name__ == "__main__":
    # Lancement de l'application
    racine = Tk()
    lecteur = LecteurMusique(racine)
    racine.mainloop()