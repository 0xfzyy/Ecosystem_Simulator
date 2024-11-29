# simulation/ecosystem.py
import random
from typing import List, Dict
from entities import Environment, Organism

class Ecosystem:
    def __init__(self, config):
        self.config = config
        self.environment = Environment()
        self.organisms = []
        self.statistics = {"plants": [], "herbivores": [], "carnivores": []}
        self.paused = False
        
        # Define ground height
        self.ground_height = self.config["WINDOW_CONFIG"]["height"] * 0.7  # Ground is at 70% of the window height
        self.initialize_population()

    def initialize_population(self):
        for species_name, count in self.config["INITIAL_POPULATION"].items():
            for _ in range(count):
                self.add_organism(species_name)

    def add_organism(self, species_name, x=None, y=None):
        species_config = self.config["SPECIES_CONFIG"][species_name]
        
        # Randomly generate position if not specified
        if x is None:
            x = random.uniform(0, self.config["WINDOW_CONFIG"]["width"])
            
        # Determine y-coordinate based on organism type
        if y is None:
            if species_config["diet"] == "Plant":
                # Plants are generated on the ground
                y = self.ground_height
            else:
                # Animals are generated slightly above the ground
                y = random.uniform(
                    self.ground_height - 50,  # Slightly above ground
                    self.ground_height        # Ground level
                )

        # Ensure organisms are not generated outside the screen
        x = max(0, min(x, self.config["WINDOW_CONFIG"]["width"]))
        y = max(0, min(y, self.config["WINDOW_CONFIG"]["height"]))
        
        organism = Organism(x, y, species_config, self.config)  # Pass config
        self.organisms.append(organism)

    def update(self):
        if self.paused:
            return

        self.environment.update()
        self._update_organisms()
        self._handle_interactions()
        self._collect_statistics()

    def _update_organisms(self):
        # Update existing organisms
        for organism in self.organisms[:]:  # Use slicing to create a copy to avoid modifying the list during iteration
            organism.update(self.environment, self.organisms)
            
            # Handle death
            if organism.health <= 0 or organism.energy <= 0:
                self.organisms.remove(organism)
                continue
            
            # Handle reproduction
            offspring = organism.reproduce()
            if offspring:
                self.organisms.append(offspring)

    def _handle_interactions(self):
        for org in self.organisms:
            if org.species_config["diet"] == "Plant":
                continue

            # Find nearest food
            nearest_prey = None
            min_distance = float('inf')
            
            for potential_prey in self.organisms:
                if self._is_valid_prey(org, potential_prey):
                    distance = ((org.x - potential_prey.x) ** 2 + 
                              (org.y - potential_prey.y) ** 2) ** 0.5
                    if distance < min_distance:
                        min_distance = distance
                        nearest_prey = potential_prey

            # Prey if close enough
            if nearest_prey and min_distance < 20:
                org.energy = min(100, org.energy + 30)
                self.organisms.remove(nearest_prey)

    def _is_valid_prey(self, predator, prey):
        if predator.species_config["diet"] == "Herbivore":
            return prey.species_config["diet"] == "Plant"
        elif predator.species_config["diet"] == "Carnivore":
            return prey.species_config["diet"] == "Herbivore"
        return False

    def _collect_statistics(self):
        counts = {"plants": 0, "herbivores": 0, "carnivores": 0}
        for org in self.organisms:
            if org.species_config["diet"] == "Plant":
                counts["plants"] += 1
            elif org.species_config["diet"] == "Herbivore":
                counts["herbivores"] += 1
            else:
                counts["carnivores"] += 1

        for category, count in counts.items():
            self.statistics[category].append(count)
            # Keep history within a reasonable range
            if len(self.statistics[category]) > 100:
                self.statistics[category].pop(0)

    def toggle_pause(self):
        self.paused = not self.paused