import pygame

pygame.init()
win_width, win_height = 1000, 700
win = pygame.display.set_mode((win_width, win_height))

class button():
    '''Button for navigating in the menu'''
    def __init__(self, location, size, color, text=None):
        self.location = location
        self.size = size
        self.color = color
        self.text = text

    def show(self, surface):
        '''Draws the button on a surface'''
        ## Draws the button
        rect = (self.location[0], self.location[1], self.size[0], \
        self.size[1])
        pygame.draw.rect(surface, self.color, rect)
        
        ## Calculates the right font size
        button_size = (self.size[0], self.size[1])
        font_size = self.size[0]
        font = pygame.font.SysFont("timesnewroman", font_size)
        
        while font.size(self.text)[0] >= (button_size[0]) or \
        font.size(self.text)[1] >= (button_size[1]):
            font_size -= 1
            font = pygame.font.SysFont("timesnewroman", font_size)

        ## Writes the text on the button
        text_locationx = self.location[0] + (self.size[0] - font.size(self.text)[0]) // 2
        text_locationy = self.location[1] + (self.size[1] - font.size(self.text)[1]) // 2
        text_location = (text_locationx, text_locationy)
        text_surface = font.render(self.text, True, (255, 255, 255))
        surface.blit(text_surface, text_location)

    def pressed(self, on):
        colors = ['r', 'g', 'b']
        for i in range(4):
            if self.color[i] > 0:
                colors[i] = self.color[i] - 20

def menu():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    
    text = "Settings"
    b_1 = button(((win_width - 200) // 2, (win_height - 100) // 2), \
    (200, 100), RED, text)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        win.fill(BLACK)
        b_1.show(win)
        ## win.blit(text_surface, location)
        pygame.display.update()

    pygame.quit()

menu()