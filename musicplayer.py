#Trouver les modules a importer 
#Tkinter ou pygame?
#OS?
#Faire la logique
#Interface graphique
#Peut etre faire vraiment ça car ca serait bien d'avoir un media player autre que pot player, VLC ou autres qui datent trop
import os
import tkinter as tk
from tkinter import filedialog
import pygame

class LecteurAudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Lecteur Audio")

        self.playlist = []

        pygame.init()
        pygame.mixer.init()

        self.current_track = tk.StringVar()
        self.current_track.set("Aucune piste sélectionnée")

        self.create_widgets()

    def create_widgets(self):
        # Boutons
        tk.Button(self.root, text="Choisir une piste", command=self.choose_track).pack(pady=10)
        tk.Button(self.root, text="Lancer la lecture", command=self.play).pack(pady=5)
        tk.Button(self.root, text="Mettre en pause", command=self.pause).pack(pady=5)
        tk.Button(self.root, text="Arrêter la lecture", command=self.stop).pack(pady=5)
        tk.Button(self.root, text="Volume +", command=self.volume_up).pack(pady=5)
        tk.Button(self.root, text="Volume -", command=self.volume_down).pack(pady=5)
        tk.Button(self.root, text="Lire en boucle", command=self.toggle_loop).pack(pady=5)
        tk.Button(self.root, text="Piste suivante", command=self.next_track).pack(pady=5)
        tk.Button(self.root, text="Sélection aléatoire", command=self.random_track).pack(pady=5)

        # Barre de progression
        self.progress_bar = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, length=300, label="Progression")
        self.progress_bar.pack(pady=10)

        # Étiquette pour afficher la piste en cours
        tk.Label(self.root, textvariable=self.current_track).pack(pady=10)

    def choose_track(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers audio", "*.mp3;*.wav")])
        if file_path:
            self.playlist.append(file_path)
            self.current_track.set(os.path.basename(file_path))

    def play(self):
        if self.playlist:
            pygame.mixer.music.load(self.playlist[0])
            pygame.mixer.music.play()
            self.root.after(100, self.update_progress)

    def pause(self):
        pygame.mixer.music.pause()

    def stop(self):
        pygame.mixer.music.stop()

    def volume_up(self):
        current_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(min(1.0, current_volume + 0.1))

    def volume_down(self):
        current_volume = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(max(0.0, current_volume - 0.1))

    def toggle_loop(self):
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        if pygame.mixer.music.get_endevent() == pygame.USEREVENT:
            pygame.mixer.music.play(-1)  # -1 will loop the music indefinitely

    def update_progress(self):
        if pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000  # convert to seconds
            total_time = pygame.mixer.Sound(self.playlist[0]).get_length()
            progress_percent = (current_time / total_time) * 100
            self.progress_bar.set(progress_percent)
            self.root.after(100, self.update_progress)

    def next_track(self):
        if len(self.playlist) > 1:
            self.playlist.pop(0)
            self.play()
        else:
            self.stop()

    def random_track(self):
        if self.playlist:
            import random
            random.shuffle(self.playlist)
            self.play()

if __name__ == "__main__":
    root = tk.Tk()
    lecteur_audio = LecteurAudio(root)
    root.mainloop()