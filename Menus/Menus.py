import pygame
import pygame_menu

#Le menu est créé en fonction de la taille de l'écran du jeu
#Utilisation de l'héritage, car les deux menus ont les mêmes fonctions
#d'affichage et de fermeture
class Menu :
    def __init__(self, screen, title):
        self.showed = False
        self.screen = screen
        self.menu = pygame_menu.Menu(title, screen.get_width(), screen.get_height(), theme=pygame_menu.themes.THEME_BLUE)
    #Si le menu à déjà été fermé, il est à l'état "Disable",
    # alors on le réactive pour l'afficher
    def show_menu(self):
        if not self.menu.is_enabled():
            self.menu.enable()
        self.showed = True
        self.menu.mainloop(self.screen)

    def close_menu(self):
        self.showed = False
        self.menu.disable()

#Passage de la fonction de réinitialisation pour pouvoir l'éxécuter
class PauseMenu(Menu):
    def __init__(self, screen, restart_function):
        super().__init__(screen, "Pause")
        self.menu.add.button('Reprendre', self.menu.disable)
        self.menu.add.button('Recommencer', restart_function)
        self.menu.add.button('Quitter', pygame_menu.events.EXIT)
        self.screen = screen

#Passage de la fonction de réinitialisation pour pouvoir l'éxécuter
class EndMenu(Menu):
    def __init__(self, screen, restart_function):
        super().__init__(screen, "Fin de la partie")
        self.restart_function = restart_function
        self.menu.add.button('Recommencer', self.restart_menu)
        self.menu.add.button('Quitter', pygame_menu.events.EXIT)

    def restart_menu(self):
        self.close_menu()
        self.restart_function()
