

## Main Loop

The main file provided in the corelib template provides a simple event loop and automatically binds user event handlers if they are provided. Corelib event handlers are considered the primary target, and are not optional.

User content should be provided in a module called "game". The main loop will load this module after corelib has been initialized to ensure all essential library functions are available and fully functional. Once loaded, the game module may provide any of the following event handler functions by simply defining them:
 - `load()`
  Called immediately after the module is loaded. Primarily semantic, though it can also be used to ensure code runs after other modules are loaded.
 - `update(dt)`
  Called every frame. dt is the time since the beginning of the last frame, in seconds. Precision is ensured down to 1/1000th of a second.
 - `draw()`
  Called every frame after update. The window is automatically cleared to black before each call to draw.
 - `keydown(id, mod, unicode, scancode)`
  Called whenever a key is pressed down. The id of the key is passed as a Pygame constant.
 - `keyup(id, mod, unicode, scancode)`
  Called whenever a key is released. The id of the key is passed as a Pygame constant.
 - `mousedown(button, x, y)`
  Called whenever the mouse is clicked. It is not guaranteed that the button will release due to unhandled releases outside the window. The button is passed as a Pygame constant.
 - `mouseup(button, x, y)`
  Called whenever the mouse is released. A prior call to mousedown is not guaranteed, as clicks outside the window are unhandled. The button is passed as a Pygame constant.

## Corelib Modules

Corelib is the primary interface for interacting with the game during runtime. A standard game script will import the main corelib module like so:
```python
import core as game
```
This will provide all necessary components of the module, accessible through the `game` object.

### Game module

The `game` object is the entrypoint into the corelib module. It contains many of the most immediately useful operations and tools for modifying the game's behavior, as well as global constants.

#### Objects:

 - `game.player`
  A direct reference to the singleton player object. See "entity submodules" for methods and members.
 - `game.screen`
  A dummy entity which only exists to provide the dimensions of the game window for collisions. Same methods and members as base entity.
 - `game.cullbox`
  A dummy entity which only exists to provide the dimensions of the culling bounds around the game window. Same methods and members as base entity.
 - `game.entities`
  A list of all active entities in the game. If an entity is not included here, it will not be displayed or updated by default.
 - `game.bullets`
  A list of all active projectiles in the game. If a projectile is not included here, it will not appear onscreen, update, or collide with entities by default.
 - `game.images`
  A utility dictionary for the sprites used by the game.
 - `game.base_spawn`
  The default `spawnTimer` instance, or `spawn`, which spawns enemies every 1-2 seconds. May be safely disabled by calling its `remove()` method.

#### Utilities:

 - `game.clamp(v, a, b)`
  Clamps the input number (v) to the range [a, b] (inclusive), and returns the result.
 - `game.wrap(v, a, b)`
  Wraps the input number (v) to the range [a, b), causing it to loop around if it exceeds either limit.
 - `game.lerp(v, a, b)`
  Performs linear interpolation between a and b on a single axis and returns the result. Does not clamp the input before the operation.
 - `game.addEnemy(variant, x, y, radius)`
  Constructs an enemy and adds it to the game. Returns a reference to the enemy object afterwards. Valid variants are:
    - `"base"`
 - `game.addBullet(variant, x, y, angle, damage, speed, scale)`
  Constructs a bullet and adds it to the game with no team designation (it will hit both players and enemies). Returns a reference to the bullet afterwards. Valid variants are:
    - `"base"`
 - `game.keyIsDown(key)`
  Returns the status of a key at the time of calling; `True` for pressed and `False` for unpressed. The key argument can be a Pygame key constant or a string designator from the `game.keys` constant, which will automatically be translated.
 - `game.project(x, y, x1, y1, x2, y2)`
  Vector projection of (x, y) onto a line segment defined by the endpoints (x1, y1) and (x2, y2). Equivalent to basic vector projection when (x1, y1) = (0, 0)
 - `game.dist(x1, y1, x2, y1)`
  Returns the Euclidean distance between the points (x1, y1) and (x2, y2)
 - `game.sign(v)`
  A more traditional sign function than Python provides. Returns `-1` if the value is negative, `1` if the value is positive, and `0` if the value is 0 or not a number.

#### Constants:

 - `game.keys`
  A dictionary used to translate between Pygame key constants and some user-friendly string representations.
 - `game.lightmode`
  A boolean value indicating whether the game should run in a "cpu-light" mode, disabling certain features for smaller devices or development on Replit. Note that this should not change the API significantly; dummy objects and classes will still be present but simply do nothing.

