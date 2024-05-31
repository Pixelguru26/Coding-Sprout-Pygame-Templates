import pygame
import core as game
import random

basicEnemySpawnTimer = 0
basicEnemySpawnDelay = 1

images = {}

def load():
	game.player_class.load()

def update(dt):
	global basicEnemySpawnTimer
	global basicEnemySpawnDelay

	# Update player
	speed = 400
	if game.keyIsDown("left"):
		game.player_class.x -= speed * dt
	if game.keyIsDown("right"):
		game.player_class.x += speed * dt
	if game.keyIsDown("up"):
		game.player_class.y -= speed * dt
	if game.keyIsDown("down"):
		game.player_class.y += speed * dt
	
	game.player_class.x = game.clampX(game.player_class.x)
	game.player_class.y = game.clampY(game.player_class.y)

	# Spawn enemies
	basicEnemySpawnTimer += dt
	while basicEnemySpawnTimer > basicEnemySpawnDelay:
		# Reset timer but retain progress past the last spawn
		basicEnemySpawnTimer -= basicEnemySpawnDelay
		# Reset delay until next spawn to a random value
		basicEnemySpawnDelay = random.randrange(1, 2)
		# Spawn enemy offscreen at a random x position
		game.addEnemy("base", random.randrange(32, 1024-32), -32)
	
	# Update bullets
	for bullet in game.bullets:
		bullet.forward(1024 * dt)

	# Update enemies
	for entity in game.entities:
		# Enemy movement patterns and ai
		if entity.type == "base": # Base enemy ai
			entity.y += 200 * dt

		# Collide with bullets
		for bullet in game.bullets:
			if entity.intersects(bullet):
				bullet.impact(entity)
		
		# Collide with player
		if entity.intersects(game.player_class):
			game.player_class.damage(1)
			entity.health = 0

		# Enemy deletion
		if not entity.intersects(game.screen): # Cull off-screen enemies
			entity.alive = False
		elif entity.health <= 0: # Remove dead enemies
			entity.detonate()
			entity.alive = False

def draw():
	for bullet in game.bullets:
		if bullet.type == "base":
			game.graphics.draw(images["bullet_base"], bullet.x, bullet.y, bullet.scale, bullet.angle)
	
	game.player_class.draw()

	for entity in game.entities:
		if entity.type == "base":
			game.graphics.draw(images["enemy_base"], entity.x, entity.y, entity.scale, entity.angle)

def keydown(key, mod, unicode, scancode):
  # Handle key presses
	if key == pygame.K_SPACE:
		game.player_class.fire("base")

def keyup(key, mod, unicode, scancode):
  # Handle key releases
  pass

def mousedown(button, x, y):
  # Handle mouse button presses
  pass

def mouseup(button, x, y):
  # Handle mouse button releases
  pass