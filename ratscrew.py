import pygame
from random import shuffle
from time import sleep

pygame.init()
win_width, win_height = 1000, 700
win = pygame.display.set_mode((win_width, win_height))

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class card():
    '''Depicts a playing card that has a suit and a value. Possible 
    suits and their symbols are 'clubs(c)', 'diamonds(d)', 'hearts(h)' and 
    'spades(s)'. Possible values range from 1 to 13, where 1 stands for ace.
    '''
    def __init__(self, suit, value, img):
        self.suit = suit
        self.value = value
        self.img = img

class player():
    '''Depicts a player who takes part in the game and has specific 
    set of cards(hand).'''
    def __init__(self, name, cards):
        self.name = name
        self.hand = cards

class deck():
    def __init__(self, cards):
        self.cards = cards

    def shuffle(self):
        shuffle(self.cards)

def card_loader(players):
    '''Creates instances of all individual playing cards, assigning 
    corresponding suit, value and  image to each card.'''
    playing_cards = []
    ## The card dimensions. (X,Y)
    dimensions = (225, 426)
    suits = ["clubs", "diamonds", "hearts", "spades"]
    player_packs = []
    for suit in suits:
        for i in range(1,14):
            file_name = "./data_files/playing_cards_png/{0}of{1}.png"\
            .format(i, suit)
            img = pygame.image.load(file_name)
            img = pygame.transform.scale(img, dimensions)
            new_card = card(suit, i,img)
            playing_cards.append(new_card)
    number = round(52/players)
    for i in range(0, players):
        player_packs.append(player("Matti{0}".format(i), playing_cards[:number]))

    return player_packs

def setup(divider):
    playing_cards = card_loader()
    number = round(52/divider)
    player1 = playing_cards[:number]
    return player1

def remaining_cards(P1_rem, P2_rem, P3_rem, P4_rem, pile_rem):
    '''Draws the amount of remaining cards for each player on the win.'''
    # Draws over the previous text so that the win doesn't get cluttered.
    pygame.draw.rect(win, BLACK, (0,0, 105, 30))
    pygame.draw.rect(win, BLACK, (390, 470, 105, 30))
    pygame.draw.rect(win, BLACK, (390, 0, 115, 30))
    pygame.draw.rect(win, BLACK, (0, 470, 115, 30))
    pygame.draw.rect(win, BLACK, (200, 470, 115, 30))
    fontObj = pygame.font.Font("./data_files/Rationale-Regular.otf", 25)
    textObj = fontObj.render("P1 cards: {0}".format(P1_rem),
                             True, WHITE)
    textObj2 = fontObj.render("P2 cards: {0}".format(P2_rem),
                              True, WHITE)
    textObj3 = fontObj.render("P3 cards: {0}".format(P3_rem),
                              True, WHITE)
    textObj4 = fontObj.render("P4 cards: {0}".format(P4_rem),
                              True, WHITE)
    textObj5 = fontObj.render("Card pile: {0}".format(pile_rem),
                              True, WHITE)
    win.blit(textObj, (0, 0))
    win.blit(textObj2, (390, 0))
    win.blit(textObj3, (390, 470))
    win.blit(textObj4, (0, 470))
    win.blit(textObj5, (200, 470))

def game_turn(p_packs, card_pile, card_location):
    '''Handles the regular turns of each player.'''
    next_card = p_packs[0]
    win.blit(next_card.img, card_location)
    card_pile.append(p_packs[0])
    # Deletes the played card from the player's hand.
    p_packs.pop(0)

def win_update():

    win.fill((0, 0, 0))
    pygame.display.update()


def main():
    players = 4
    ind = 0
    turn = 1
    x_location = 140
    y_location = 40
    location = (x_location, y_location)
    running = True
    player_packs = card_loader(players)
    card_pile = []
    while running:
        pygame.time.delay(200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if turn == 1:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    game_turn(player_packs[0], card_pile, location)
                    turn = 2

            elif turn == 2:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    game_turn(player_packs[1], card_pile, location)
                    if players == 2:
                        turn = 1
                    else:
                        turn = 3

            elif turn == 3:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    game_turn(player_packs[2], card_pile, location)
                    if players == 3:
                        turn = 1
                    else:
                        turn = 4

            elif turn == 4:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    game_turn(player_packs[3], card_pile, location)
                    turn = 1

            # Player 1 slaps.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                turn = slap_check(win, card_pile, P1_cards, P2_cards, 1, turn)

            # Player 2 slaps.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                turn = slap_check(win, card_pile, P2_cards, P1_cards, 2, turn)

            # Player 3 slaps.
            if players == 3:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    pass
            #Player 4 slaps.
            if players == 4:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                    pass
            
            # Inserts the remaining card amounts onto the win.
            remaining_cards(len(player_packs[0]), len(player_packs[1]), len(player_packs[2]), len(player_packs[3]), len(card_pile))


            #victory_check(len(P1_cards), len(P2_cards))

        x_location += 10
        y_location += 2
        location = (x_location, y_location)
        if (ind/5 - round(ind/5) == 0):
            x_location = 140
            #y_location = 40
            location = (x_location, y_location)
        pygame.display.update()
        ind += 1
        

    pygame.quit()

main()
