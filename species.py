import operator
import random

class Species: # een groep spelers met vergelijkbare eigenschappen
    def __init__(self, player):
        self.players = [] # Net zoals bij de pipes, maak ik een lege lijst aan om de spelers in op te slaan die tot deze soort behoren
        self.average_fitness = 0 # gemiddelde fitness van de soort
        self.treshold = 1.2 #welke gaan gekozen worden en welke niet
        self.players.append(player) # voef de vogel die de player is toe aan de soort
        self.benchmark_fitness = player.fitness # fitness van de beste speler in de soort
        self.benchmark_brain = player.brain.clone() # kopieer het brein van de beste speler in de soort
        self.champion = player.clone() # kopieer de beste speler in de soort
        self.staleness = 0 # dit is hoe lang de soort al geen verbetering heeft laten zien. Het is 0 omdat het nog maar net is gemaakt.

    def similarity(self, brain): # 
        similarity = self.weight_difference(self.benchmark_brain, brain)
        return self.treshold - similarity

    @staticmethod
    def weight_difference(brain1, brain2):
        total_weight_difference = 0
        for i in range(0, len(brain1.connections)):
            for j in range(0, len(brain2.connections)):
                if i ==j:
                    total_weight_difference += abs(brain1.connections[i].weight - brain2.connections[j].weight)
        return total_weight_difference

    def add_to_species(self, player):
        self.players.append(player)

    def sort_players_by_fitness(self):
        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)
        if self.players[0].fitness > self.benchmark_fitness:
            self.staleness = 0
            self.benchmark_fitness = self.players[0].fitness
            self.champion = self.players[0].clone()
        else:
            self.staleness += 1
    def calculate_average_fitness(self):
        total_fitness = 0
        for p in self.players:
            total_fitness += p.fitness
        if self.players:
            self.average_fitness = int(total_fitness / len(self.players))
        else:
            self.average_fitness = 0

    def offspring(self):
        bebe = self.players[random.randint(1, len(self.players) - 1)].clone()
        bebe.brain.mutate()
        return bebe

