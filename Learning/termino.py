import pygame
import random
import time

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
CARD_WIDTH = 250
CARD_HEIGHT = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
PURPLE = (147, 112, 219)

# Game setup
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Advanced Termino - Learning Game")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.Font(None, 48)
font = pygame.font.Font(None, 32)
score_font = pygame.font.Font(None, 36)

# Game levels
LEVELS = {
    1: {
        "Algorithm": "Step-by-step procedure to solve a problem",
        "Variable": "Container for storing data",
        "Function": "Reusable block of code",
    },
    2: {
        "Loop": "Structure to repeat code",
        "Array": "Ordered collection of items",
        "Class": "Blueprint for creating objects",
    }
}

class DraggableItem:
    def __init__(self, text, x, y, is_term=True):
        self.text = text
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.original_pos = (x, y)
        self.dragging = False
        self.matched = False
        self.is_term = is_term
        self.highlight = False
    
    def draw(self, surface):
        if self.highlight:
            color = RED
        elif self.matched:
            color = GREEN
        else:
            color = BLUE if self.is_term else PURPLE
            
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def reset_position(self):
        self.rect.topleft = self.original_pos
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.rect.move_ip(event.rel)
        return False

class Game:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.term_items = []
        self.definition_items = []
        self.start_time = time.time()
        self.game_duration = 180  # 3 minutes
        self.setup_level()

    def setup_level(self):
        self.term_items.clear()
        self.definition_items.clear()
        
        terms = LEVELS[self.level]
        y_pos = 150
        for term, definition in terms.items():
            self.term_items.append(DraggableItem(term, 50, y_pos, True))
            self.definition_items.append(DraggableItem(definition, 650, y_pos, False))
            y_pos += 100

        # Randomize definition positions
        random.shuffle(self.definition_items)
        y_pos = 150
        for item in self.definition_items:
            item.rect.x = 650
            item.rect.y = y_pos
            item.original_pos = (650, y_pos)
            y_pos += 100

    def draw(self, screen):
        screen.fill(WHITE)
        
        # Draw title
        title = title_font.render(f"Level {self.level}", True, BLACK)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 20))
        
        # Draw score
        score_text = score_font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        
        # Draw timer
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.game_duration - elapsed_time)
        timer_text = score_font.render(f"Time: {int(remaining_time)}s", True, BLACK)
        screen.blit(timer_text, (WINDOW_WIDTH - 150, 20))
        
        # Draw items
        for item in self.term_items + self.definition_items:
            item.draw(screen)

    def run(self):
        running = True
        while running:
            screen.fill(WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle dragging events
                for item in self.term_items:
                    if not item.matched:
                        if item.handle_event(event):
                            break
                        
                        if event.type == pygame.MOUSEBUTTONUP and item.dragging:
                            matched = False
                            for def_item in self.definition_items:
                                if item.rect.colliderect(def_item.rect):
                                    if LEVELS[self.level][item.text] == def_item.text:
                                        item.matched = True
                                        def_item.matched = True
                                        self.score += 100
                                        matched = True
                                        
                                        # Check if level is complete
                                        if all(term.matched for term in self.term_items):
                                            self.level += 1
                                            if self.level <= len(LEVELS):
                                                self.setup_level()
                                            else:
                                                running = False
                                    break
                            
                            if not matched:
                                item.reset_position()
            
            # Check if time is up
            if time.time() - self.start_time >= self.game_duration:
                running = False
            
            self.draw(screen)
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
