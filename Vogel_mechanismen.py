import Algoritme_voor_leren
import pygame
import Scherm


class Player: # DIt is de class voor de vogels
    def __init__(self):
        # Vogel eigenschappen
        self.x, self.y = 50, 200 # Begin coordinaten van de vogel
        self.rect = pygame.Rect(self.x, self.y, 20, 20) # Dit is de hitbox van de vogel. Dit is nodig voor collision detection
        self.color = (255, 255, 0) 
        self.vel = 0 # snelheid van de vogel. Is 0 omdat hij nog niet beweegt
        self.flap = False # Dit is of de vogel aan het flappen is of niet. In dit geval is hij dat niet omdat het False is
        self.alive = True # Dit is of de vogel leeft of niet. In dit geval leeft hij omdat het True is
        self.lifespan = 0 # Dit is hoe lang de vogel al leeft. Begint bij 0 omdat hij net is gemaakt
        self.image = pygame.image.load("bird.png") # nu voeg je de foto toe van de originele vogel van Flappy Bird
        self.image = pygame.transform.scale(self.image, (20, 20)) # schaal de afbeelding naar de juiste grootte

        # AI eigenschappen
        self.decision = None
        self.vision = [1, 1, 1]
        self.inputs = 3
        self.fitness = 0
        self.brain = Algoritme_voor_leren.Brain(self.inputs)
        self.brain.generate_net()
        # Dit zijn alle AI eigenschappen van de vogel.
        # Die heb ik nodig om de vogel te laten leren hoe hij moet vliegen
    

   
    def draw(self, window):
        window.blit(self.image, self.rect) 
        # Hiermee teken ik de vogel op het scherm op de positie van zijn hitbox. 
        


    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)
    # Controleer of de vogel de grond raakt. 
    # Als de hitbox van de vogel en de grond elkaar overlappen, is er een botsing.
    

    def sky_collision(self):
        return bool(self.rect.y < 30)
    # Als de vogel hoger gaat dan 30 pixels vanaf de bovenkant van het scherm, is er een botsing met de lucht.

    def pipe_collision(self):
        for p in Scherm.pipes:
            return pygame.Rect.colliderect(self.rect, p.top_rect) or \
                   pygame.Rect.colliderect(self.rect, p.bottom_rect)
# Als de hitbox van de vogel en een van de pijpen elkaar overlappen, is er een botsing.
    def update(self, ground):
        if not (self.ground_collision(ground) or self.pipe_collision()):
            # Als de vogel niet botst met de grond of een pijp, update zijn positie
            self.vel += 0.4 # dit is de zwaartekracht op de vogel. Dat is een positieve waarde omdat hij naar beneden valt
            # De bird heeft geen snelheid dus is het eigenlijk plus de 0.4 gwn 0.4
            self.rect.y += self.vel # Hier update ik de y positie van de vogel met de werking van zwaartekracht
            if self.vel > 5:# Als de snelheid van de vogel groter is dan 5
                self.vel = 5 # dan gaat hij niet sneller vallen dan 5. Dat doe je om te voorkomen dat hij te snel valt
            # Het is dus een limiet.
            self.lifespan += 1 # Hier verhoog ik de levensduur van de vogel met 1 elke keer dat hij geupdate wordt
       
            

        else:
            self.alive = False # Als de vogel botst met de grond of een pijp, is hij dood
            self.flap = False # Hij kan niet meer flappen omdat hij dood is
            self.vel = 0 # Zijn snelheid is 0 omdat hij niet meer beweegt

    def bird_flap(self):
        if not self.flap and not self.sky_collision(): # Als de vogel niet al aan het flappen is en niet tegen de lucht botst
            self.flap = True # dan zet ik de flap status op True, zodat hij kan flappen
            self.vel = -5.5 # Dit is de waarde van elke flap. Het is negatief omdat de vogel omhoog gaat
            # Je ziet dus dat de self.vel groter is dan de zwaartekracht en dat is logisch want zo kan hij gematigd omhoog.
        if self.vel >= 3:   # als de snelheid van de vogel groter is dan of gelijk is aan 3
            self.flap = False # dan zet ik de flap status op False, zodat hij niet meer kan flappen

    @staticmethod
    def closest_pipe():
        for p in Scherm.pipes:
            if not p.passed:
                return p


   

    def look(self):
      if Scherm.pipes:
      # Hier wordt de afstand van de vogel tot de bovenkant van de opening van de pijp berekend en dat gedeeld door 500 omdat het voor een Neural Networks handig is om getallen tussen 0 en 1 te hebben

        self.vision[0] = max(0, self.rect.center[1] - self.closest_pipe().top_rect.bottom) / 500
        # Hier wordt de afstand van de vogel tot de bovenkant van de opening van de pijp berekend en dat gedeeld door 500 omdat het voor een Neural Networks handig is om getallen tussen 0 en 1 te hebben
  
        pygame.draw.line(Scherm.window, self.color, self.rect.center, (self.rect.center[0], Scherm.pipes[0].top_rect.bottom))
# Dit is de lijn die naar de bovenste pijp gaat die je tijdens de game ziet. Hij gaat dus recht omhoog van de vogel.


        # mid pipe
        self.vision[1] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
        pygame.draw.line(Scherm.window, self.color, self.rect.center, (Scherm.pipes[0].x, self.rect.center[1]))
# Hier wordt de afstand van de vogel tot de pijp zelf berekend. Dit is de horizontale afstand.
# Die komt ook als een lijn op het scherm tijdens de game

        # Line to bottom pipe
        self.vision[2] = max(0, self.closest_pipe().bottom_rect.top - self.rect.center[1]) / 500
        pygame.draw.line(Scherm.window, self.color, self.rect.center,(self.rect.center[0], Scherm.pipes[0].bottom_rect.top))
# Precies hetzelfde maar dan voor de onderkant van de pijp.
# Hier komt een lijn vanaf de vogel recht naar beneden tot de onderkant van de pijp.
    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision >= 0.74: 
            self.bird_flap()
# Hier gaat de AI nadenken op basis van wat hij ziet.
# Je had door 500 gedeeld om getallen tussen 0 en 1 te krijgen.
# hier zeg je dus, als dat getal groter is dan 0.73, flap dan. 
# Het getal heb ik zelf gekozen na wat experimenteren.

    def calculate_fitness(self):
        self.fitness = self.lifespan
# Hier bereken ik de fitness van de vogel op basis van hoe lang hij heeft geleefd.
# De vogel kreeg voor elke frame dat hij leefde 1 punt. 
# Dus de self.lifespan is eigenlijk het aantal frames dat de vogel heeft overleefd en dat is gelijk aan self.fitness.
    def clone(self):
        clone = Player() # Je maakt hiermee een nieuwe vogel aan
        clone.fitness = self.fitness # Je kopieert de fitness van de huidige vogel naar de nieuwe vogel
        clone.brain = self.brain.clone() # Je kopieert het brein van de huidige vogel naar de nieuwe vogel
        clone.brain.generate_net() # Het brein van de nieuwe vogel wordt gegenereerd. Dit is geen kopie maar een nieuw brein met dezelfde structuur en gewichten
        return clone # je stuurt de nieuwe vogel terug om te gebruiken
    


