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

  # Exercise 2: "secrets"
  # This code is used in "try_secret()" to unlock a hidden variant.
  secret = "A113"
  # This code is read from the secret_# variables
  # When copied to the secret_digit_# variables, update will unlock a hidden ability
  secret_1 = 2
  secret_2 = 3
  secret_3 = 1
  secret_4 = 9
  secret_digit_1 = 0
  secret_digit_2 = 0
  secret_digit_3 = 0
  secret_digit_4 = 0

  def __init__(this):
    # Player is created facing upwards by default.
    entity.__init__(this, "player", 0, 0, -90, 128/512)
    this.health = 100
    this.radius = 64
    this.speed = 400
    this.mainfire = "base"
    this.altfire = "rocket"
    # Shots fired per second. If 0, semi automatic firing.
    this.main_fire_rate = 10
    this.alt_fire_rate = 0
    this.__main_fire_timer = 0
    this.__alt_fire_timer = 0
    this.__main_fire_state = False
    this.__alt_fire_state = False
    this.__main_fire_offset = (10, 0)
    this.__alt_fire_offset = (32, 0)
    # Ammunition per fire type. Infinite if negative.
    this.ammo_base = 2000
    this.ammo_rocket = 10
    this.__lastVariant = None
    this.update_graphics()

  def setVariant(this, var = "base"):
    # Optionally set variant of this player
    this.variant = var

    # Reset invalid variants
    if not (this.variant in player_class.variants):
      this.variant = player_class.variants["base"]
    
    # General loading
    this.sprite = images[f"player_{this.variant}"]
    this.update_graphics(True)
    this.__lastVariant = this.variant

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
    if this.variant != this.__lastVariant:
      this.setVariant(this.variant)
    
    if this.__main_fire_state and this.main_fire_rate > 0:
      this.__main_fire_timer += dt
      while this.__main_fire_timer >= 1/this.main_fire_rate:
        this.__main_fire_timer -= 1/this.main_fire_rate
        # Update bullet by subframe delta time after firing
        this.shoot("main").update(this.__main_fire_timer)
    if this.__alt_fire_state and this.alt_fire_rate > 0:
      this.__alt_fire_timer += dt
      while this.__alt_fire_timer >= 1/this.alt_fire_rate:
        this.__alt_fire_timer -= 1/this.alt_fire_rate
        # Update bullet by subframe delta time after firing
        this.shoot("alt").update(this.__alt_fire_timer)

    entity.update(this, dt)
  
  # Begins automatic firing of an ammo type
  def begin_fire(this, mode = "main"):
    if mode == "main":
      this.__main_fire_timer = 0
      this.__main_fire_state = True
    elif mode == "alt":
      this.__alt_fire_timer = 0
      this.__alt_fire_state = True
    this.shoot(mode)

  # Ends automatic firing of an ammo type
  def end_fire(this, mode = "main"):
    if mode == "main":
      this.__main_fire_state = False
    elif mode == "alt":
      this.__alt_fire_state = False

  # Causes the player to attempt to fire either its main or alt weapon.
  # Automatically includes ammo checking and use.
  # Set override to "True" to skip ammo checking.
  # "ammouse" determines how much the ammunition is depleted by.
  def shoot(this, mode = "main", override = False, ammouse = 1):
    if mode == "main":
      # Prevent fire if ammo is ~0.
      # Comparisons used to handle float cases sensibly.
      if not override:
        if this.ammo_base < 1 and this.ammo_base >= 0: return
        this.ammo_base -= ammouse
      # Alternating fire offset
      this.__main_fire_offset = (-this.__main_fire_offset[0], -this.__main_fire_offset[1])
      return entity.shoot(this, this.mainfire, this.__main_fire_offset)
    else:
      # Prevent fire if ammo is ~0.
      # Comparisons used to handle float cases sensibly.
      if not override:
        if this.ammo_rocket < 1 and this.ammo_rocket >= 0: return
        this.ammo_rocket -= ammouse
      # Alternating fire offset
      this.__alt_fire_offset = (-this.__alt_fire_offset[0], -this.__alt_fire_offset[1])
      return entity.shoot(this, this.altfire, this.__alt_fire_offset)

# Load appropriate images for player variants
# Todo: find some way to move this to the load event
for key in player_class.variants:
  val = player_class.variants[key]
  images[f"player_{key}"] = pygame.image.load(f"assets\image\player\player_{val}.png")

player = player_class()
