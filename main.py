import pygame 
from sys import exit
import Scherm
import Grond_en_pijpensets # dit is de file 
import population
score = 0
generation = 1
passpipe = False
pygame.init()
clock = pygame.time.Clock()
population = population.Population(200)
fast_forward = False

font = pygame.font.SysFont('comicsans', 30)
display_score_font = pygame.font.SysFont('comicsans', 50)

def generate_pipes():
    Scherm.pipes.append(Grond_en_pijpensets.Pipes(Scherm.win_width))
def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

def draw_score():
    score_display = Scherm.display_score_font.render(f'Score: {score}', True, (255, 255, 255))
    Scherm.window.blit(score_display, (10, 10))
    gen_display = Scherm.display_score_font.render(f'Generation: {generation}', True, (255, 255, 255))
    Scherm.window.blit(gen_display, (10, 50))


def main():
    pipes_spawn_time = 10
    global score, passpipe, fast_forward, generation

    while True:
        quit_game()

        Scherm.window.blit(Scherm.background, (0, 0))

        #spawn ground
        Scherm.ground.draw(Scherm.window)

        

        #spawn pipes
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1

        if len(Scherm.pipes) > 0:
                if Scherm.pipes[0].x + Scherm.pipes[0].top_rect.width < population.players[0].x and not passpipe:
                    score += 1
                    passpipe = True
                if Scherm.pipes[0].x + Scherm.pipes[0].top_rect.width >= population.players[0].x:
                    passpipe = False


        for p in Scherm.pipes:
            p.draw(Scherm.window)
            p.update()
            if p.off_screen:
                Scherm.pipes.remove(p)
        if not population.extinct():
            population.update_live_players()
        else:
            Scherm.pipes.clear()
            population.natural_selection()

    

            final_score = score
            print(f"Generation {generation} finished with score: {score}")            
            
            score = 0
            generation += 1
            print(f"starting Generation {generation}")

           

        if fast_forward:
            clock.tick(300)
        else:
         clock.tick(60)
        draw_score()
        pygame.display.flip()

main()  