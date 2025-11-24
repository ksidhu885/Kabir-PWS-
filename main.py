import pygame
from sys import exit
import Scherm
import Grond_en_pijpensets
import population
import pickle
import csv
import os
#import random
#random.seed(10)

score = 0
generation = 1
target_score = 150
brain_saved = False
passpipe = False
pygame.init()
clock = pygame.time.Clock()
population = population.Population(200)
fast_forward = False

font = pygame.font.SysFont('comicsans', 30)
display_score_font = pygame.font.SysFont('comicsans', 50)


def save_weights_csv(bird, generation, score):
    weights = [round(c.weight, 4) for c in bird.brain.connections]
    filename = "weights_log.csv"
    header = ["generation", "score"] + [f"w{i}" for i in range(len(weights))]

    write_header = not os.path.exists(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow([generation, score] + weights)



def save_full_network_csv(bird, generation, score):
    filename = "network_log.csv"
    write_header = not os.path.exists(filename)




    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow([
                "generation",
                "score",
                "from_node_id",
                "from_layer",
                "to_node_id",
                "to_layer",
                "weight"
            ])

        for c in bird.brain.connections:
            writer.writerow([
                generation,
                score,
                c.from_node.id,
                c.from_node.layer,
                c.to_node.id,
                c.to_node.layer,
                c.weight
            ])




if os.path.exists("weights_log.csv"):
    os.remove("weights_log.csv")

if os.path.exists("network_log.csv"):
    os.remove("network_log.csv")



def generate_pipes():
    Scherm.pipes.append(Grond_en_pijpensets.Pipes(Scherm.win_width))

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

def draw_score():
    score_display = display_score_font.render(f'Score: {score}', True, (255, 255, 255))
    Scherm.window.blit(score_display, (10, 10))
    gen_display = display_score_font.render(f'Generation: {generation}', True, (255, 255, 255))
    Scherm.window.blit(gen_display, (10, 50))


def main():
    global score, passpipe, fast_forward, generation, brain_saved
    pipes_spawn_time = 10

    while True:
        quit_game()
        Scherm.window.blit(Scherm.background, (0, 0))
        Scherm.ground.draw(Scherm.window)

        # Spawn pipes
        if pipes_spawn_time <= 0:
            generate_pipes()
            pipes_spawn_time = 200
        pipes_spawn_time -= 1

        # Update score
        if len(Scherm.pipes) > 0:
            if Scherm.pipes[0].x + Scherm.pipes[0].top_rect.width < population.players[0].x and not passpipe:
                score += 1
                passpipe = True
            if Scherm.pipes[0].x + Scherm.pipes[0].top_rect.width >= population.players[0].x:
                passpipe = False

        # Check if target score reached
        if score >= target_score:
            print(f"Target score {target_score} reached! Ending run.")
            best_bird = max(population.players, key=lambda p: p.fitness)
            save_weights_csv(best_bird, generation, score)
            

            

            pygame.quit()

            

            filename = f"final_brain_gen{generation}_score{score}.pkl"
            with open(filename, "wb") as f:
                pickle.dump(best_bird.brain, f)
            print(f"Saved final brain: {filename}")
            pygame.quit()
            return  # exit the main loop

        # Update and draw pipes
        for p in Scherm.pipes:
            p.draw(Scherm.window)
            p.update()
            if p.off_screen:
                Scherm.pipes.remove(p)
        

        if len(population.players) > 0:
          bird = population.players[0]
        else:
          bird = None

          


        # Update population
        if not population.extinct():
            population.update_live_players()
          

        else:
            # Start next generation
            best_bird = max(population.players, key=lambda p: p.fitness)
            save_weights_csv(best_bird, generation, score)
            save_full_network_csv(best_bird, generation, score)
            


            Scherm.pipes.clear()
            population.natural_selection()
            score = 0
            generation += 1
            brain_saved = False
            print(f"Starting Generation {generation}")

        clock.tick(300 if fast_forward else 60)
        draw_score()
        pygame.display.flip()

main()
