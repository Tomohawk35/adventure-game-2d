# SceneManager.py

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
import sys

class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.scenes = {}
        self.current_scene = None

    def add_scene(self, scene_name, scene):
        self.scenes[scene_name] = scene

    def switch_scene(self, scene_name):
        if self.current_scene:
            self.current_scene.cleanup()

        self.current_scene = self.scenes.get(scene_name)

        if self.current_scene:
            self.current_scene.setup()

    def run_current_scene(self):
        if self.current_scene:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.current_scene.handle_event(event)

            self.current_scene.update()
            self.current_scene.render()
