# config/settings.py
from typing import Dict, Any

WINDOW_CONFIG = {
    "width": 1400,
    "height": 800,
    "title": "Advanced Ecosystem Simulator",
    "fps": 60
}

COLORS = {
    "background": (255, 255, 255),
    "text": (0, 0, 0),
    "graph_bg": (240, 240, 240),
    "graph_border": (200, 200, 200)
}

SPECIES_CONFIG = {
    "Tree": {
        "color": (34, 139, 34),
        "size": 15,
        "diet": "Plant",
        "optimal_temp": 20,
        "energy_consumption": 0.1,      # 增加能量消耗
        "lifespan": 1000,
        "reproduction_rate": 0.005,     # 增加繁殖率
        "mutation_chance": 0.1,
        "min_reproduction_energy": 60,   # 降低繁殖能量要求
        "competition_radius": 50,        # 添加竞争范围
    },
    "Grass": {
        "color": (124, 252, 0),
        "size": 5,
        "diet": "Plant",
        "optimal_temp": 25,
        "energy_consumption": 0.08,      # 增加能量消耗
        "lifespan": 500,
        "reproduction_rate": 0.008,      # 增加繁殖率
        "mutation_chance": 0.1,
        "min_reproduction_energy": 50,   # 降低繁殖能量要求
        "competition_radius": 30,        # 添加竞争范围
    },
    "Rabbit": {
        "color": (169, 169, 169),  # 灰色
        "size": 10,
        "diet": "Herbivore",
        "optimal_temp": 15,
        "energy_consumption": 0.3,
        "lifespan": 300,
        "reproduction_rate": 0.006,  # 增加繁殖率
        "mutation_chance": 0.1,
        "min_reproduction_energy": 65,  # 降低繁殖能量要求
    },
    "Deer": {
        "color": (139, 69, 19),  # 棕色
        "size": 20,
        "diet": "Herbivore",
        "optimal_temp": 20,
        "energy_consumption": 0.4,
        "lifespan": 400,
        "reproduction_rate": 0.004,  # 增加繁殖率
        "mutation_chance": 0.1,
        "min_reproduction_energy": 70,  # 降低繁殖能量要求
    },
    "Wolf": {
        "color": (128, 0, 0),  # 深红色
        "size": 25,
        "diet": "Carnivore",
        "optimal_temp": 10,
        "energy_consumption": 0.5,
        "lifespan": 500,
        "reproduction_rate": 0.003,  # 增加繁殖率
        "mutation_chance": 0.1,
        "min_reproduction_energy": 75,  # 降低繁殖能量要求
    }
}

INITIAL_POPULATION = {
    "Tree": 50,    # 增加初始数量
    "Grass": 100,  # 增加初始数量
    "Rabbit": 15,
    "Deer": 8,
    "Wolf": 3
}