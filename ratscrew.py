import pygame, time
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
    card_amount = round(52/players)
    shuffle(playing_cards)
    for i in range(4):
        player_packs.append(player("Matti{0}".format(i), playing_cards[:card_amount]))
        del playing_cards[:card_amount]
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
    '''Draws the face_mode["amount"] of remaining cards for each player on the win.'''
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

def pile_empty(player_packs, card_pile, player, text):
    '''Adds the played cards to the winner's hand
     and prints the winning text on the screen.'''
    # Adds the played cards to the slap winner's cards.
    player_packs[player-1].hand.extend(card_pile)
    # Empties the played cards.
    del card_pile[:]
    # Renders the supplied victory text on win.
    fontObj = pygame.font.Font("./data_files/BlackOpsOne-Regular.ttf", 32)
    textObj = fontObj.render(text, True, GREEN)
    win.blit(textObj, (125, 0))
    pygame.display.update()
    # Waits two seconds after a winning slap.
    time.sleep(2)
    # Removes the commands players input during the waiting period.
    # Prevents other people's slaps from being registered.
    pygame.event.clear()
    win.fill(BLACK)

def game_turn(p_packs, card_pile, card_location, angle):
    '''Handles the regular turns of each player.'''
    next_card = p_packs.hand[0]
    rotated_card = pygame.transform.rotate(next_card.img, angle)
    win.blit(rotated_card, card_location)
    card_pile.append(p_packs.hand[0])
    # Deletes the played card from the player's hand.
    p_packs.hand.pop(0)

def face_win(player_packs, card_pile, face_mode):
    '''Handles the face card mode wins.'''
    pile_empty(player_packs, card_pile, face_mode["player"],
    "P{0} won the cards.".format(face_mode["player"]))
    winner = face_mode["player"]
    # Changes these to zero, so that the game is no longer in face card mode.
    face_mode["player"] = 0
    face_mode["amount"] = 0
    # Returns the winning player's number, so it can be assigned to turn.
    return winner

def turn_check(player_packs, turn, face_mode, card_pile, event, location, key):
    '''Checks all the various things that need to be checked each turn.'''
    # Skips the players turn if they don't have any cards
    # and face card mode isn't on.
    if len(player_packs[turn-1].hand) == 0 and face_mode["player"] == 0:
        if turn != 4:
            turn += 1
        else:
            turn = 1
    # Defined in case the player runs out of cards while
    # in face card mode.
    elif len(player_packs[turn-1].hand) == 0 and face_mode["player"] != 0:
        turn = face_win(player_packs, card_pile, face_mode)

    # The player who played the face card won.
    elif face_mode["amount"] == 0 and face_mode["player"] != 0:
        turn = face_win(player_packs, card_pile, face_mode)

    elif event.type == pygame.KEYDOWN and event.key == key:
        game_turn(player_packs[turn-1], card_pile, (location["x"],
        location["y"]), location["angle"])
        if face_mode["player"] == 0 and turn != 4:
            turn += 1
        elif face_mode["player"] == 0 and turn == 4:
            turn = 1
        # The face card mode is on, and thus the turn isn't changed.
        else:
            face_mode["amount"] -= 1
        location["angle"] -= 5
    return turn

def slap_check(card_pile, player_packs, player, turn, players, face_mode):
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
        pile_empty(player_packs, card_pile, player,
        "P{0} won the slap".format(player))
        # Clears the face card mode, if it is active.
        face_mode["player"] = 0
        face_mode["amount"] = 0
        # The winner of the slap plays next.
        return player
    # If the player slapped prematurely, the other players get given a card;
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
    # These are defined in a dictionary, so the angle's value
    # can be changed in a function without a return value.
    # Also possibly the x and y coordinates later if needed.
    location = {
        "x" : 40,
        "y" : 40,
        "angle" : 0
    }
    # Used for keeping track of the face card mode.
    # Player designates the player who played the face card.
    # Amount designates the amount of cards the next player must play.
    # Also defined in a dictionary, so the values can be changed in functions.
    face_mode = {
        "player" : 0,
        "amount" : 0
    }
    # Used to prevent the face card mode from being initiated by
    # the same card.
    previous_card = 0
    running = True
    player_packs = card_loader(players)
    card_pile = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Checks if the card_pile is empty, so the program doesn't crash if
            # card_pile is empty.
            if card_pile:
                # Checks if the played card is different from the previous card.
                # Otherwise the following code would be executed by the
                # first face card and initiated by all events.
                if previous_card != card_pile[-1]:
                    # Checks if the last played card was a face card.
                    # (An ace, king, queen or jack.)
                    if card_pile[-1].value == 11 or card_pile[-1].value == 12\
                    or card_pile[-1].value == 13 or card_pile[-1].value == 14:
                        previous_card = card_pile[-1]
                        face_mode["amount"] = card_pile[-1].value-10
                        # If face mode wasn't previously active.
                        if face_mode["player"] == 0 and turn != 1:
                            # Subtracting one because turn has already been
                            # changed in the turn_check function.
                            face_mode["player"] = turn-1
                        elif face_mode["player"] == 0 and turn == 1:
                            face_mode["player"] = 4
                        # If face mode was previously active.
                        elif face_mode["player"] > 0:
                            if turn != 4:
                                face_mode["player"] = turn
                                turn += 1
                            else:
                                face_mode["player"] = 4
                                turn = 1

            # Turn events for each player.
            if turn == 1:
                turn = turn_check(player_packs, turn, face_mode, card_pile, event,
                location, pygame.K_w)

            elif turn == 2:
                turn = turn_check(player_packs, turn, face_mode, card_pile, event,
                location, pygame.K_u)

            elif turn == 3:
                turn = turn_check(player_packs, turn, face_mode, card_pile, event,
                location, pygame.K_s)

            elif turn == 4:
                turn = turn_check(player_packs, turn, face_mode, card_pile, event,
                location, pygame.K_j)
            
            # The slap events for each player.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                turn = slap_check(card_pile, player_packs, 1, turn, players,
                face_mode)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                turn = slap_check(card_pile, player_packs, 2, turn, players,
                face_mode)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                turn = slap_check(card_pile, player_packs, 3, turn, players,
                face_mode)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                turn = slap_check(card_pile, player_packs, 4, turn, players,
                face_mode)

            # Inserts the remaining card amounts onto the window.
            remaining_cards(len(player_packs[0].hand), len(player_packs[1].hand),
            len(player_packs[2].hand), len(player_packs[3].hand), len(card_pile))

            victory_check(player_packs)

        pygame.display.update()
        victory_check(player_packs)

if __name__ == "__main__":
    main()
