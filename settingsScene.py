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

class SettingsScene:
    def __init__(self, screen, scene_manager):
        self.screen = screen
        self.scene_manager = scene_manager
        self.font = pygame.font.Font(None, 36)

        self.title_text = self.font.render("Settings", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen.get_width() // 2, 100))

        self.debug_mode_text = self.font.render("Debug Mode: Off", True, (255, 255, 255))
        self.debug_mode_rect = self.debug_mode_text.get_rect(center=(screen.get_width() // 2, 200))

        self.debug_mode = False

    def setup(self):
        pass

    def cleanup(self):
        pass

    def update(self):
        self.debug_mode_text = self.font.render(f"Debug Mode: {'On' if self.debug_mode else 'Off'}", True, (255, 255, 255))

    def render(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.debug_mode_text, self.debug_mode_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.handle_selection()

    def handle_selection(self):
        if self.debug_mode:
            print("Debug Mode Off")
            self.debug_mode = False
        else:
            print("Debug Mode On")
            self.debug_mode = True