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
    '''Depicts a player who takes part in the game and has a specific
    set of cards(hand).'''
    def __init__(self, name, cards):
        self.name = name
        self.hand = cards

def card_loader(players, card_pile, location):
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
    # Removes one card from the deck and puts it on the table.
    if players == 3:
        # Searches for the earliest card that isn't a face card.
        # Necessary so that the first card on the table isn't a face card.
        for i in  range(0, 52):
            if playing_cards[i].value < 11:
                extra_card = i
                break
        card_pile.append(playing_cards[extra_card])
        draw_card(playing_cards[extra_card], location)
        playing_cards.pop(extra_card)
    for i in range(4):
        player_packs.append(player("Matto{0}".format(i+1), playing_cards[:card_amount]))
        del playing_cards[:card_amount]
    return player_packs

def draw_text(text, color, rect_draw):
    '''Draws event text on the screen and waits 2 seconds after that.'''
    text_size = 28
    font_obj = pygame.font.Font("./data_files/BlackOpsOne-Regular.ttf", text_size)
    text_obj = font_obj.render(text, True, color)
    # Location of the event text.
    location = (115, 0)
    win.blit(text_obj, location)
    pygame.display.update()
    # The text is displayed for two seconds so that players have time to react.
    time.sleep(2)
    # Removes the commands players input during the waiting period.
    pygame.event.clear()
    # Draws a rectangle over the previous text. Necessary for the time being
    # because cards need to remain on screen on losing slaps.
    if rect_draw == True:
        rect_size = (115, 5, 270, 35)
        pygame.draw.rect(win, BLACK, rect_size)
    else:
        win.fill(BLACK)

def victory_check(player_packs):
    '''Checks if any of the players have won (by checking if
    the other players' hands are empty).'''
    P1_cards = len(player_packs[0].hand)
    P2_cards = len(player_packs[1].hand)
    P3_cards = len(player_packs[2].hand)
    P4_cards = len(player_packs[3].hand)
    if P1_cards != 0 and P2_cards == 0 and P3_cards == 0 and P4_cards == 0:
        draw_text("P1 won the game", WHITE, False)
        sys.exit()
    elif P1_cards == 0 and P2_cards != 0 and P3_cards == 0 and P4_cards == 0:
        draw_text("P2 won the game", WHITE, False)
        sys.exit(0)
    elif P1_cards == 0 and P2_cards == 0 and P3_cards != 0 and P4_cards == 0:
        draw_text("P3 won the game", WHITE, False)
        sys.exit(0)
    elif P1_cards == 0 and P2_cards == 0 and P3_cards == 0 and P4_cards != 0:
        draw_text("P4 won the game", WHITE, False)
        sys.exit(0)
        
def remaining_cards(P1_rem, P2_rem, P3_rem, P4_rem, pile_rem):
    '''Draws the amount of remaining cards for each player on the screen.'''
    # Draws over the previous text so that the screen doesn't get cluttered.
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

def draw_card(card, location):
    '''Draws a card on the screen and changes location's angle value.'''
    angle = location["angle"]
    card_location = (location["x"], location["y"])
    rotated_card = pygame.transform.rotate(card.img, angle)
    win.blit(rotated_card, card_location)
    location["angle"] -= 5

def game_turn(player_hand, card_pile, location):
    '''Handles the regular turns of each player.'''
    next_card = player_hand[0]
    draw_card(next_card, location)
    card_pile.append(player_hand[0])
    # Deletes the played card from the player's hand.
    player_hand.pop(0)
    location["angle"] -= 5
    
def face_win(player_packs, card_pile, face_mode):
    '''Handles the face card mode wins.'''
    winner = face_mode["face_player"]
    text = "P{0} won the cards".format(winner+1)
    draw_text(text, GREEN, False)
    # Adds the played cards to the winner's cards.
    player_packs[winner].hand.extend(card_pile)
    # Empties the played cards.
    del card_pile[:]
    # Changes these to zero, so that the game is no longer in face card mode.
    face_mode["face_player"] = -1
    face_mode["amount"] = -1
    face_mode["card_player"] = -1
    # Returns the winning player's number, so it can be assigned to turn.
    return winner

def turn_check(player_packs, turn, face_mode, card_pile, event, location, key):
    '''Checks all the various things that need to be checked each turn.'''
    # Defined in case the player runs out of cards while
    # in face card mode.
    if len(player_packs[face_mode["card_player"]].hand) == 0 and face_mode["face_player"] != -1:
        turn = face_win(player_packs, card_pile, face_mode)
    # The player who played the face card won.
    elif face_mode["amount"] == 0 and face_mode["face_player"] != -1:
        turn = face_win(player_packs, card_pile, face_mode)
    # If face mode is on set card player to face_mode["card_player"]
    # Otherwise use turn as card player
    elif event.type == pygame.KEYDOWN and event.key == key:
        card_loser = turn
        if face_mode["face_player"] != -1:
            card_loser = face_mode["card_player"]
        game_turn(player_packs[card_loser].hand, card_pile, location)
        if face_mode["face_player"] == -1 and turn != 3:
            turn += 1
        elif face_mode["face_player"] == -1 and turn == 3:
            turn = 0
        # The face card mode is on, and thus the turn isn't changed.
        else:
            face_mode["amount"] -= 1
        location["angle"] -= 5
    return turn

