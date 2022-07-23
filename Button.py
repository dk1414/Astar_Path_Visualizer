
import pygame


class Button:
    def __init__(self,screen,text,width,height,pos,pressed_func):

        self.screen = screen
        self.orig_pos = pos

        self.pressed = False
        self.pressed_func = pressed_func
        self.elevation = 6

        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = (200,200,200)

        self.font = pygame.font.SysFont('georgia', 20)

        self.top_rect_text = self.font.render(text, True, (0,0,0))

        self.top_text_rec = self.top_rect_text.get_rect()
        self.top_text_rec.center = (self.top_rect.center)

        self.bottom_rect = pygame.Rect(pos,(width,self.elevation))
        self.bottom_color = (150,150,150)


    def draw(self):

        self.top_rect.y = self.orig_pos[1] - self.elevation
        self.top_text_rec.center = self.top_rect.center



        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.elevation

        pygame.draw.rect(self.screen,self.bottom_color,self.bottom_rect,border_radius=10)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=10)
        self.screen.blit(self.top_rect_text, self.top_text_rec)

        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = (100,100,100)
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                self.elevation = 0
            elif self.pressed:
                self.pressed_func()
                self.pressed = False
                self.elevation = 6
        else:
            self.top_color = (200,200,200)
            self.elevation = 6