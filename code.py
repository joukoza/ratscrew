import pygame, random, time, sys
from pygame.locals import *

# Defines the necessary colours here, to improve code readability.
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


    '''Loads the image files of all individual playing cards
    and saves them in a dictionary, which is then returned.'''

    playing_cards = {}
    # The card dimensions. (X,Y)
    dimensions = (225, 426)

    for i in range(1,14):
        file_name = "./data_files/playing_cards_png/{0}_of_diamonds.png".format(i)
        dict_key = "d{0}".format(i)
        playing_cards[dict_key] = pygame.image.load(file_name)
        playing_cards[dict_key] = pygame.transform.scale(playing_cards[dict_key], dimensions)

    for i in range(1,14):
        file_name = "./data_files/playing_cards_png/{0}_of_clubs.png".format(i)
        dict_key = "c{0}".format(i)
        playing_cards[dict_key] = pygame.image.load(file_name)
        playing_cards[dict_key] = pygame.transform.scale(playing_cards[dict_key], dimensions)

    for i in range(1,14):
        file_name = "./data_files/playing_cards_png/{0}_of_hearts.png".format(i)
        dict_key = "h{0}".format(i)
        playing_cards[dict_key] = pygame.image.load(file_name)
        playing_cards[dict_key] = pygame.transform.scale(playing_cards[dict_key], dimensions)

    for i in range(1,14):
        file_name = "./data_files/playing_cards_png/{0}_of_spades.png".format(i)
        dict_key = "s{0}".format(i)
        playing_cards[dict_key] = pygame.image.load(file_name)
        playing_cards[dict_key] = pygame.transform.scale(playing_cards[dict_key], dimensions)
    
    return playing_cards

def placeholder():
    print("This is a test")

def main():

    pygame.init()

    # card_files contains the image files of all playing cards.
    # A specific playing card can be loaded with card_files["xn"], where x
    # is the first letter of the desired suit and n is the number.
    # Queen of hearts would for instance be 'card_files["h12"]'.
    # Ace is the first card.
    card_files = card_loader()
    
    # Creates a list of strings that will act as a deck of cards and then
    # shuffles it. The shuffled deck is then split among players.
    random.seed()
    card_deck = ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10",
                "h11", "h12", "h13", "d1", "d2", "d3", "d4", "d5", "d6", "d7",
                "d8", "d9", "d10", "d11", "d12", "d13", "c1", "c2", "c3", "c4",
                "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "c13",
                "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10",
                "s11", "s12", "s13"]
    random.shuffle(card_deck)
    P1_cards = card_deck[:26]
    P2_cards = card_deck[26:]
    # Keeps track of the played cards.
    card_pile = []

    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption("ratscrew_0.1")
    turn = 1

    pygame.mixer.music.load("data_files/music.mid")
    pygame.mixer.music.play(-1, 0.0)
    
    # The actual game loop.
    while True:
        for event in pygame.event.get():

            if turn == 1:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    game_turn(screen, card_files, P1_cards, card_pile)
                    turn = 2

            elif turn == 2:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    game_turn(screen, card_files, P2_cards, card_pile)
                    turn = 1

            # Player 1 slaps.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                turn = slap_check(screen, card_pile, P1_cards, P2_cards, 1, turn)

            # Player 2 slaps.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                turn = slap_check(screen, card_pile, P2_cards, P1_cards, 2, turn)

            # Inserts the remaining card amounts onto the screen.
            remaining_cards(screen, len(P1_cards), len(P2_cards), len(card_pile))
            pygame.display.update()

            victory_check(screen, len(P1_cards), len(P2_cards))
            
            if event.type == pygame.QUIT:
                sys.exit()

main()