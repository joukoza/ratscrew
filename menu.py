import pygame

pygame.init()
win_width, win_height = 1000, 700
win = pygame.display.set_mode((win_width, win_height))

class button():
    '''Button for navigating in the menu'''
    def __init__(self, surface, location, size, color, text=None):
        self.surface = surface
        self.location = location
        self.size = size
        self.color = color
        self.text = text
        self.drawcolor = self.color
        
        ## Defines darker color for push animation
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
        pygame.draw.rect(self.surface, self.drawcolor, rect)
        
        ## Calculates the right font size
        button_size = (self.size[0], self.size[1])
        font_size = self.size[0]
        font = pygame.font.SysFont("./data_files/BlackOpsOne-Regular.ttf", font_size)
        
        while font.size(self.text)[0] >= (button_size[0]) or \
        font.size(self.text)[1] >= (button_size[1]):
            font_size -= 1
            font = pygame.font.SysFont("./data_files/BlackOpsOne-Regular.ttf", font_size)

        ## Writes the text on the button
        text_locationx = self.location[0] + (self.size[0] - font.size(self.text)[0]) // 2
        text_locationy = self.location[1] + (self.size[1] - font.size(self.text)[1]) // 2
        text_location = (text_locationx, text_locationy)
        text_surface = font.render(self.text, True, (255, 255, 255))
        self.surface.blit(text_surface, text_location)

    def update(self):
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
        else:
            self.drawcolor = self.color

def menu():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    
    text1 = "Settings"
    b_1 = button(win, ((win_width - 200) // 2, (win_height - 100) // 2), \
    (200, 100), RED, text1)
    text2 = "Highscores"
    b_2 = button(win, ((win_width - 200) // 2, (win_height - 100) // 2 + 200),\
    (200, 100), RED, text2)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        win.fill(BLACK)
        b_1.update()
        b_1.show()
        b_2.update()
        b_2.show()
        ## win.blit(text_surface, location)
        pygame.display.update()

    pygame.quit()

menu()