### Entity module

Accessible through `game.entity`

The entity class provides a base for all active game objects to inherit from, as well as access to the classes of the default objects. It can be instantiated directly, which can be used for convenient collision checks, as in the case of `game.screen` and `game.cullbox`. Any methods or members included here are inherited by `game.player` and any instances of `bullet` or `enemy`.

#### Entity class
##### Constructors
There are multiple valid constructor overloads, separated by the collision type (`"circle"`, `"aabb"`, or `"line"`). Default parameters are shared across all versions.
 - `__init__(team = "none", x = 0, y = 0, angle = 0, scale = 1, collisionType = "circle")`
  This is the default constructor if nothing is specified. Parameters are as follows:
  - `team` Indicates which attacks will connect with this entity. It can be any of the following values:
    - `"none"`
    - `"all"`
    - `"player"`
    - `"enemy"`
  Other values will be accepted, but will damage (and be damaged by) all other teams except `"all"`.
  - `x`, `y`
    Indicates the position of the entity. For circular entities, this indicates the center.
  - `angle`
    Indicates the rotation of the entity, in degrees. This behavior is entirely graphical and does not affect collisions at all.
  - `collisionType`
    Indicates what collision shape the entity should use. This also determines which overload of the constructor will be used.
 - `__init__(team, x, y, angle, scale, "circle", radius = 0)`
  This is the default constructor if no collision type is specified.
 - `__init__(team, x, y, angle, scale, "aabb", width = 0, height = 0)`
  `x` and `y` represent the coordinates of the top left corner of the entity.
 - `__init__(team, x, y, angle, scale, "line", x2 = 0, y2 = 0)`
  `x` and `y` serve as the coordinates of the first end point of the line segment. `x2` and `y2` are the coordinates of the second end point.
##### Methods
 - `update(dt)`
  Intended to be called every update tick with delta time (`dt`) provided in seconds. Handles basic optimizations as well as ai for derived classes. If the entity is registered to the game, calling this method is redundant.
 - `update_graphics(override = False)`
  An optimization method which updates caches if `rotation`, `scale`, or `sprite` have changed. Only call with `override = True` if the old values have been changed externally.
  Currently also required after changing `sprite`, as detection is unimplemented as of yet.
 - `draw()`
  Renders the entity to the screen with its appropriate attributes.
 - `intersects(target)`
  Returns `True` if this entity intersects with the target entity.

  The `"line"` collisionType is currently only partially supported.
 - `delete()`
  Sets the entity's `alive` status to `False`. Derived classes will use this to perform cleanup and animations. If the entity is registered to the game, it will be unregistered after this is called.
 - `forward(amount = 1)`
  Moves the entity forward according to its angle by the provided number of pixels.
 - `backward(amount = 1)`
  Moves the entity backward according to its angle by the provided number of pixels. Equivalent to `forward(-amount)`
 - `right(amount = 1)`
  Moves the entity to the right (strafes) according to its angle by the provided number of pixels.
 - `left(amount = 1)`
  Moves the entity to the left (strafes) according to its angle by the provided number of pixels. Equivalent to `right(-amount)`
 - `rotate(amount = 90)`
  Rotates the entity clockwise by the specified number of degrees.
 - `turnRight(amount = 90)`
  Rotates the entity clockwise by the specified number of degrees. Equivalent to `rotate(amount)`
 - `turnLeft(amount = 90)`
  Rotates the entity counter-clockwise by the specified number of degrees.
  Equivalent to `turnRight(-amount)`
 - `move(offset = (0, 0))`
  Moves the entity both forward and right. `offset` is a vector in which the first (or x) value indicates the movement to the right in pixels, and the second (or y) value indicates the movement forward in pixels.
 - `shoot(variant = "base", offset = (0, 0))`
  Fires a projectile from this entity, if the operation is supported. 
  `variant` may be any of `["base", "rocket"]`.
  `offset` is a vector oriented so that y+ is equivalent to forward from the parent entity, and x+ is equivalent to right. This is added to the projectile's position when it is created.
##### Static Members
- `collisionTypes`
  A dictionary containing all valid collisionTypes supported by the class. Contains the following values:
  - `"circle"`
  - `"aabb"` (rectangle)
  - `"line"` (line segment)
- `type`
  Indicates the type of this entity. Used for more convenient comparisons. In the base class, this evaluates to `"entity"`.
