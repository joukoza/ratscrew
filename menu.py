import pygame
import sys
import ratscrew

pygame.init()
win_width, win_height = 640, 480
win = pygame.display.set_mode((win_width, win_height))

class button():
    '''Button for navigating in the menu'''
    def __init__(self, surface, location, size, color, text=None):
        self.surface = surface
        self.location = location
        self.size = size
        self.color = color
        self.drawcolor = self.color
        self.text = text
        self.state = "NORMAL"
        
        ## Defines a darker color for the push animation
        colors = ['r', 'g', 'b']
        for i in range(3):
            if self.color[i] > 50:
                colors[i] = self.color[i] - 50
            else:
                colors[i] = self.color[i]
        self.darkcolor = (colors[0], colors[1], colors[2])

    def show(self):
        '''Draws the button on a surface'''
        ## Draws the button
        rect = (self.location[0], self.location[1], self.size[0], \
        self.size[1])
        pygame.draw.rect(self.surface, self.drawcolor, rect, 2)    
        
        font_size = 27
        font_path = "./data_files/BlackOpsOne-Regular.ttf"
        font = pygame.font.Font(font_path, font_size)
        
        ## Calculates the right font size
        ## MIGHT BE HANDY AT SOME POINT! DO NOT DELETE!
        ## button_size = (self.size[0], self.size[1])
        ## while font.size(self.text)[0] >= (button_size[0]) or \
        ## font.size(self.text)[1] >= (button_size[1]):
        ##    font_size -= 1
        ##    font = pygame.font.Font(font_path, font_size)

        ## print(font_size)

        ## Writes the text on the button
        text_locationx = self.location[0] + (self.size[0] - \
                         font.size(self.text)[0]) // 2
        text_locationy = self.location[1] + (self.size[1] - \
                         font.size(self.text)[1]) // 2
        text_location = (text_locationx, text_locationy)
        text_surface = font.render(self.text, True, (255, 255, 255))
        self.surface.blit(text_surface, text_location)

    def pressed(self):
        ## Gets states of all mouse buttons and position of the mouse
        mouse = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        ## Checks if the mouse is clicked
        if mouse[0] == True:
            ## Checks if the mouse is on the button
            x1 = self.location[0]
            x2 = self.location[0] + self.size[0]
            y1 = self.location[1]
            y2 = self.location[1] + self.size[1]
            if x1 <= mouse_pos[0] <= x2  and y1 <= mouse_pos[1] <= y2:
                self.drawcolor = self.darkcolor
                self.state = "DOWN"
        else:
            self.drawcolor = self.color
            
            if self.state == "DOWN":
                self.state = "UP"
                return False
            
            if self.state == "UP":
                self.state = "NORMAL"
                return True

def draw_text(font_size):
    width = win.get_width()
    font_path = "./data_files/BlackOpsOne-Regular.ttf"
    title_text = "R a t s c r e w"

    font = pygame.font.Font(font_path, font_size)
    title_size = font.size(title_text)
    title_location = ((width - title_size[0]) // 2, 10)
    title_surface = font.render(title_text, True, (255, 255, 255))
    win.blit(title_surface, title_location)

    if font_size > 85:
        font_size = font_size - 1
    
    return font_size

def menu():
    BLACK = (0, 0, 0)
    RED = (200, 0, 0)
    SIZE = (300, 100)
    MIDDLE = (win_width - SIZE[0]) // 2
    
    text1 = "PLAY"
    play = button(win, (MIDDLE, 150),\
    SIZE, RED, text1)

    text4 = "EXIT"
    ext = button(win, (MIDDLE, 330),\
    SIZE, RED, text4)
    
    ##text2 = "SETTINGS"
    ##settings = button(win, ((win_width - 200) // 2, 225), \
    ##200, 100), RED, text2)
    
    ##text3 = "HIGHSCORES"
    ##highscores = button(win, ((win_width - 200) // 2, 375),\
    ##(200, 100), RED, text3)
    
    font_size = 200

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        win.fill(BLACK)
        
        if play.pressed():
            ratscrew.main()
        play.show()

        if ext.pressed():
            sys.exit()
        ext.show()

        font_size = draw_text(font_size)

        pygame.display.update()

    sys.exit()

menu()