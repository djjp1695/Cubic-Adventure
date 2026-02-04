import os
import sys

import pygame
from pygame import mixer

"""Classe qui gère tout ce qui concerne la gestion de la musique et des sons"""

@staticmethod
def resource_path(relative_path):
    """
    Retourne le chemin absolu vers un fichier ou dossier.
    Compatible développement et PyInstaller --onefile
    """
    if hasattr(sys, "_MEIPASS"):  # PyInstaller onefile
        base_path = sys._MEIPASS
    else:  # développement normal
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MusicHandler:
    errorsList = []
    """Définition des constantes pour chaque son ou musique utilisée dans le jeu
    Tous les sons sont en provenance de https://pixabay.com/sound-effects/
    plateforme libre de droits"""
    GAME_MUSIC = resource_path( os.path.join("Assets", 'Music/2019-12-11_-_Retro_Platforming_-_David_Fesliyan.mp3'))
    GAME_OVER_SOUND = resource_path(os.path.join("Assets", 'Music/game-over-38511.mp3'))
    GAME_WIN_SOUND = resource_path(os.path.join("Assets", 'Music/8-bit-video-game-win-level-sound-version-1-145827.mp3'))
    JUMP_SOUND = resource_path(os.path.join("Assets", 'Music/retro-jump-3-236683.mp3'))
    ENEMY_KILL_SOUND = resource_path(os.path.join("Assets", 'Music/knife-demo-309903.mp3'))

    """Joue la musique du jeu par défaut, lors de l'initialisation du jeu"""

    def __init__(self):
        self.__game_over_sound_played = False
        self.__game_win_sound_played = False
        mixer.init()
        try:
            self.game_over_sound = mixer.Sound(self.GAME_OVER_SOUND)
        except Exception as e:
            self.errorsList.append(e)
        try:
            self.game_win_sound = mixer.Sound(self.GAME_WIN_SOUND)
        except Exception as e:
            self.errorsList.append(e)
        try:
            self.jump_sound = mixer.Sound(self.JUMP_SOUND)
        except Exception as e:
            self.errorsList.append(e)
        try:
            self.game_win_sound = mixer.Sound(self.GAME_WIN_SOUND)
        except Exception as e:
            self.errorsList.append(e)
        try:
            self.jump_sound = mixer.Sound(self.JUMP_SOUND)
        except Exception as e:
            self.errorsList.append(e)
        try:
            self.enemy_kill_sound = mixer.Sound(self.ENEMY_KILL_SOUND)
        except Exception as e:
            self.errorsList.append(e)
        try:
            mixer.music.load(self.GAME_MUSIC)
            mixer.music.play(-1)
        except Exception as e:
            self.errorsList.append(e)

    """Remplace la musique par défaut, par celle de la défaite"""

    def play_game_over_sound(self):
        if not self.__game_over_sound_played:
            if hasattr(self, 'game_over_sound'):
                mixer.music.fadeout(500)
                self.game_over_sound.play()
                self.__game_over_sound_played = True

    """Remplace la musique par défaut, par celle de la victoire"""

    def play_win_music(self):
        if not self.__game_win_sound_played:
            if hasattr(self, 'game_win_sound'):
                mixer.music.fadeout(500)
                self.game_win_sound.play()
                self.__game_win_sound_played = True

    """Joue le son de saut, à chaque fois que le personnage effectue un saut"""

    def play_jump_sound(self):
        if hasattr(self, 'jump_sound'):
            self.jump_sound.play()

    """Joue le son d'élimination de l'ennemie lorsque celui-ci est touché"""

    def play_enemy_kill_sound(self):
        # if not self.__game_win_sound_played:
        if hasattr(self, 'enemy_kill_sound'):
            self.enemy_kill_sound.play()


