import pygame
import random
import math

# --- Initialization ---
pygame.init()
WIDTH, HEIGHT = 800, 700  # Made height taller for more play space
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elemental Particle Canvas")
clock = pygame.time.Clock()

# --- Constants & Colors ---
BACKGROUND_COLOR = (10, 10, 25) # A dark navy blue
GRAVITY = pygame.Vector2(0, 0.3)
FONT = pygame.font.SysFont("Arial", 18)

# --- The Unified Particle Class ---
class Particle:
    def __init__(self, x, y, particle_type):   # <-- FIXED HERE
        self.type = particle_type
        self.pos = pygame.Vector2(x, y)
        self.is_alive = True

        # --- Behavior Customization Based on Type ---
        if self.type == 'water':
            self.vel = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 2))
            self.radius = random.randint(4, 6)
            self.lifespan = 255
            self.color = (50, 100, 255)

        elif self.type == 'smoke':
            self.vel = pygame.Vector2(random.uniform(-0.5, 0.5), random.uniform(-2, -0.5))
            self.radius = random.randint(15, 25)
            self.lifespan = random.randint(80, 150)
            self.color = [random.randint(50, 80)] * 3 

        elif self.type == 'sparks':
            angle = random.uniform(-math.pi / 2, -math.pi * 3/2)
            speed = random.uniform(2, 5)
            self.vel = pygame.Vector2(math.sin(angle) * speed, math.cos(angle) * speed)
            self.radius = random.randint(2, 4)
            self.lifespan = random.randint(40, 70)
            self.color = (255, random.randint(150, 200), 0)

        elif self.type == 'swarm':
            self.vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
            self.radius = random.randint(3, 5)
            self.lifespan = random.randint(100, 200)
            self.color = (150, 255, 100)
            self.wander_angle = random.uniform(0, 2 * math.pi)

        elif self.type == 'bubbles':
            self.vel = pygame.Vector2(random.uniform(-0.3, 0.3), random.uniform(-2, -1))
            self.radius = random.randint(8, 16)
            self.lifespan = random.randint(150, 300)
            self.color = (180, 220, 255)

    def update(self):
        self.lifespan -= 1
        if self.lifespan <= 0:
            self.is_alive = False
            return

        if self.type == 'water':
            self.vel += GRAVITY
            if self.pos.y > HEIGHT - 10:
                self.vel.y *= -0.4
                self.vel.x *= 0.8
                self.pos.y = HEIGHT - 10
            if abs(self.vel.y) < 0.1:
                self.lifespan -= 5
        
        elif self.type == 'smoke':
            self.vel *= 0.98
            self.radius -= 0.1
            if self.radius <= 0:
                self.is_alive = False
            for i in range(3): 
                self.color[i] = max(0, self.color[i] - 0.5)

        elif self.type == 'sparks':
            self.vel += GRAVITY * 0.5
            r, g, b = self.color
            if g > 50: g -= 3
            self.color = (r, g, b)

        elif self.type == 'swarm':
            self.wander_angle += random.uniform(-0.4, 0.4)
            turn_vec = pygame.Vector2(math.cos(self.wander_angle), math.sin(self.wander_angle))
            self.vel += turn_vec * 0.3
            if self.vel.length() > 2:
                self.vel.scale_to_length(2)
            if not (0 < self.pos.x < WIDTH): self.vel.x *= -1
            if not (0 < self.pos.y < HEIGHT): self.vel.y *= -1

        elif self.type == 'bubbles':
            self.pos.x += math.sin(self.pos.y / 20) * 0.5
            if self.pos.y < 0:
                self.is_alive = False
            
        self.pos += self.vel

    def draw(self, surface):
        if not self.is_alive:
            return

        if self.type == 'smoke':
            temp_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (*self.color, 100), (self.radius, self.radius), self.radius)
            surface.blit(temp_surf, (self.pos.x - self.radius, self.pos.y - self.radius), special_flags=pygame.BLEND_RGBA_ADD)
        
        elif self.type == 'bubbles':
            temp_surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (*self.color, 80), (self.radius, self.radius), self.radius)
            pygame.draw.circle(temp_surf, (*self.color, 200), (self.radius, self.radius), self.radius, 1)
            surface.blit(temp_surf, (self.pos.x - self.radius, self.pos.y - self.radius), special_flags=pygame.BLEND_RGBA_ADD)
        
        else:
            pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), int(self.radius))


# --- Main Game Setup ---
particles = []
current_mode = 'water'
running = True

# --- UI Button Setup ---
button_rects = {
    'water': pygame.Rect(10, 10, 100, 40),
    'smoke': pygame.Rect(120, 10, 100, 40),
    'sparks': pygame.Rect(230, 10, 100, 40),
    'swarm': pygame.Rect(340, 10, 100, 40),
    'bubbles': pygame.Rect(450, 10, 100, 40)
}
button_colors = {
    'water': (50, 100, 255),
    'smoke': (100, 100, 100),
    'sparks': (255, 150, 0),
    'swarm': (150, 255, 100),
    'bubbles': (180, 220, 255)
}

def draw_ui(surface):
    for mode, rect in button_rects.items():
        color = button_colors[mode]
        if mode == current_mode:
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (255, 255, 255), rect, 3)
        else:
            pygame.draw.rect(surface, color, rect, 3)
        
        text = FONT.render(mode.title(), True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)

# --- Game Loop ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for mode, rect in button_rects.items():
                    if rect.collidepoint(event.pos):
                        current_mode = mode
                        break

    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        is_on_button = any(rect.collidepoint(mouse_pos) for rect in button_rects.values())
        if not is_on_button:
            for _ in range(5):
                particles.append(Particle(mouse_pos[0], mouse_pos[1], current_mode))

    screen.fill(BACKGROUND_COLOR)

    particles = [p for p in particles if p.is_alive]
    
    for p in particles:
        p.update()
        p.draw(screen)

    draw_ui(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
