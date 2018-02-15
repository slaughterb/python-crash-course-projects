import pygame.font

class Button():

    def __init__(self, game_settings, screen, message):
        ''' init attributes '''
        self.screen = screen
        self.screen_rect = screen.get_rect()

        ''' set button dimensions and properties: '''
        self.width = 200
        self.height = 50
        self.button_color = (255,255,0)
        self.text_color = (0,0,0)
        self.text = "Play!"
        self.font = pygame.font.SysFont(None, 48)

        # build button's rect, center it:
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        self.render_message()

    def render_message(self):
        ''' turn the message into a rendered image;
        center the text on the button '''
        self.text_image = self.font.render(self.text, True, self.text_color, self.button_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.rect.center

    def draw_button(self):
        #draw blank button, then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.text_image, self.text_image_rect)