##### Instance Members
 - `team`
  The current "team" alignment of the entity. This determines which attacks will connect. It can be any of the following values:
  - `"none"`
  - `"all"`
  - `"player"`
  - `"enemy"`
  Other values will be accepted, but will damage (and be damaged by) all other teams except `"all"`.
 - `x`, `y`
  The location of the entity in pixels. Depending on the collision type, this will either be the center, top left corner, or first point of the entity.
  Note that corelib uses a "y-down" coordinate system, so that the coordinates (0, 0) represent the top left corner of the window. Increasing y values will move the entity further down the window.
 - `angle`
  The angle of the entity, in degrees clockwise from screen-East (facing directly to the right). Collisions are not affected by this value.
 - `scale`
  The visual scale of the entity. Image dimensions are multiplied by this amount when rendering. Does not affect collisions or movement speed.
 - `speed`
  The speed at which this entity will move. This is only used as a stat for the entity's ai, and must therefore be implemented by any derived classes.
 - `sprite`
  The source image which this entity will render to the screen after rotation and scaling.
  Currently, if this is changed, `update_graphics(True)` must be called manually, including the override argument.
 - `collisionType`
  A string indicating which of the three collision shapes apply to this entity. See `entity.collisionTypes` for valid options.
  Note that each option requires a different set of dimension values, which may not be assigned if this is changed after construction.
 - `alive`
  A boolean value indicating whether this entity is "alive" and should be updated, or "dead" and should be removed from the registry.
 - `last_angle`
  Internal optimization cache which should not be assigned by the user.
 - `last_scale`
  Internal optimization cache which should not be assigned by the user.
 - `sprite_cache`
  Internal optimization cache which should not be assigned by the user. Contains the appropriately rotated and scaled sprite for the entity.


#### Player class

Accessible through `game.player`

The player *instance* is a singleton of its class. The class itself should thus not be accessed or inherited.
By default, its `collisionType` is `"circle"`.

In addition to the methods and members provided by `game.entity`, the player includes the following:

##### Methods
 - `setVariant(var = "base")`
  Sets the variant of the player, if valid. This is (currently) only an aesthetic change.
  Valid variants are:
    - `"base"`
    - `"gold"`
    - `"red"`
    - `"skull"`
 - `load()`
  Called when the player is first loaded into the game. Should not be called by the user.
 - `damage(amount)`
  Damages the player by the specified amount.
  Note that there is currently no "death" condition.
 - `shoot(mode = "main", offset = False)`
  Fires a bullet from the player. `mode` can either be `"main"` or `"alt"`, which determines whether the player's main fire mode or alt fire mode is invoked.
##### Instance Members
 - `health`
  Begins at 100. Player is "killed" if it reaches 0.
 - `radius`
  The player has a collision radius of 64 by default. This does not affect graphical representation whatsoever.
 - `speed`
  The number of pixels the player will move per second while a control is pressed. By default, this is 400.
 - `mainfire`
  The primary fire mode of the player, invoked with the space bar. Eventually, this will enable switching to different projectiles. By default, this is set to `"base"`.
 - `altfire`
  The secondary fire mode of the player, invoked with the left shift key. Eventually, this will enable switching to different projectiles. By default, this is set to `"base"`.
##### Static Members
 - `type = "player"`

#### Enemy class

Accessible through `game.entity.enemy`

The enemy class is inherited by all enemies in the game. It provides the ai functionality and health behavior. Enemies are stored in the `game.entities` list and removed when killed.

In addition to the methods and members of `game.entity`, the enemy class provides the following:
##### Methods

##### Instance Members
 - `health`
  Begins at 100 by default.
 - `speed`
  This is the speed the entity will move at, in pixels per second. By default, this is 100.

##### Static Members
 - `type = "enemy_base"`

#### Bullet class

Accessible through `game.entity.bullet`

The bullet class is inherited by all projectiles in the game. These are handled slightly differently from general entities so that they can respond to collisions. Note that bullets currently do not collide with other bullets, however.

In addition to the methods and members of `game.entity`, the bullet class provides the following:
##### Methods
 - `impact(target)`
  Deals appropriate damage to the target and deletes this bullet. Generally, prefer `touch(target)` as the filtered version of this method accounting for teams.
 - `touch(target)`
  Deals appropriate damage to the target if it is on an opposing team, otherwise does nothing.

