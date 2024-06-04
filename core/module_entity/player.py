from core.module_entity.entity import entity
import pygame
from core.globals import screen

# Singleton class for the player, allowing it to inherit properly from entity.
# Constructing new instances is ill-advised, though technically possible.
class player_class(entity):
  # Set of all valid player variants.
  # Key: id, Val: filename
  variants = {
    "base": "base"
  }
  # Entity type used to distinguish subclasses
  type = "player"

  def __init__(this):
    # Player is created facing upwards by default.
    entity.__init__(this, "player", 0, 0, -90, 128/512)
    this.health = 100
    this.radius = 64
    this.speed = 400
    this.update_graphics()

  def setVariant(this, var = "base"):
    # Optionally set variant of this player
    this.variant = var

    # Reset invalid variants
    if not (this.variant in player_class.variants):
      this.variant = player_class.variants["base"]
    
    # General loading
    this.sprite = pygame.image.load(f"assets\image\player\player_{this.variant}.png")
    this.update_graphics()

  # Called after game is loaded and player entity is created.
  def load(this, var = "base"):
    this.setVariant(var)
    this.x = screen.w / 2
    this.y = screen.h - 128

  def damage(this, amt):
    this.health -= amt # Limited effects for now

  def update(this, dt):
    entity.update(this, dt)

  def fire(this, variant = "base", offset = False):
    entity.fire(this, "player", variant, offset)

player = player_class()