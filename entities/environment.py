# entities/environment.py
from enum import Enum
from dataclasses import dataclass
import random

class Weather(Enum):
    SUNNY = "Sunny"
    RAINY = "Rainy"
    CLOUDY = "Cloudy"
    STORMY = "Stormy"

class Season(Enum):
    SPRING = "Spring"
    SUMMER = "Summer"
    FALL = "Fall"
    WINTER = "Winter"

# entities/environment.py
@dataclass
class EnvironmentalFactors:
    temperature: float
    humidity: float
    sunlight: float
    water_level: float
    pollution: float = 0.0  # 添加污染属性，默认值为0

class Environment:
    def __init__(self):
        self.season = Season.SPRING
        self.weather = Weather.SUNNY
        self.time = 0
        self.factors = EnvironmentalFactors(
            temperature=20.0,
            humidity=0.5,
            sunlight=1.0,
            water_level=1.0
        )

    def update(self):
        self.time += 1
        self._update_season()
        self._update_weather()
        self._update_factors()

    def _update_season(self):
        # 每1000个时间单位更换季节
        if self.time % 1000 == 0:
            seasons = list(Season)
            current_idx = seasons.index(self.season)
            self.season = seasons[(current_idx + 1) % len(seasons)]

    def _update_weather(self):
        # 2%的概率改变天气
        if random.random() < 0.02:
            self.weather = random.choice(list(Weather))

    def _update_factors(self):
        # 根据季节和天气更新环境因素
        target_temp = {
            Season.SPRING: 20,
            Season.SUMMER: 30,
            Season.FALL: 15,
            Season.WINTER: 5
        }[self.season]

        # 温度渐变
        self.factors.temperature += (target_temp - self.factors.temperature) * 0.1

        # 天气影响
        weather_effects = {
            Weather.SUNNY: {"humidity": -0.02, "sunlight": 0.1, "water_level": -0.01},
            Weather.RAINY: {"humidity": 0.05, "sunlight": -0.1, "water_level": 0.05},
            Weather.CLOUDY: {"humidity": 0.01, "sunlight": -0.05, "water_level": 0},
            Weather.STORMY: {"humidity": 0.1, "sunlight": -0.2, "water_level": 0.1}
        }

        effects = weather_effects[self.weather]
        self.factors.humidity = max(0.1, min(1.0, self.factors.humidity + effects["humidity"]))
        self.factors.sunlight = max(0.1, min(1.0, self.factors.sunlight + effects["sunlight"]))
        self.factors.water_level = max(0.1, min(1.0, self.factors.water_level + effects["water_level"]))