import pygame_menu

class Menu :
    def __init__(self, screen, title):
        self.screen = screen
        self.menu = pygame_menu.Menu(title, screen.get_width(), screen.get_height(), theme=pygame_menu.themes.THEME_BLUE)
    def show_menu(self):
        if not self.menu.is_enabled():
            self.menu.enable()
        self.menu.mainloop(self.screen)

    def close_menu(self):
        self.menu.disable()

class PauseMenu(Menu):
    def __init__(self, screen, restart_function):
        super().__init__(screen, "Pause")
        self.menu.add.button('Reprendre', self.menu.disable)
        self.menu.add.button('Recommencer', restart_function)
        self.menu.add.button('Quitter', pygame_menu.events.EXIT)
        self.screen = screen

class EndMenu(Menu):
    def __init__(self, screen, restart_function):
        super().__init__(screen, "Fin de la partie")
        self.restart_function = restart_function
        self.menu.add.button('Recommencer', self.restart_menu)
        self.menu.add.button('Quitter', pygame_menu.events.EXIT)

    def restart_menu(self):
        self.close_menu()
        self.restart_function()
