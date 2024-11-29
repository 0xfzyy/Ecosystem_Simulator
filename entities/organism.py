# entities/organism.py
import random
from dataclasses import dataclass

@dataclass
class Genetics:
    size_modifier: float
    energy_efficiency: float
    temperature_tolerance: float
    reproduction_rate: float

class Organism:
    def __init__(self, x, y, species_config, config):  # 添加config参数
        self.x = x
        self.y = y
        self.species_config = species_config
        self.config = config  # 保存config引用
        self.genetics = self._generate_genetics()
        self.energy = 100
        self.health = 100
        self.age = 0
        self.reproduction_cooldown = 0
        self.partner = None
        print(f"Created {species_config['diet']} at ({x}, {y})")  # 添加调试信息

    def _generate_genetics(self):
        return Genetics(
            size_modifier=random.uniform(0.8, 1.2),
            energy_efficiency=random.uniform(0.8, 1.2),
            temperature_tolerance=random.uniform(0.8, 1.2),
            reproduction_rate=random.uniform(0.8, 1.2)
        )

    def update(self, environment, organisms):
        self.age += 1
        self._update_energy(environment)
        self._update_health(environment)
        self._handle_competition(organisms)
        self._find_partner(organisms)  # 确保调用寻找配偶
        self._move()
        self.reproduction_cooldown = max(0, self.reproduction_cooldown - 1)

    def _find_partner(self, organisms):
        if self.species_config["diet"] == "Plant" or self.partner:
            return

        for other in organisms:
            if (other != self and 
                other.species_config == self.species_config and 
                other.partner is None and  # 确保对方也没有配偶
                other.can_reproduce()):  # 检查对方是否可以繁殖
                
                distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
                if distance < 40:  # 增加检测范围
                    print(f"Found partner for {self.species_config['diet']}")  # 调试信息
                    self.partner = other
                    other.partner = self
                    break

    def _update_energy(self, environment):
        if self.species_config["diet"] == "Plant":
            # 植物能量获取受环境因素影响
            energy_gain = (
                environment.factors.sunlight * 0.5 +
                environment.factors.water_level * 0.3 +
                (1 - environment.factors.humidity) * 0.2  # 改用humidity代替pollution
            )
            
            # 根据季节调整能量获取
            if environment.season.value == "Winter":
                energy_gain *= 0.3
            elif environment.season.value == "Fall":
                energy_gain *= 0.7
            elif environment.season.value == "Spring":
                energy_gain *= 1.2
            
            # 能量消耗
            energy_loss = self.species_config["energy_consumption"]
            
            # 最终能量变化
            self.energy = max(0, min(100, self.energy + energy_gain - energy_loss))
        else:
            # 动物的能量更新保持不变
            base_consumption = self.species_config["energy_consumption"]
            actual_consumption = base_consumption / self.genetics.energy_efficiency
            self.energy = max(0, self.energy - actual_consumption)

    def _update_health(self, environment):
        # 温度影响健康
        temp_diff = abs(environment.factors.temperature - self.species_config["optimal_temp"])
        temp_damage = temp_diff * (1 - self.genetics.temperature_tolerance)
        self.health = max(0, self.health - temp_damage * 0.1)

        # 能量影响健康
        if self.energy < 20:
            self.health = max(0, self.health - 1)

    def _handle_competition(self, organisms):
        if self.species_config["diet"] != "Plant":
            return

        competition_radius = self.species_config["competition_radius"]
        nearby_plants = 0

        # 统计附近的植物数量
        for other in organisms:
            if other != self and other.species_config["diet"] == "Plant":
                distance = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
                if distance < competition_radius:
                    nearby_plants += 1

        # 根据竞争程度减少能量
        competition_factor = 0.1 * nearby_plants
        self.energy = max(0, self.energy - competition_factor)

    def _move(self):
        if self.species_config["diet"] == "Plant":
            # 植物不移动
            return
            
        # 获取移动速度
        speed = self.species_config.get("speed", 2.0)
        
        # 随机移动
        self.x += random.uniform(-speed, speed)
        
        # 如果是动物，确保它们在地面上移动
        ground_height = 0.7 * self.config["WINDOW_CONFIG"]["height"]  # 需要传入config
        
        # 添加一点垂直移动，但保持在合理范围内
        vertical_movement = random.uniform(-speed/2, speed/2)
        new_y = self.y + vertical_movement
        
        # 限制垂直移动范围
        min_height = ground_height - 50  # 动物最高可以跳到离地面50像素
        max_height = ground_height       # 不能低于地面
        
        self.y = max(min_height, min(new_y, max_height))
        
        # 限制水平移动范围（不超出屏幕）
        self.x = max(0, min(self.x, self.config["WINDOW_CONFIG"]["width"]))

    def can_reproduce(self):
        # 放宽繁殖条件
        if self.species_config["diet"] == "Plant":
            return (self.energy > 60 and  # 降低能量要求
                    self.health > 50 and  # 降低健康要求
                    self.reproduction_cooldown <= 0 and
                    random.random() < self.species_config["reproduction_rate"])
        else:
            # 动物的繁殖条件
            return (self.energy > 70 and
                    self.health > 60 and
                    self.reproduction_cooldown <= 0 and
                    self.partner is not None and  # 确保有配偶
                    random.random() < self.species_config["reproduction_rate"])

    def reproduce(self):
        if self.species_config["diet"] == "Plant":
            if self.can_reproduce():
                self.energy -= 30  # 减少能量消耗
                self.reproduction_cooldown = 50  # 减少冷却时间
                offspring = self._create_offspring()
                print(f"Plant reproduced at ({offspring.x}, {offspring.y})")  # 调试信息
                return offspring
        else:
            if self.partner and self.can_reproduce() and self.partner.can_reproduce():
                # 双方都消耗能量
                self.energy -= 30
                self.partner.energy -= 30
                self.reproduction_cooldown = 50
                self.partner.reproduction_cooldown = 50
                
                # 创建后代
                offspring = self._create_offspring()
                print(f"Animal reproduced at ({offspring.x}, {offspring.y})")  # 调试信息
                
                # 解除配偶关系
                self.partner.partner = None
                self.partner = None
                
                return offspring
        return None

    def _create_offspring(self):
        # 创建后代，包含基因突变
        offspring = Organism(
            x=self.x + random.uniform(-20, 20),
            y=self.y + random.uniform(-20, 20),
            species_config=self.species_config,
            config=self.config  # 传递config参数
        )
        
        # 基因突变
        if random.random() < self.species_config["mutation_chance"]:
            offspring.genetics.size_modifier *= random.uniform(0.9, 1.1)
            offspring.genetics.energy_efficiency *= random.uniform(0.9, 1.1)
            offspring.genetics.temperature_tolerance *= random.uniform(0.9, 1.1)
            offspring.genetics.reproduction_rate *= random.uniform(0.9, 1.1)

        return offspring