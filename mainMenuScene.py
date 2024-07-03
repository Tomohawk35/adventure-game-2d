# MainMenuScene.py

'''
MIT License

Copyright (c) 2024 Chester Allyn Cadiz Tag-at

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import pygame

class MainMenuScene:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.font = pygame.font.Font(None, 36)

        self.title_text = self.font.render("Game Title", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, 100))

        self.menu_options = [
            "Continue",
            "New Game",
            "Settings",
            "Quit"
        ]
        self.selected_option = 0


    def setup(self):
        pass

    def cleanup(self):
        pass

    def update(self):
        pass

    def render(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.title_text, self.title_rect)

        for i, option in enumerate(self.menu_options):
            color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 200 + i * 50))
            self.screen.blit(text, rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self.handle_selection()

    def handle_selection(self):

        if self.selected_option == 0:
            print("Continue selected")
            # Add continue logic here
        elif self.selected_option == 1:
            print("New Game selected")
            self.scene_manager.switch_scene("NewGameScene")
        elif self.selected_option == 2:
            print("Settings selected")
            self.scene_manager.switch_scene("SettingsScene")
        elif self.selected_option == 3:
            print("Quit selected")
            pygame.quit()
            sys.exit()