import pygame, random, time, sys
from pygame.locals import *

# Defines the necessary colours here, to improve code readability.
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def victory_check(screen, P1_rem, P2_rem):
    if P1_rem == 0:
        fontObj = pygame.font.Font("./data_files/BlackOpsOne-Regular.ttf", 36)
        textObj = fontObj.render("P2 won the game", True, RED)
        screen.blit(textObj, (100, 0))
        pygame.display.update()
        time.sleep(2)
        sys.exit()
    elif P2_rem == 0:
        fontObj = pygame.font.Font("./data_files/BlackOpsOne-Regular.ttf", 36)
        textObj = fontObj.render("P1 won the game", True, RED)
        screen.blit(textObj, (100, 0))
        pygame.display.update()
        time.sleep(2)
        sys.exit(0)

def game_turn(screen, card_files, P_cards, card_pile):
    '''Handles the regular turns of each player.'''
    card_location = (140, 40)
    # Stores the image file of the next card.
    next_card = card_files[P_cards[0]]
    screen.blit(next_card, card_location)
    card_pile.append(P_cards[0])
    P_cards.pop(0)

def remaining_cards(screen, P1_rem, P2_rem, pile_rem):
    '''Draws the amount of remaining cards for each player on the screen.'''
    # Draws over the previous text so that the screen doesn't get cluttered.
    pygame.draw.rect(screen, BLACK, (0,0, 105, 30))
    pygame.draw.rect(screen, BLACK, (390, 470, 105, 30))
    pygame.draw.rect(screen, BLACK, (200, 470, 115, 30))
    fontObj = pygame.font.Font("./data_files/Rationale-Regular.otf", 25)
    textObj = fontObj.render("P1 cards: {0}".format(P1_rem),
                             True, WHITE)
    textObj2 = fontObj.render("P2 cards: {0}".format(P2_rem),
                              True, WHITE)
    textObj3 = fontObj.render("Card pile: {0}".format(pile_rem),
                              True, WHITE)
    screen.blit(textObj, (0, 0))
    screen.blit(textObj2, (390, 470))
    screen.blit(textObj3, (200, 470))

def slap_check(screen, card_pile, player_cards, other_cards, player, turn):
    '''Checks whether a slap was premature or victorious.'''
    # A safeguard in case someone slaps before two cards have been played.
    if len(card_pile) < 2:
        current_card = "cmon"
        previous_card = "lolnoob"
    else:
        current_card = card_pile[-1]
        previous_card = card_pile[-2]
    # Checks if the slapping player was victorious.
    if current_card[1:] == previous_card[1:]:
        # Adds the played cards to the slap winner's cards.
        player_cards.extend(card_pile)
        # Empties the played cards.
        del card_pile[:]
        # Renders the slap victory text on screen.
        fontObj = pygame.font.Font("./data_files/BlackOpsOne-Regular.ttf", 32)
        textObj = fontObj.render("P{0} won the slap".format(player),
                                 True, GREEN)
        screen.blit(textObj, (125, 0))
        pygame.display.update()
        # Waits two seconds after a winning slap.
        time.sleep(2)
        # Removes the commands players input during the waiting period.
        # Prevents other people's slaps from being registered.
        pygame.event.clear()
        screen.fill(BLACK)
        # The winnder of the slap plays next.
        return player
    # If the player slapped prematurely, the other player gets given a card.
    else:
        other_cards.append(player_cards[0])
        player_cards.pop(0)
        fontObj = pygame.font.Font("./data_files/BlackOpsOne-Regular.ttf", 32)
        textObj = fontObj.render("P{0} lost the slap".format(player),
                                 True, GREEN)
        screen.blit(textObj, (125, 0))
        pygame.display.update()
        time.sleep(2)
        pygame.event.clear()
        pygame.draw.rect(screen, BLACK, (125, 5, 270, 35))
        # The next turn remains unchanged.
        return turn

def card_loader():
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

def placeholder

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