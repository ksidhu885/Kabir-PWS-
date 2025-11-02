import pygame
# Pygame is een module die kan helpen bij het maken van game in Python.
# Het zorgt namelijk voor het weergeven van graphics, het afspelen van geluiden en het verwerken van gebruikersinvoer.
# Je hoeft dan niet alles zelf te programmeren, wat het maken van games een stuk makkelijker maakt.
# Hiermeer importeer ik pygame om de functies van pygame te kunnen gebruiken
pygame.font.init()
import Grond_en_pijpensets
# Hiermee importeer ik het bestand Grond_en_pijpensets.py om de functies van dat bestand te kunnen gebruiken

win_height = 720 #hoogte van het venster waarin de game wordt weergegeven
win_width = 550 #breedte van het venster waarin de game wordt weergegeven
window = pygame.display.set_mode((win_width, win_height)) 
# Hiermee maak ik een venster aan met de opgegeven breedte en hoogte waarin de game wordt weergegeven

background = pygame.image.load('bg.png')
# Zoals ik al zei, zou ik de originele achtergrond gebruiken van Flappy Bird
# Deze regel code laadt de afbeelding 'bg.png' in als achtergrondafbeelding voor het spel
background = pygame.transform.scale(background, (win_width, win_height))
# Deze regel code schaalt de achtergrondafbeelding zodat deze precies past in het venster van het spel met de opgegeven breedte en hoogte
display_score_font = pygame.font.SysFont('comicsans', 50)
ground = Grond_en_pijpensets.Ground(win_width)
# Hiermee maak ik een grond object aan uit het bestand Grond_en_pijpensets.py

pipes = []
# Hiermee maak ik een lege lijst aan waarin ik de pijpen ga opslaan die in het spel verschijnen
# dit doe ik omdat ik meerdere pijpen nodig heb tijdens het spelen van het spel
# Zo kan ik ze allemaal bijhouden en updaten tijdens het spel.
