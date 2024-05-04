import pygame


class Button():
    def __init__(self, window: pygame.Surface, x: int, text: str = ""):
        self.WINDOW = window
        self.WINDOW_WIDTH: int = window.get_width()
        self.WINDOW_HEIGHT: int = window.get_height()
        
        self.x = x
        self.y = 0
        
        self.width: float = window.get_width()/8
        self.height: int = 20
        
        self.string = text
        
        self.color: tuple[int] = (50, 50, 50)
        self.colorActive: tuple[int] = (100, 100, 100)
        self.textColor: tuple[int] = (255, 255, 255)
        
        self.FONT = pygame.font.SysFont("comicsan", 20)
        self.text: pygame.Surface = self.FONT.render(self.string, True, self.textColor)
        
        self.txt: str = text
        
        self.hitbox: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.active: bool = False
    
    def press(self) -> bool:
        if pygame.mouse.get_pressed()[0]:
            mouse = pygame.mouse.get_pos()
            
            if self.hitbox.collidepoint(mouse[0], mouse[1]):
                return True
    
    def draw(self) -> None:
        if self.active:
            pygame.draw.rect(self.WINDOW, self.colorActive, self.hitbox)
        else:
            pygame.draw.rect(self.WINDOW, self.color, self.hitbox)
        
        self.WINDOW.blit(self.text, (self.x + self.width/2 - self.text.get_width()/2, self.y + self.text.get_height()/2))
