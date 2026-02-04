import os

from pygame import mixer

"""Classe qui gère tout ce qui concerne la gestion de la musique et des sons"""
class MusicHandler:
    """Définition des constantes pour chaque son ou musique utilisée dans le jeu
    Tous les sons sont en provenance de https://pixabay.com/sound-effects/
    plateforme libre de droits"""
    GAME_MUSIC =  os.path.join("Assets", 'Music/2019-12-11_-_Retro_Platforming_-_David_Fesliyan.mp3')
    GAME_OVER_SOUND = os.path.join("Assets", 'Music/game-over-38511.mp3')
    GAME_WIN_SOUND= os.path.join("Assets", 'Music/8-bit-video-game-win-level-sound-version-1-145827.mp3')
    JUMP_SOUND = os.path.join("Assets", 'Music/retro-jump-3-236683.mp3')
    ENEMY_KILL_SOUND = os.path.join("Assets", 'Music/knife-demo-309903.mp3')

    """Joue la musique du jeu par défaut, lors de l'initialisation du jeu"""
    def __init__(self):
        mixer.init()
        mixer.music.load(self.GAME_MUSIC)
        mixer.music.play(-1)
        self.__game_over_sound_played = False
        self.__game_win_sound_played=False

    """Remplace la musique par défaut, par celle de la défaite"""
    def play_game_over_sound(self):
        if not self.__game_over_sound_played:
            mixer.music.stop()
            mixer.music.load(self.GAME_OVER_SOUND)
            mixer.music.play()
            self.__game_over_sound_played = True

    """Remplace la musique par défaut, par celle de la victoire"""
    def play_win_music(self):
        if not self.__game_win_sound_played:
            mixer.music.stop()
            mixer.music.load(self.GAME_WIN_SOUND)
            mixer.music.play()
            self.__game_win_sound_played = True

    """Joue le son de saut, à chaque fois que le personnage effectue un saut"""
    def play_jump_sound(self):
        if not self.__game_win_sound_played:
            mixer.Sound(self.JUMP_SOUND).play()

    """Joue le son d'élimination de l'ennemie lorsque celui-ci est touché"""
    def play_enemy_kill_sound(self):
        if not self.__game_win_sound_played:
            mixer.Sound(self.ENEMY_KILL_SOUND).play()