##### Instance Members
 - `speed`
  This is the speed the bullet will move at, in pixels per second. By default, this is 1024.
  Note that if the speed is too high, the bullet may skip over enemies without colliding.
 - `team`
  This is the team that fired this bullet, ie the team which will *not* collide with it. Bullets will always collide with team `"none"`, and never collide with team `"all"`.

##### Static Members
 - `type = "bullet_base"`
 - `default_speed`
  The default initial speed of all projectiles instantiated from this class, in pixels per second.
 - `default_damage = 100`
  The default initial damage of all projectiles instantiated from this class.

#### Rocket class

Accessible through `game.entity.rocket`

Rockets are a subtype of `bullet` which have a different sprite and more complex behavior.

In addition to the methods and members of `game.entity.bullet`, the rocket class provides the following:
##### Methods

##### Instance Members
 - `fallspeed`

##### Static Members
 - `initial_fall_speed = 400`
  The initial speed at which the rocket is dropped from its hardpoint/bay/origin. This corresponds directly to an initial positive y velocity tracked separately from its normal speed.
 - `vertical_damping = 1024`
  The rate of deceleration from the initial fall speed, in pixels per second per second. Will stop a minimum fall speed of `-100` pixels per second.
 - `initial_speed = -100`
  The rocket is launched slightly backward for visual effect.
 - `acceleration = 2048`
  Once launched, the rocket's speed will increase by this amount every second.
 - `default_damage = 200`
  See parent class
 - `type = "bullet_rocket`
  See entity class

### Spawner module

Accessible through `game.spawner`

The spawner object is used to handle repeated enemy spawning with minimal user intervention. The object as a whole is the `spawner`, and any tracked instance are called a `spawn`. Each `spawn` handles the spawning of one type of entity.

#### Functions
 - `addBasic(entityType, minDelay, maxDelay)`
  Creates a `spawn` object for the provided entity type and returns a reference to it. The entity will immediately begin to spawn with random delays between `minDelay` and `maxDelay` in seconds.
 - `update(dt)`
  Propagates an update tick to the spawner module and allows spawns to update appropriately. Should not be called by the user, as this is already handled by corelib directly.
#### Classes
 - `timer`
  A generalized class for repeating a function at irregular intervals between a minimum and maximum delay.

  Constructor:
  `timer(minDelay, maxDelay, function)`

  Methods:
   - `update(dt)`
    Updates this particular timer and calls its function as many times as is appropriate.
    The function is called with a single argument, `subdt`, which is the time since the beginning of that frame at which it should have been called based on the delay. This can be used to account for long frame times.
   - `register()`
    Registers this timer as a `spawn` if it is not already registered. Otherwise, does nothing.
   - `remove()`
    Removes the timer from the spawner object's registry.
 - `spawnTimer`
  A simpler class designed specifically to spawn enemies at regular intervals.
  Includes a default spawn function which spawns this timer's assigned entity type at a random position above the screen.

  It inherits all methods from the more advanced `timer` class.

  Constructor:
  `spawnTimer(entityType, minDelay, maxDelay, spawnFunction = {internal default})`
  The entity type should be the actual class which the spawner will instantiate. It should inherit from the base `enemy` class and accept the same parameters as the default constructor, with defaults past the first 3 arguments.

### Graphics module

Accessible through `game.graphics`

The graphics module provides some basic utilities as an abstraction for Pygame's rendering. Performance of these utilities is not a high priority compared to simple ease of use.

#### Functions
 - `check()`
  Checks that the current display surface used by the module is valid. If so, returns the display surface. Otherwise, returns `None`.
 - `blit(image, x, y)`
  Wrapper for Pygame's blit function. Renders the provided image to the screen at the provided coordinates with no transformation.
 - `blit_centered(image, x, y)`
  Wrapper for pygame's blit function. Renders the provided image to the screen with the center at the provided coordinates with no transformation.
 - `draw(image, x, y, scale = 1, angle = 0)`
  Draws the provided image centered at the provided coordinates with a rotation and zoom applied as appropriate. Returns the transformed image instance when complete. If scale and angle are left as default, operates exactly the same as `blit_centered(image, x, y)`.

#### Particle submodule

Accessible through `game.graphics.particle`

The particle submodule will provide an efficient way to spawn large numbers of visual elements which follow simple rules over a short lifespan. It is currently unsupported and incomplete, however.

### Menu module

This feature is currently in development. It will allow students to add simple actuator buttons and scoring.
