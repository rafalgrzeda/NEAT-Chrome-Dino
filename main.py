import pygame
import os
import neat
from dino import Dino
from background import Background
from cactus import Cactus

pygame.font.init()
STAT_FONT = pygame.font.SysFont("comicsans", 40)
WIN_WIDTH = 600     # szerokosc okna
WIN_HEIGHT = 600    # wysokosc okna
BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("img", "dino_bg.png")), (600, 600))        #wczytanie tła


def draw_window(window, dinos, bg, cactuses, score):
    bg.draw(window)
    for dino in dinos:
        dino.draw(window)
    for cactus in cactuses:
        cactus.draw(window)
    text = STAT_FONT.render("Score: " + str(score), 1, (0, 0, 0))
    window.blit(text, (10, 10))
    pygame.display.update()


def main(genomes, config):
    nn = []         #lista sieci neurnowych
    ge = []     #lista genomów
    dinos = []      #lista dino

    os.environ['SDL_VIDEO_WINDOW_POS'] = '400,50'                   # ustiawienie pozycji okna
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))       # stworzenie okna

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)      #stowrzenie sieci neuronowej
        nn.append(net)                                          #dodanie jej do listy sieci
        dinos.append(Dino(50, 450))                             #stworzenie dino i dodanie go do listy
        g.fitness = 0                                           #ustawienie funkcji fitness
        ge.append(g)                                            #dodanie genomu do listy

    run = True
    bg = Background(0)
    cactuses = [Cactus()]
    score = 0
    add_cactus = False

    while run:
        cactus_ind = 0
        if len(dinos) > 0:
            if len(cactuses) > 1 and dinos[0].x > cactuses[0].x + cactuses[0].IMG.get_width():
                cactus_ind = 1
        else:
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        for x, dino in enumerate(dinos):
            dino.move()
            output = nn[x].activate((dino.y, dino.x - cactuses[cactus_ind].x))
            if output[0] > 0.5 and not dino.is_jumping:
                dino.jump()
                ge[x].fitness -= 1.5

        remove_cactus = []
        for cactus in cactuses:
            for x, dino in enumerate(dinos):
                if not cactus.passed and cactus.x < dino.x:  # pokonanie przez Dino
                    score += 1
                    cactus.passed = True
                    add_cactus = True
                if cactus.collide(dino):
                    dinos.pop(x)
                    nn.pop(x)
                    ge.pop(x)
            if cactus.x + cactus.IMG.get_width() < 0:  # wyjsce poza ekran
                remove_cactus.append(cactus)

        for cactus in cactuses:
            cactus.move()

        if add_cactus:
            cactuses.append(Cactus())
            for g in ge:
                g.fitness += 3
            add_cactus = False

        for r in remove_cactus:
            cactuses.remove(r)
        bg.move()
        draw_window(window, dinos, bg, cactuses, score)


def run_neat(m_config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, m_config_path)

    population = neat.Population(config)                    # Pobranie populacji

    # Wyswietlanie statystyk
    population.add_reporter(neat.StdOutReporter(True))
    stat = neat.StatisticsReporter()
    population.add_reporter(stat)

    winner = population.run(main, 50)       #fitness function i liczba generacji


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat_config.txt")
    run_neat(config_path)