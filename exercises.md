
IDE Basics:

  0. Class expectations
  1. Log in to Replit
  2. Fork the template
  3. Open the game
  4. Launch the game
  5. Access the script file (game.py)
      - Explain that `import core as game` is just required, ignore it
  6. Modify one (1) player stat

      `player.speed = 999`
  7. Other player variables to play with:
      - health
      - scale
      - speed
      - mainfire/altfire
      - variant

Variables:

  0. Login & troubleshooting
  1. What is a variable?
  2. Print a value
  3. Set a variable
  4. Print a variable
  
  Flexible segment

  - Player shortcut

      `player = game.player`
  - Player secret activity

      `player.try_secret(player.secret)`
      or `player.secret_digit_1 = player.secret_1` (4 digits)
  - Player shoots itself down (currently unimplemented)

      `player.speed = game.entity.bullet.default_speed`
  - Negative values do fun stuff

      `player.ammo_base = -1` (infinite ammunition)
      `player.ammo_rocket = -1`

Variables (cont):

  0. Login & troubleshooting
  1. Variable review
  2. Variables in expressions

      `player.speed = -player.speed` (moves backwards)
  3. Booleans

      `game.base_spawn.enabled = False` (disable enemy spawns)
  4. Strings?
        - Name print exercise
        - "bonono" exercise
            ```Python
            var = "banana"
            print(var) # "banana"
            vowel = 'o'
            var[1] = vowel
            var[3] = vowel
            var[-1] = vowel
            print(var) # "bonono"
            var[-2] = 'b'
            print(var) # "bonobo"
            # etc
            ```

Conditionals:

  0. Login should at this point be routine
  1. Boolean variable review
  2. Boolean values from expressions
      - Introduce the concept of boolean expressions before if statements.
        This ground-up approach avoids later confusion.
  3. If statements
      - Physical analog: ![trolley problem](https://pyxis.nymag.com/v1/imgs/08a/3a4/0b0584bf02449513f879837cc95f19e7e0-09-trolley.rhorizontal.w700.jpg)
  3. Exercises
      - Even/odd check
      - Input check (runs before game starts, so we essentially just have a console)
  4. Advanced exercises
      - First function: `def update(dt): pass`; this allows reactions to in-game scenarios, which is simply the best way to teach conditionals.
      - Score check: if score > 100, win()

Conditionals (cont):

  0. Conditionals review, update function review or introduction, nested code syntax review
  1. Password checker
  2. Exercises
      - Time limit: if time > 100s: if score > 100, win(): else: lose()

Logical conjunctions:

  0. Conditional branches review
  1. Introduce an inconvenient stacking if to check multiple conditions at once. Ideas:
      - Cheat code inputs on the console which activate on certain game states (for instance, player health < 10: heal)
      - Autofire when player holds still (check all four keyboard inputs)
  2. Introduce conjunction keywords (and/or) as a solution
  3. Introduce some logical statements
  4. Clarify: conjunctions are a shorthand, they don't behave the same as English. `if a == b or c` doesn't work the way they expect.
  5. Nest conjunctions using parentheses

Lists:

  0. Review of nested code syntax
  1. Introduction to lists
      - The problem to solve: lots of variables with similar jobs
      - Another problem to solve: program needs to do unknown number of tasks
      - Introduce list access syntax
      - Introduce concept of 0-based indexing
  2. Create a list `["name1", "name2", etc]`
  3. Read from list
  4. Introduction to entity list
      - Entities in the game are stored in a list, where the main script checks and updates every single one of them every frame. The list can be read and written to in the game.py script.
  5. Kill entities on the list (this works well enough because entities are autoculled, thereby accessing a new entity every update)
      ```Python
      def update(dt):
        if game.entities.count > 0:
          game.entities[0].alive = False
      ```
  6. 

For loops:

  Note: broken into a separate lesson because this slot was previously just "review," but loops and lists are both very large concepts.

  0. Review lists, entity list
  1. Iterate over entity list as a more elegant approach to operating on any that appear. Note that the previous method only works because each update removes one of the entities, no other function would affect all of them.
      ```Python
      def update(dt):
        for entity in game.entities:
          entity.dosomethingidk()
      ```

Todo:
  - Add helpers for custom entities
  - Add option to create a spawner which copies an instance of an entity
