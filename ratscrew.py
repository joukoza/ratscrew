import pygame, time, sys
from random import shuffle

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
    'spades(s)'. Possible values range from 2 to 14, where 14 stands for ace.
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
        for i in range(2,15):
            file_name = "./data_files/playing_cards_png/{0}_of_{1}.png"\
            .format(i, suit)
            img = pygame.image.load(file_name)
            img = pygame.transform.scale(img, dimensions)
            new_card = card(suit, i,img)
            playing_cards.append(new_card)
    amount = round(52/players)
    shuffle(playing_cards)
    for i in range(4):
        player_packs.append(player("Matti{0}".format(i), playing_cards[:amount]))
        del playing_cards[:amount]
    return player_packs

def victory_check(player_packs):
    P1_cards = len(player_packs[0].hand)
    P2_cards = len(player_packs[1].hand)
    P3_cards = len(player_packs[2].hand)
    P4_cards = len(player_packs[3].hand)
    if P1_cards != 0 and P2_cards == 0 and P3_cards == 0 and P4_cards == 0:
        fontObj = pygame.font.Font("./data_files/BlackOpsOne-Regular.ttf", 36)
        textObj = fontObj.render("P2 won the game", True, RED)
        win.blit(textObj, (100, 0))
        pygame.display.update()
        time.sleep(2)
        sys.exit()
    elif P1_cards == 0 and P2_cards != 0 and P3_cards == 0 and P4_cards == 0:
        fontObj = pygame.font.Font("./data_files/BlackOpsOne-Regular.ttf", 36)
        textObj = fontObj.render("P2 won the game", True, RED)
        win.blit(textObj, (100, 0))
        pygame.display.update()
        time.sleep(2)
        sys.exit(0)
    elif P1_cards == 0 and P2_cards == 0 and P3_cards != 0 and P4_cards == 0:
        fontObj = pygame.font.Font("./data_files/BlackOpsOne-Regular.ttf", 36)
        textObj = fontObj.render("P3 won the game", True, RED)
        win.blit(textObj, (100, 0))
        pygame.display.update()
        time.sleep(2)
        sys.exit(0)
    elif P1_cards == 0 and P2_cards == 0 and P3_cards == 0 and P4_cards != 0:
        fontObj = pygame.font.Font("./data_files/BlackOpsOne-Regular.ttf", 36)
        textObj = fontObj.render("P4 won the game", True, RED)
        win.blit(textObj, (100, 0))
        pygame.display.update()
        time.sleep(2)
        sys.exit(0)

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

def game_turn(p_packs, card_pile, card_location, to_angle):
    '''Handles the regular turns of each player.'''
    next_card = p_packs.hand[0]
    rotated_card = pygame.transform.rotate(next_card.img, to_angle)
    win.blit(rotated_card, card_location)
    card_pile.append(p_packs.hand[0])
    # Deletes the played card from the player's hand.
    p_packs.hand.pop(0)

def win_update():

    win.fill((0, 0, 0))
    pygame.display.update()

def slap_check(card_pile, player_packs, player, turn, players):
    '''Checks whether a slap was premature or victorious.'''
    # A safeguard in case someone slaps before two cards have been played.
    if len(card_pile) < 2:
        current_card = "cmon"
        previous_card = "lolnoob"
    else:
        current_card = card_pile[-1].value
        previous_card = card_pile[-2].value
    # Checks if the slapping player was victorious.
    if current_card == previous_card:
        # Adds the played cards to the slap winner's cards.
        player_packs[player-1].hand.extend(card_pile)
        # Empties the played cards.
        del card_pile[:]
        # Renders the slap victory text on win.
        fontObj = pygame.font.Font("./data_files/BlackOpsOne-Regular.ttf", 32)
        textObj = fontObj.render("P{0} won the slap".format(player),
                                 True, GREEN)
        win.blit(textObj, (125, 0))
        pygame.display.update()
        # Waits two seconds after a winning slap.
        time.sleep(2)
        # Removes the commands players input during the waiting period.
        # Prevents other people's slaps from being registered.
        pygame.event.clear()
        win.fill(BLACK)
        # The winner of the slap plays next.
        return player
    # If the player slapped prematurely, the other players get given a card,
    # unless they have no cards.
    else:
        for i in range(players):
            if len(player_packs) != 0:
                player_packs[i].hand.append(player_packs[player-1].hand[0])
                player_packs[player-1].hand.pop(0)
        fontObj = pygame.font.Font("./data_files/BlackOpsOne-Regular.ttf", 32)
        textObj = fontObj.render("P{0} lost the slap".format(player),
                                 True, GREEN)
        win.blit(textObj, (125, 0))
        pygame.display.update()
        time.sleep(2)
        pygame.event.clear()
        pygame.draw.rect(win, BLACK, (125, 5, 270, 35))
        # The next turn remains unchanged.
        return turn

def main():
    players = 4
    turn = 1
    x_location = 40
    y_location = 40
    angle = 0
    amount = 0
    location = (x_location, y_location)
    running = True
    player_packs = card_loader(players)
    card_pile = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Checks if the card_pile is empty, so the face card rule isn't
            # invoked before any cards have been played.
            if card_pile:
                # Checks if the last played card was a face card.
                # (An ace, king, queen or jack.)
                if card_pile[-1].value == 11 or card_pile[-1].value == 12\
                or card_pile[-1].value == 13 or card_pile[-1].value == 14:
                    amount = card_pile[-1].value-10
                    if turn < 4:
                        turn += 1
                    else:
                        turn = 1
            
            if turn == 1:
                if len(player_packs[0].hand) == 0:
                    turn = 2
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    game_turn(player_packs[0], card_pile, location, angle)
                    if amount == 0:
                        turn = 2
                    angle -= 5

            elif turn == 2:
                if len(player_packs[1].hand) == 0:
                    turn = 3
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    game_turn(player_packs[1], card_pile, location, angle)
                    if amount == 0:
                        turn = 3
                    angle -= 5

            elif turn == 3:
                if len(player_packs[2].hand) == 0:
                    turn = 4
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    game_turn(player_packs[2], card_pile, location, angle)
                    if amount == 0:
                        turn = 4
                    angle -= 5

            elif turn == 4:
                if len(player_packs[3].hand) == 0:
                    turn = 1
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    game_turn(player_packs[3], card_pile, location, angle)
                    if amount == 0:
                        turn = 1
                    angle -= 5
            
            # Player 1 slaps.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                turn = slap_check(card_pile, player_packs, 1, turn, players)

            # Player 2 slaps.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                turn = slap_check(card_pile, player_packs, 2, turn, players)

            # Player 3 slaps.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                turn = slap_check(card_pile, player_packs, 3, turn, players)
            #Player 4 slaps.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                turn = slap_check(card_pile, player_packs, 4, turn, players)

            # Inserts the remaining card amounts onto the win.
            remaining_cards(len(player_packs[0].hand), len(player_packs[1].hand),
            len(player_packs[2].hand), len(player_packs[3].hand), len(card_pile))

            victory_check(player_packs)

        pygame.display.update()
        victory_check(player_packs)

if __name__ == "__main__":
    main()