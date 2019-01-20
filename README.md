# ratscrew-windows

Keys:
P1: "w" for a card
    "e" for a slap
    
P2: "u" for a card
    "i" for a slap
   
P3: "s" for a card
    "d" for a slap
    
P4: "j" for a card
    "k" for a slap

TODO:
ratscrew.py:

The game crashes if somebody makes a wrong slap and doesn't have enough cards
to give to other players.

Related to the previous one, the for-loop that handles the wrong slaps in slap_check
uses players, which is currently defined only in main. So if someone were to join
in the middle of the game, they wouldn't get cards from the player who made the wrong slap.

Possibly add a separate function that handles all window updates.

Add more comments to the code.

Add the sandwich rule (and possibly a way to easily turn it off).
