from core.module_entity.entity import entity
import pygame
from core.globals import screen, images

# Singleton class for the player, allowing it to inherit properly from entity.
# Constructing new instances is ill-advised, though technically possible.
class player_class(entity):
  # Set of all valid player variants.
  # Key: id, Val: file name hint
  variants = {
    "base": "base",
    "gold": "gold",
    "red": "red",
    "skull": "skull"
  }
  # Entity type used to distinguish subclasses
  type = "player"

  def __init__(this):
    # Player is created facing upwards by default.
    entity.__init__(this, "player", 0, 0, -90, 128/512)
    this.health = 100
    this.radius = 64
    this.speed = 400
    this.mainfire = "base"
    this.altfire = "base"
    this.update_graphics()

  def setVariant(this, var = "base"):
    # Optionally set variant of this player
    this.variant = var

    # Reset invalid variants
    if not (this.variant in player_class.variants):
      this.variant = player_class.variants["base"]
    
    # General loading
    this.sprite = images[f"player_{this.variant}"]
    this.update_graphics(True

  # Called after game is loaded and player entity is created.
  def load(this, var = "base"):
    this.setVariant(var)
    this.x = screen.w / 2
    this.y = screen.h - 128

  def damage(this, amt):
    this.health -= amt # Limited effects for now
    if this.health <= 0:
      this.alive = False

  def update(this, dt):
    entity.update(this, dt)

  def shoot(this, mode = "main", offset = False):
    if mode == "main":
      entity.shoot(this, this.mainfire, offset)
    else:
      entity.shoot(this, this.altfire, offset)

# Load appropriate images for player variants
# Todo: find some way to move this to the load event
for key, val in player_class.variants:
  images[f"player_{key}"] = pygame.image.load(f"assets\image\player\player_{val}.png")

player = player_class()
