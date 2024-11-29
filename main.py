# main.py
import random
import pygame
import sys
from config import WINDOW_CONFIG, SPECIES_CONFIG, INITIAL_POPULATION, COLORS
from simulation.ecosystem import Ecosystem
from visualization.renderer import Renderer

class Application:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_CONFIG["width"], WINDOW_CONFIG["height"]))
        pygame.display.set_caption(WINDOW_CONFIG["title"])
        self.clock = pygame.time.Clock()
        
        self.ecosystem = Ecosystem({
            "WINDOW_CONFIG": WINDOW_CONFIG,
            "SPECIES_CONFIG": SPECIES_CONFIG,
            "INITIAL_POPULATION": INITIAL_POPULATION
        })
        
        self.renderer = Renderer(self.screen, {
            "WINDOW_CONFIG": WINDOW_CONFIG,
            "COLORS": COLORS
        })
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_keypress(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)

   # main.py 中的增强版按键控制
    def handle_keypress(self, key):
        if key == pygame.K_SPACE:
            self.ecosystem.toggle_pause()  # 暂停/继续
        elif key == pygame.K_ESCAPE:
            self.running = False    # 退出
        elif key == pygame.K_1:
            # 添加树
            x, y = pygame.mouse.get_pos()
            self.ecosystem.add_organism("Tree", x, y)
        elif key == pygame.K_2:
            # 添加草
            x, y = pygame.mouse.get_pos()
            self.ecosystem.add_organism("Grass", x, y)
        elif key == pygame.K_3:
            # 添加兔子
            x, y = pygame.mouse.get_pos()
            self.ecosystem.add_organism("Rabbit", x, y)
        elif key == pygame.K_4:
            # 添加鹿
            x, y = pygame.mouse.get_pos()
            self.ecosystem.add_organism("Deer", x, y)
        elif key == pygame.K_5:
            # 添加狼
            x, y = pygame.mouse.get_pos()
            self.ecosystem.add_organism("Wolf", x, y)

    def handle_mouse_click(self, event):
        x, y = event.pos
        # 随机添加一种生物
        species_name = random.choice(list(SPECIES_CONFIG.keys()))
        self.ecosystem.add_organism(species_name, x, y)

    def run(self):
        while self.running:
            self.handle_events()
            self.ecosystem.update()
            self.renderer.render(self.ecosystem)
            self.clock.tick(WINDOW_CONFIG["fps"])

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = Application()
    app.run()