def slap_check(card_pile, player_packs, player, turn, players, face_mode, location):
    '''Checks whether a slap was premature or victorious.'''
    # A safeguard in case someone slaps before two cards have been played.
    if len(card_pile) < 2:
        current_card = "cmon matto"
        previous_card = "lolnoob"
    else:
        current_card = card_pile[-1].value
        previous_card = card_pile[-2].value
    # Checks for the sandwich rule. Needs to be defined separately so the
    # regular slaps aren't affected.
    if len(card_pile) < 3:
        sandwich_card = "embarassing"
    else:
        sandwich_card = card_pile[-3].value
    # Checks if the slapping player was victorious.
    if current_card == previous_card or current_card == sandwich_card:
        text = "P{0} won the slap".format(player+1)
        draw_text(text, GREEN, False)
        # Adds the played cards to the slap winner's cards.
        player_packs[player].hand.extend(card_pile)
        # Empties the played cards.
        del card_pile[:]
        # Clears the face card mode, if it is active.
        face_mode["face_player"] = -1
        face_mode["amount"] = -1
        # The winner of the slap plays next.
        return player
    # If the player slapped prematurely, the other players get given a card;
    # unless they have no cards.
    else:
        loser_hand = player_packs[player].hand
        num_players = []
        for i in range(0,4):
            if len(player_packs[i].hand) > 0 and i != player:
                num_players.append(i)
        if len(loser_hand) >= len(num_players):
            for i in num_players:
                player_packs[i].hand.append(loser_hand[0])
                loser_hand.pop(0)
        else:
            for i in range(0, len(loser_hand)):
                game_turn(loser_hand, card_pile, location)
        # Draws the losing text on the screen.
        text = "P{0} lost the slap".format(player+1)
        draw_text(text, RED, True)
        # The next turn remains unchanged.
        return turn

def main():
    # Designates the number of players at the start of the game.
    players = 4
    turn = 0
    # These are defined in a dictionary, so the angle's value
    # can be changed in a function without a return value.
    # Also possibly the x and y coordinates later if needed.
    location = {
        "x" : 40,
        "y" : 40,
        "angle" : 0
    }
    # Used for keeping track of the face card mode.
    # face_player designates the player who played the face card.
    # card_player designates the player who plays cards.
    # Amount designates the amount of cards the next player must play.
    # Also defined in a dictionary, so the values can be changed in functions.
    # Facemode numbers correspond player indices in player_packs list.
    face_mode = {
        "face_player" : -1,
        "amount" : -1,
        "card_player": -1
    }
    # Used to prevent the face card mode from being initiated by
    # the same card.
    previous_card = 0
    running = True
    card_pile = []
    player_packs = card_loader(players, card_pile, location)
    while running:
        victory_check(player_packs)
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
                        if face_mode["face_player"] == -1 and turn != 0:
                            # Subtracting one because turn has already been
                            # changed in the turn_check function.
                            face_mode["face_player"] = turn-1
                            face_mode["card_player"] = turn
                        elif face_mode["face_player"] == -1 and turn == 0:
                            face_mode["face_player"] = 3
                            face_mode["card_player"] = 0
                        # If face mode was previously active.
                        elif face_mode["face_player"] > -1:
                            if turn != 3:
                                face_mode["face_player"] = turn
                                face_mode["card_player"] = (turn + 1)%4
                                turn = face_mode["card_player"]
                            else:
                                face_mode["face_player"] = 3
                                face_mode["card_player"] = 0
                                turn = 0
                        # If card_player has no cards, go to the next player.
                        if (len(player_packs[face_mode["card_player"]].hand)) == 0:
                            face_mode["card_player"] = (face_mode["card_player"]+1)%4
                            turn = face_mode["card_player"]
                            # Go to the next player if he has cards left.
                            if (len(player_packs[face_mode["card_player"]].hand) == 0 and 
                            len(player_packs[(face_mode["card_player"]+1)%4].hand) != 0):
                                face_mode["card_player"] = (face_mode["card_player"]+1)%4
                                turn = face_mode["card_player"]
                                
            # Skips the players turn if they don't have any cards
            if len(player_packs[turn].hand) == 0:
                if turn != 3:
                        turn += 1
                else:
                    turn = 0
            # Turn events for each player.
            if turn == 0:
                turn = turn_check(player_packs, turn, face_mode, card_pile, event,
                location, pygame.K_w)

            elif turn == 1:
                turn = turn_check(player_packs, turn, face_mode, card_pile, event,
                location, pygame.K_u)

            elif turn == 2:
                turn = turn_check(player_packs, turn, face_mode, card_pile, event,
                location, pygame.K_s)

            elif turn == 3:
                turn = turn_check(player_packs, turn, face_mode, card_pile, event,
                location, pygame.K_j)

            # The slap events for each player.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                turn = slap_check(card_pile, player_packs, 0, turn, players,
                face_mode, location)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                turn = slap_check(card_pile, player_packs, 1, turn, players,
                face_mode, location)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                turn = slap_check(card_pile, player_packs, 2, turn, players,
                face_mode, location)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                turn = slap_check(card_pile, player_packs, 3, turn, players,
                face_mode, location)

            # Inserts the remaining card amounts onto the window.
            remaining_cards(len(player_packs[0].hand), len(player_packs[1].hand),
            len(player_packs[2].hand), len(player_packs[3].hand), len(card_pile))

        pygame.display.update()

if __name__ == "__main__":
    main()