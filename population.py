import Scherm
import Vogel_mechanismen
import math
import species
import operator




class Population:
    def __init__(self, size):
        self.players = []
        self.generation = 1
        self.species = []
        self.size = size
        for i in range(0, self.size):
            self.players.append(Vogel_mechanismen.Player())

    def update_live_players(self):
        for p in self.players:
            if p.alive:
                p.look()
                p.think()
                p.draw(Scherm.window)
                p.update(Scherm.ground)
            

    def natural_selection(self):
        print("natuurlijke selectie")
        self.speciate()

        print("Kill extinct")
        self.kill_extinct_species()

        print("Kill staleness")
        self.kill_stale_species()

        print("Calculate fitness")
        self.calculate_fitness()


        print("Sort by fitness")
        self.sort_species_by_fitness()

        print("Children for next gen")
        self.next_gen()

    def speciate(self):
        for s in self.species:
            s.players = []

        for p in self.players:
            add_to_species = False
            for s in self.species:
                if s.similarity(p.brain):
                    s.add_to_species(p)
                    add_to_species = True
                    break
            if not add_to_species:
                self.species.append(species.Species(p))

    def kill_extinct_species(self):
        species_to_kill = []
        for s in self.species:
            if len(s.players) == 0:
                species_to_kill.append(s)
        for s in species_to_kill:
            self.species.remove(s)

    def kill_stale_species(self):
        players_to_kill = []
        species_to_kill = []
        for s in self.species:
            if s.staleness >= 8:
                if len(self.species) > len(species_to_kill) + 1:
                    species_to_kill.append(s)
                    for p in s.players:
                        players_to_kill.append(p)
                    else:
                        s.staleness = 0
        for p in players_to_kill:
            self.players.remove(p)
        for s in species_to_kill:
            self.species.remove(s)

    def calculate_fitness(self):
        for p in self.players:
            p.calculate_fitness()
        for s in self.species:
            s.calculate_average_fitness()
            print("Species average fitness:", s.average_fitness)

    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_players_by_fitness()

        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True) 
        # dit zorgt ervoor dat de species met de hoogste benchmark fitness eerst komt
        # Dit gebeurt omdat de species met de hoogste benchmark fitness waarschijnlijk de beste kans heeft om succesvolle nakomelingen te produceren.
        # De module operator wordt gebruikt om de sortering op een efficiënte en leesbare manier uit te voeren.
        # De mo

    def next_gen(self):
        children = []
        
        for s in self.species:
            children.append(s.champion.clone())
        
        children_per_species = math.floor((self.size / len(self.species)) / len(self.species[0].players))
        for s in self.species:
            for i in range(0, children_per_species):
               children.append(s.offspring())
        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.players = []
        for child in children:
            self.players.append(child)
        self.generation += 1



    def extinct(self):
        extinct = True
        for p in self.players:
            if p.alive:
                extinct = False
        return extinct

