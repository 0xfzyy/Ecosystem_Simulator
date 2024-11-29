# visualization/renderer.py
import pygame
import math
import random
from typing import Dict, List

class Renderer:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        # 使用更好看的字体
        try:
            self.font = pygame.font.Font("assets/fonts/Roboto-Bold.ttf", 36)
            self.small_font = pygame.font.Font("assets/fonts/Roboto-Regular.ttf", 24)
        except:
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
            
        self.graph_rect = pygame.Rect(
            self.config["WINDOW_CONFIG"]["width"] - 300,
            self.config["WINDOW_CONFIG"]["height"] - 200,
            280,
            180
        )
        
        # 创建更漂亮的背景
        self.background = self._create_background()
        self.clouds = self._create_clouds()
        self.animation_timer = 0
        
        # 粒子系统
        self.particles = []
        
    def _create_clouds(self):
        clouds = []
        for _ in range(5):
            x = random.randint(0, self.config["WINDOW_CONFIG"]["width"])
            y = random.randint(0, 200)
            speed = random.uniform(0.2, 0.5)
            clouds.append({"x": x, "y": y, "speed": speed})
        return clouds

    def _create_background(self):
        width = self.config["WINDOW_CONFIG"]["width"]
        height = self.config["WINDOW_CONFIG"]["height"]
        background = pygame.Surface((width, height))
        
        # 创建渐变天空
        for y in range(height):
            progress = y / height
            if progress < 0.4:  # 上部分天空
                color = self._blend_colors((135, 206, 235), (100, 149, 237), progress/0.4)
            else:  # 下部分地面
                ground_progress = (progress - 0.4) / 0.6
                color = self._blend_colors((34, 139, 34), (0, 100, 0), ground_progress)
            pygame.draw.line(background, color, (0, y), (width, y))

        # 添加远景山脉
        self._draw_mountains(background)
        
        # 添加装饰性元素
        self._add_decorative_elements(background)
        
        return background

    def _blend_colors(self, color1, color2, progress):
        return tuple(int(c1 + (c2 - c1) * progress) for c1, c2 in zip(color1, color2))

    def _draw_mountains(self, surface):
        width = self.config["WINDOW_CONFIG"]["width"]
        height = self.config["WINDOW_CONFIG"]["height"]
        points = [(0, height * 0.7)]
        
        # 生成山脉轮廓
        for x in range(0, width + 50, 50):
            y = height * 0.7 - random.randint(50, 150)
            points.append((x, y))
        points.append((width, height * 0.7))
        
        # 绘制山脉
        pygame.draw.polygon(surface, (100, 100, 100), points)
        
        # 添加雪顶
        snow_points = [(p[0], p[1] - 10) for p in points[1:-1] if p[1] < height * 0.6]
        for p in snow_points:
            pygame.draw.circle(surface, (255, 255, 255), p, 5)

    def _add_decorative_elements(self, surface):
        width = self.config["WINDOW_CONFIG"]["width"]
        height = self.config["WINDOW_CONFIG"]["height"]
        
        # 添加随机的小花
        for _ in range(100):
            x = random.randint(0, width)
            y = random.randint(int(height * 0.7), height)
            color = random.choice([
                (255, 192, 203),  # 粉色
                (255, 255, 0),    # 黄色
                (255, 0, 0),      # 红色
                (255, 165, 0)     # 橙色
            ])
            pygame.draw.circle(surface, color, (x, y), 2)

    def _update_clouds(self):
        width = self.config["WINDOW_CONFIG"]["width"]
        for cloud in self.clouds:
            cloud["x"] += cloud["speed"]
            if cloud["x"] > width + 100:
                cloud["x"] = -100
                cloud["y"] = random.randint(0, 200)

    def _draw_cloud(self, surface, x, y):
        color = (255, 255, 255, 150)
        positions = [(0, 0), (20, 0), (40, 0), (10, -10), (30, -10)]
        for px, py in positions:
            pygame.draw.circle(surface, color, (int(x + px), int(y + py)), 20)

    def _add_particle(self, x, y, color):
        self.particles.append({
            "x": x,
            "y": y,
            "dx": random.uniform(-1, 1),
            "dy": random.uniform(-2, 0),
            "life": 30,
            "color": color
        })

    def _update_particles(self):
        for particle in self.particles[:]:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.particles.remove(particle)

    def render(self, ecosystem):
        # 更新动画
        self.animation_timer = (self.animation_timer + 1) % 360
        self._update_clouds()
        self._update_particles()
        
        # 绘制基础背景
        self.screen.blit(self.background, (0, 0))
        
        # 绘制云
        cloud_surface = pygame.Surface(
            (self.config["WINDOW_CONFIG"]["width"], 
             self.config["WINDOW_CONFIG"]["height"]), 
            pygame.SRCALPHA
        )
        for cloud in self.clouds:
            self._draw_cloud(cloud_surface, cloud["x"], cloud["y"])
        self.screen.blit(cloud_surface, (0, 0))
        
        # 绘制生物（按Y坐标排序）
        sorted_organisms = sorted(ecosystem.organisms, key=lambda x: x.y)
        for org in sorted_organisms:
            self._render_organism(org)
            
        # 绘制粒子
        for particle in self.particles:
            alpha = int(255 * (particle["life"] / 30))
            color = (*particle["color"][:3], alpha)
            pygame.draw.circle(
                self.screen, 
                color, 
                (int(particle["x"]), int(particle["y"])), 
                2
            )
        
        # 绘制UI
        self._render_ui(ecosystem)
        
        pygame.display.flip()

    def _render_organism(self, org):
        size = int(org.species_config["size"] * org.genetics.size_modifier)
        base_color = org.species_config["color"]
        
        # 添加简单的动画效果
        if org.species_config["diet"] != "Plant":
            offset_y = math.sin(self.animation_timer * 0.1 + org.x * 0.1) * 2
        else:
            offset_y = math.sin(self.animation_timer * 0.05 + org.x * 0.1) * 1
        
        # 根据健康状况调整颜色透明度
        alpha = min(255, max(0, int(255 * (org.health / 100))))
        color = (*base_color, alpha)
        
        # 绘制生物
        surface, pos = self._draw_organism(
            int(org.x), 
            int(org.y + offset_y), 
            size, 
            color, 
            org.species_config["diet"]
        )
        self.screen.blit(surface, pos)
        
        # 添加粒子效果
        if random.random() < 0.1:
            self._add_particle(org.x, org.y, org.species_config["color"])

    def _draw_organism(self, x, y, size, color, species_type):
        """绘制更详细的生物图形"""
        surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        
        if species_type == "Plant":
            # 绘制植物
            # 茎
            stem_color = (0, 100, 0)
            pygame.draw.rect(surface, stem_color, (size-2, size, 4, size))
            # 叶子
            leaf_color = color
            pygame.draw.circle(surface, leaf_color, (size, size-2), size//2)
            
        elif species_type == "Herbivore":
            # 绘制食草动物
            # 身体
            pygame.draw.ellipse(surface, color, (size//2, size//2, size, size//1.5))
            # 头部
            head_pos = (size//2 + size, size//2 + size//4)
            pygame.draw.circle(surface, color, head_pos, size//3)
            # 耳朵
            ear_color = (min(color[0] + 20, 255), min(color[1] + 20, 255), min(color[2] + 20, 255))
            pygame.draw.ellipse(surface, ear_color, (head_pos[0], head_pos[1]-size//2, 4, size//3))
            
        elif species_type == "Carnivore":
            # 绘制食肉动物
            # 身体
            pygame.draw.ellipse(surface, color, (size//2, size//2, size*1.2, size//1.5))
            # 头部
            head_pos = (size//2 + size*1.2, size//2 + size//4)
            pygame.draw.circle(surface, color, head_pos, size//3)
            # 尾巴
            pygame.draw.ellipse(surface, color, (size//4, size//2 + size//4, size//2, size//4))
        
        return surface, (x - size, y - size)

    def _render_ui(self, ecosystem):
        # 创建半透明的UI面板
        ui_surface = pygame.Surface((300, 200), pygame.SRCALPHA)
        pygame.draw.rect(ui_surface, (0, 0, 0, 128), ui_surface.get_rect())
        
        # 渲染环境信息
        info_texts = [
            f"Season: {ecosystem.environment.season.value}",
            f"Weather: {ecosystem.environment.weather.value}",
            f"Temperature: {ecosystem.environment.factors.temperature:.1f}°C",
            f"Humidity: {ecosystem.environment.factors.humidity:.2f}"
        ]
        
        for i, text in enumerate(info_texts):
            text_surface = self.font.render(text, True, (255, 255, 255))
            ui_surface.blit(text_surface, (10, 10 + i * 30))
            
        self.screen.blit(ui_surface, (10, 10))
        
        # 渲染统计图表
        self._render_statistics(ecosystem.statistics)
        self._render_graph(ecosystem.statistics)

    def _render_statistics(self, statistics):
        y_pos = 10
        colors = {
            "plants": (34, 139, 34),
            "herbivores": (0, 0, 255),
            "carnivores": (255, 0, 0)
        }
        
        for category, history in statistics.items():
            if history:
                count = history[-1]
                text = f"{category.capitalize()}: {count}"
                surface = self.font.render(text, True, colors[category])
                self.screen.blit(surface, 
                               (self.config["WINDOW_CONFIG"]["width"] - 200, y_pos))
                y_pos += 30

    def _render_graph(self, statistics):
        # 绘制图表背景
        pygame.draw.rect(self.screen, (240, 240, 240), self.graph_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.graph_rect, 2)

        colors = {
            "plants": (34, 139, 34),
            "herbivores": (0, 0, 255),
            "carnivores": (255, 0, 0)
        }

        for category, history in statistics.items():
            if not history:
                continue

            # 找到最大值用于缩放
            max_value = max(max(stat) for stat in statistics.values() if stat)
            
            # 计算点的位置
            points = []
            for i, value in enumerate(history):
                x = self.graph_rect.left + (i * self.graph_rect.width / 100)
                y = self.graph_rect.bottom - (value * self.graph_rect.height / 
                                            (max_value + 1))
                points.append((int(x), int(y)))

            # 绘制折线
            if len(points) > 1:
                pygame.draw.lines(self.screen, colors[category], False, points, 2)