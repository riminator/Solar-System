import pygame
import math
pygame.init()

WIDTH, HEIGHT =  1800, 1800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (211, 211, 211)
ORANGE = (255, 165, 0)
JUPITER_COLOR = (235, 243, 246)
LIGHT_BROWN = (196, 164, 132)
LIGHT_BLUE = (173, 216, 230)
MIDNIGHT_BLUE = (25, 25, 112)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
  AU = 149.6e6 * 1000
  G = 6.67428e-11
  SCALE = 150 / AU
  TIMESTEP = 3600*24 

  def __init__(self, x, y, radius, color, mass):
    self.x = x
    self.y = y
    self.radius = radius
    self.color = color
    self.mass = mass

    self.orbit = []
    self.sun = False
    self.distance_to_sun = 0

    self.x_vel = 0
    self.y_vel = 0

  def draw(self, win, planet_names):
    x = self.x * self.SCALE + WIDTH / 2
    y = self.y * self.SCALE + HEIGHT / 2

    if len(self.orbit) > 2:
      updated_points = []
      for point in self.orbit:
        x, y = point
        x = x * self.SCALE + WIDTH / 2
        y = y * self.SCALE + HEIGHT / 2
        updated_points.append((x, y))

      pygame.draw.lines(win, self.color, False, updated_points, 2)

    pygame.draw.circle(win, self.color, (x, y), self.radius)

    if not self.sun:
      distance_text = FONT.render(planet_names[self], 1, WHITE)
      win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

  def attraction(self, other):
    other_x, other_y = other.x, other.y
    distance_x = other_x - self.x
    distance_y = other_y - self.y
    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

    if other.sun:
      self.distance_to_sun = distance

    force = self.G * self.mass * other.mass / distance**2
    theta = math.atan2(distance_y, distance_x)
    force_x = math.cos(theta) * force
    force_y = math.sin(theta) * force
    return force_x, force_y

  def update_position(self, planets):
    total_fx = total_fy = 0
    for planet in planets:
      if self == planet:
        continue

      fx, fy = self.attraction(planet)
      total_fx += fx
      total_fy += fy

    self.x_vel += total_fx / self.mass * self.TIMESTEP
    self.y_vel += total_fy / self.mass * self.TIMESTEP

    self.x += self.x_vel * self.TIMESTEP
    self.y += self.y_vel * self.TIMESTEP
    self.orbit.append((self.x, self.y))

sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
sun.sun = True

earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
#earth = Planet(-1 * Planet.AU * Planet.SCALE, 0, 16, BLUE, 5.9742 * 10**24)
earth.y_vel = 29.783 * 1000 

mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
#mars = Planet(-1.524 * Planet.AU * Planet.SCALE, 0, 12, RED, 6.39 * 10**23)
mars.y_vel = 24.077 * 1000

mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
#mercury = Planet(0.387 * Planet.AU * Planet.SCALE, 0, 8, DARK_GREY, 3.30 * 10**23)
mercury.y_vel = -47.4 * 1000

venus = Planet(0.723 * Planet.AU, 0, 14, ORANGE, 4.8685 * 10**24)
#venus = Planet(0.723 * Planet.AU * Planet.SCALE, 0, 14, ORANGE, 4.8685 * 10**24)
venus.y_vel = -35.02 * 1000

jupiter = Planet(4.249 * Planet.AU, 0, 20, JUPITER_COLOR, 1.898 * 10**27)
#jupiter = Planet(4.249 * Planet.AU * Planet.SCALE, 0, 20, JUPITER_COLOR, 1.898 * 10**27)
jupiter.y_vel = 13.07 * 1000

saturn = Planet(9.5 * Planet.AU, 0, 18, LIGHT_BROWN, 5.683 * 10**26)
#saturn = Planet(9.5 * Planet.AU * Planet.SCALE, 0, 18, LIGHT_BROWN, 5.683 * 10**26)
saturn.y_vel = 10.14 * 1000

uranus = Planet(19.8 * Planet.AU, 0, 10, LIGHT_BLUE, 8.681 * 10**25)
#uranus = Planet(19.8 * Planet.AU * Planet.SCALE, 0, 10, LIGHT_BLUE, 8.681 * 10**25)
uranus.y_vel = 24.607 * 1000

neptune = Planet(30 * Planet.AU, 0, 10, MIDNIGHT_BLUE, 1.024 * 10**26)
#neptune = Planet(30 * Planet.AU * Planet.SCALE, 0, 10, MIDNIGHT_BLUE, 1.024 * 10**26)
neptune.y_vel = 5.45 * 1000

def create_planet_names():
    return {
    sun: "Sun",
    mercury: "Mercury",
    venus: "Venus",
    earth: "Earth",
    mars: "Mars",
    jupiter: "Jupiter",
    saturn: "Saturn",
    uranus: "Uranus",
    neptune: "Neptune"  
    }

def main():
  run = True
  clock = pygame.time.Clock()

  planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]
  planet_names = create_planet_names()

  while run:
    clock.tick(60)
    WIN.fill((0, 0, 0))

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    for planet in planets:
      planet.update_position(planets)
      planet.draw(WIN, planet_names)

    pygame.display.update()

  pygame.quit()
  
main()