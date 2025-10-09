from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from random import uniform
import math

# =========================
# === SETTINGS ============
# =========================
MAP_SIZE = 100
GROUND_TEXTURE = 'grass'
SKY_TYPE = 'default'

PLAYER_GRAVITY = 0.5
PLAYER_JUMP_HEIGHT = 2
PLAYER_SPEED = 5
SPRINT_MULTIPLIER = 1.8
PLAYER_START_POS = (15, 11, 0)

SLIDE_FRICTION = 6
SLIDE_START_VELOCITY = 40
SLIDE_COOLDOWN = 2.0
SLIDE_CAMERA_Y = 0.5
NORMAL_CAMERA_Y = 1.5
GRAVITY_FORCE = 20.0

DASH_DISTANCE = 15
DASH_COOLDOWN = 1.0

OBSTACLE_COUNT = 20
OBSTACLE_COLOR = color.orange
OBSTACLE_TEXTURE = 'brick'

TIMER_DURATION = 60  # seconds for timed mode

# === Gun Physics Settings ===
GUN_GRAVITY = 12     # how fast dropped guns fall
GUN_POP_FORCE = 2    # how strongly the dropped gun pops upward
GUN_DROP_COOLDOWN = 2.0  # seconds
gun_drop_timer = 0        # initialize to 0

# === Player Physics Settings ===
ACCELERATION = 20        # how fast you speed up
FRICTION = 15            # how fast you slow down when no input
MAX_SPEED = 7            # cap on speed

# movement_velocity is the movement state we integrate each frame
movement_velocity = Vec3(0, 0, 0)

# =========================
# === INITIALIZATION ======
# =========================
app = Ursina()

# === Main Menu ===
menu_background = Entity(
    model='quad',
    scale=(1.5, 1),
    color=color.dark_gray,
    z=1,
    texture_filtering='linear'
)

title = Text(
    "Main Menu",
    scale=2,
    origin=(0, 0),
    position=(0, 0.3),
    background=True
)

casual_button = Button(
    text='Casual Play',
    scale=(0.3, 0.1),
    position=(0, 0.1)
)
timed_button = Button(
    text='Timed Mode',
    scale=(0.3, 0.1),
    position=(0, -0.05)
)

def on_hover(button):
    button.scale = (0.32, 0.11)
    button.color = color.yellow

def on_leave(button):
    button.scale = (0.3, 0.1)
    button.color = color.green

casual_button.on_mouse_enter = lambda: on_hover(casual_button)
casual_button.on_mouse_exit = lambda: on_leave(casual_button)
timed_button.on_mouse_enter = lambda: on_hover(timed_button)
timed_button.on_mouse_exit = lambda: on_leave(timed_button)

# === Map Setup ===
model_entity = Entity(
    model='./assets/tutorial_map.obj',
    texture='./assets/texture_01.png',
    scale=1,
    collider='mesh',
    position=(0, 0, 0),
    texture_scale=(20, 20),
    shader=lit_with_shadows_shader,
    double_sided=True
)

DirectionalLight(color=color.rgb(50, 50, 50), shadows=True)
AmbientLight(color=color.rgba(50, 50, 50, 0.1))

# === Player Setup ===
player = FirstPersonController(position=PLAYER_START_POS)
player.gravity = PLAYER_GRAVITY
player.jump_height = PLAYER_JUMP_HEIGHT
player.speed = PLAYER_SPEED  # still used for some features, but movement is controlled by movement_velocity now

player_model = Entity(
    parent=player,
    model='cube',
    color=color.orange,
    scale=(1, 2, 1),
    position=(0, -1, 0),
    collider=None
)

# === Gun ===
gun_model = Entity(
    model='./assets/gun3.obj',
    position=(0, 1.3, 2),
    scale=0.1,
    collider=None,
    shader=lit_with_shadows_shader,
    double_sided=True,
    parent=player
)
gun_model.texture = './assets/textures/gun3_texture.png'

barrel = Entity(
    parent=gun_model,
    position=(0, 0.1, 2.2),
    scale=0.02,
    visible=False
)
gun_equipped = True  # starts equipped

# === Target System ===
target_spheres = []

def spawn_targets(count=10):
    for _ in range(count):
        y = uniform(11, 20)
        z = uniform(-10, 10)
        sphere = Entity(
            model='sphere',
            color=color.red,
            scale=1,
            position=(62, y, z),
            collider='box',
            name='target'
        )
        target_spheres.append(sphere)

def respawn_targets():
    if len(target_spheres) < 10:
        spawn_targets(count=10 - len(target_spheres))

# === HUD for Timed Mode ===
timer_text = Text(
    text="Time: 0",
    position=window.top_left + Vec2(0.05, -0.05),
    origin=(0, 0),
    scale=1.2,
    background=True,
    enabled=False
)
score_text = Text(
    text="Score: 0",
    position=window.top + Vec2(0, -0.05),
    origin=(0, 0),
    scale=1.2,
    background=True,
    enabled=False
)
accuracy_text = Text(
    text="Accuracy: 0%",
    position=window.top_right + Vec2(-0.25, -0.05),
    origin=(0, 0),
    scale=1.2,
    background=True,
    enabled=False
)

# === Game State ===
is_sliding = False
slide_velocity = 0
slide_direction = Vec3(0, 0, 0)
momentum = Vec3(0, 0, 0)
is_airborne = False
slide_timer = 0.0
dash_timer = 0.0
is_sprinting = False
previous_position = player.position

# Timed mode state
is_timed_mode = False
time_remaining = TIMER_DURATION
score = 0
shots_fired = 0
hits = 0
results_screen = None

# === Game Visibility Control ===
def hide_game_elements():
    model_entity.enabled = False
    player.enabled = False
    gun_model.enabled = False
    for target in target_spheres:
        target.enabled = False

def start_casual_play():
    menu_background.enabled = False
    title.enabled = False
    casual_button.enabled = False
    timed_button.enabled = False
    model_entity.enabled = True
    player.enabled = True
    gun_model.enabled = True
    spawn_targets()
    camera.fov = 90
    mouse.locked = True

def start_timed_mode():
    global is_timed_mode, time_remaining, score, results_screen, shots_fired, hits
    # Hide menu
    menu_background.enabled = False
    title.enabled = False
    casual_button.enabled = False
    timed_button.enabled = False

    # Show game
    model_entity.enabled = True
    player.enabled = True
    gun_model.enabled = True
    timer_text.enabled = True
    score_text.enabled = True
    accuracy_text.enabled = True

    # Setup state
    spawn_targets()
    camera.fov = 90
    mouse.locked = True
    is_timed_mode = True
    time_remaining = TIMER_DURATION
    score = 0
    shots_fired = 0
    hits = 0
    score_text.text = f"Score: {score}"
    accuracy_text.text = "Accuracy: 0%"

    if results_screen:
        destroy(results_screen)

casual_button.on_click = start_casual_play
timed_button.on_click = start_timed_mode
hide_game_elements()

# === Shooting ===
def shoot():
    global score, shots_fired, hits
    shots_fired += 1

    hit_info = raycast(
        origin=player.world_position + Vec3(0, 1.74, 0),
        direction=camera.forward,
        distance=9999,
        ignore=[player]
    )
    if hit_info.hit and hit_info.entity and hit_info.entity.name == 'target':
        if hit_info.entity in target_spheres:
            target_spheres.remove(hit_info.entity)
        destroy(hit_info.entity)

        if is_timed_mode:
            score += 1
            hits += 1
            score_text.text = f"Score: {score}"

    # Update accuracy
    if is_timed_mode:
        accuracy = (hits / shots_fired * 100) if shots_fired > 0 else 0
        accuracy_text.text = f"Accuracy: {accuracy:.1f}%"

# === Drop + Respawn Gun ===
# Note: dropped gun takes measured_player_velocity (horizontal) so it inherits player's movement
measured_player_prev_pos = player.position
measured_player_velocity = Vec3(0,0,0)

def drop_and_respawn_gun():
    global gun_model, movement_velocity, gun_equipped, measured_player_velocity
    gun_equipped = False

    # Drop the current gun
    dropped_gun = Entity(
        model=gun_model.model,
        texture=gun_model.texture,
        position=gun_model.world_position,
        rotation=gun_model.world_rotation,
        scale=gun_model.scale,
        collider='box',
        shader=lit_with_shadows_shader,
        double_sided=True
    )

    # Initial velocity: pop up + some of player's horizontal velocity (measured at drop)
    horiz = Vec3(measured_player_velocity.x, 0, measured_player_velocity.z)
    dropped_gun.velocity = horiz * 0.9
    dropped_gun.velocity.y = GUN_POP_FORCE

    # Gravity + movement for dropped gun
    def dropped_update(e=dropped_gun):
        if e.y > -10:
            e.position += e.velocity * time.dt
            e.velocity.y -= GUN_GRAVITY * time.dt
        else:
            e.y = -10
    dropped_gun.update = dropped_update

    # Spawn replacement gun after 1 sec
    def spawn_new_gun():
        global gun_model, gun_equipped
        gun_model = Entity(
            model='./assets/gun3.obj',
            position=(0, 1.3, 2),
            scale=0.1,
            collider=None,
            shader=lit_with_shadows_shader,
            double_sided=True,
            parent=player
        )
        gun_model.texture = './assets/textures/gun3_texture.png'
        barrel.parent = gun_model
        barrel.position = (0, 0.1, 2.2)

        gun_equipped = True  # now player has gun again

    invoke(spawn_new_gun, delay=1)

# === End screen ===
def end_timed_mode():
    global is_timed_mode, results_screen
    is_timed_mode = False

    # Hide HUD + game elements
    timer_text.enabled = False
    score_text.enabled = False
    accuracy_text.enabled = False
    player.enabled = False
    gun_model.enabled = False
    for target in target_spheres:
        destroy(target)
    target_spheres.clear()

    # Unlock mouse
    mouse.locked = False

    # Calculate accuracy
    accuracy = (hits / shots_fired * 100) if shots_fired > 0 else 0

    # Results screen (centered)
    results_screen = Text(
        f"⏱ Time’s up!\nScore: {score}\nAccuracy: {accuracy:.1f}%\n\nPress ENTER to return to Menu",
        origin=(0, 0),
        scale=2,
        background=True,
        color=color.yellow
    )

def return_to_menu():
    global results_screen
    if results_screen:
        destroy(results_screen)
        results_screen = None

    # Show menu again
    menu_background.enabled = True
    title.enabled = True
    casual_button.enabled = True
    timed_button.enabled = True
    player.position = PLAYER_START_POS
    player.rotation = Vec3(0, 0, 0)

# === Input Handling ===
def input(key):
    global gun_drop_timer

    if not player.enabled and not is_timed_mode:
        if key == 'enter':
            return_to_menu()
    if not player.enabled:
        return
    if key == 'left mouse down':
        if gun_equipped:   # only shoot if gun is in hand
            shoot()
    if key == 'r' and gun_drop_timer <= 0:
        drop_and_respawn_gun()
        gun_drop_timer = GUN_DROP_COOLDOWN

# === Update Loop / Momentum Movement Injection ===
previous_player_pos = player.position  # used to compute measured velocity for dropped gun
# movement_velocity is defined at top (movement state)

def update():
    if not player.enabled and not is_timed_mode:
        return

    global is_sliding, slide_velocity, slide_direction, momentum, is_airborne
    global slide_timer, dash_timer, is_sprinting, previous_position
    global time_remaining
    global gun_drop_timer
    global previous_player_pos, measured_player_prev_pos, measured_player_velocity, movement_velocity

    # --- measure player's instantaneous velocity (used for dropped gun inertia) ---
    # measured_player_velocity = (current_pos - previous_pos) / dt
    measured_player_velocity = (player.position - measured_player_prev_pos) / time.dt
    measured_player_prev_pos = player.position

    # reduce gun drop cooldown
    gun_drop_timer = max(gun_drop_timer - time.dt, 0)

    # Gun follows camera pitch only (if gun exists)
    if gun_model:
        gun_offset = Vec3(0.3, -0.2, 1.5)
        gun_model.world_position = (
            camera.world_position +
            camera.forward * gun_offset.z +
            camera.right * gun_offset.x +
            camera.up * gun_offset.y
        )
        target_rot = Vec3(player.camera_pivot.rotation_x, 0, 0)
        gun_model.rotation = lerp(gun_model.rotation, target_rot, time.dt * 10)

    slide_timer = max(slide_timer - time.dt, 0)
    dash_timer = max(dash_timer - time.dt, 0)

    # Sprinting toggles (affects target max speed)
    if held_keys['shift'] and not is_sliding:
        target_max_speed = MAX_SPEED * SPRINT_MULTIPLIER
        is_sprinting = True
    else:
        target_max_speed = MAX_SPEED
        is_sprinting = False

    # Slide trigger (unchanged)
    if held_keys['control'] and not is_sliding and slide_timer <= 0 and is_sprinting:
        is_sliding = True
        slide_velocity = SLIDE_START_VELOCITY
        slide_direction = player.forward.normalized()
        slide_timer = SLIDE_COOLDOWN
        # zero horizontal movement while sliding
        movement_velocity.x = 0
        movement_velocity.z = 0

    respawn_targets()

    # Sliding logic stays as-is (slide overrides normal movement)
    if is_sliding:
        hit_info = raycast(player.position, Vec3(0, -1, 0), distance=2, ignore=[player])
        if hit_info.hit:
            slope_normal = hit_info.normal
            downhill = Vec3(-slope_normal.x, 0, -slope_normal.z).normalized()
            slide_direction = lerp(slide_direction, downhill, time.dt * 2)
            slide_velocity += GRAVITY_FORCE * (1 - hit_info.normal.y) * time.dt

        slide_step = slide_direction * slide_velocity * time.dt
        hit = raycast(player.position, slide_direction, distance=slide_step.length() + 0.5, ignore=[player])
        if not hit.hit:
            player.position += slide_step
        else:
            is_sliding = False
            slide_velocity = 0

        player.camera_pivot.y = lerp(player.camera_pivot.y, SLIDE_CAMERA_Y, time.dt * 8)
        slide_velocity = max(slide_velocity - SLIDE_FRICTION * time.dt, 0)

        if held_keys['space']:
            is_sliding = False
            slide_velocity = 0
    else:
        player.camera_pivot.y = lerp(player.camera_pivot.y, NORMAL_CAMERA_Y, time.dt * 6)

        # --- Momentum-based ground movement (applies only when not sliding) ---
        # Input direction from WASD / arrow keys
        input_dir = Vec3(
            held_keys['d'] - held_keys['a'],  # right-left
            0,
            held_keys['w'] - held_keys['s']   # forward-back
        )
        if input_dir.length() > 0:
            input_dir = input_dir.normalized()

        # Build world-space move direction ignoring vertical component
        if input_dir.length() > 0:
            move_dir_world = (camera.forward * input_dir.z + camera.right * input_dir.x)
            move_dir_world.y = 0
            if move_dir_world.length() > 0:
                move_dir_world = move_dir_world.normalized()
        else:
            move_dir_world = Vec3(0, 0, 0)

        # Apply acceleration when input provided
        if move_dir_world.length() > 0:
            movement_velocity += move_dir_world * ACCELERATION * time.dt
        else:
            # Apply friction to horizontal velocity
            horiz = Vec3(movement_velocity.x, 0, movement_velocity.z)
            if horiz.length() > 0:
                friction_force = horiz.normalized() * FRICTION * time.dt
                if friction_force.length() >= horiz.length():
                    movement_velocity.x = 0
                    movement_velocity.z = 0
                else:
                    movement_velocity.x -= friction_force.x
                    movement_velocity.z -= friction_force.z

        # Cap horizontal speed (respect sprint target)
        horiz_speed = math.sqrt(movement_velocity.x**2 + movement_velocity.z**2)
        if horiz_speed > target_max_speed:
            scale = target_max_speed / horiz_speed
            movement_velocity.x *= scale
            movement_velocity.z *= scale

        # --- Jumping: compute jump impulse using physics formula ---
        # gravity acceleration used for vertical integration
        gravity_accel = 9.8 * PLAYER_GRAVITY
        if player.grounded and held_keys['space']:
            # required initial velocity to reach desired jump height: v = sqrt(2 * g * h)
            jump_vel = math.sqrt(2 * gravity_accel * PLAYER_JUMP_HEIGHT)
            movement_velocity.y = jump_vel
            is_airborne = True
        # If airborne, gravity will be applied below

        # Apply gravity to vertical velocity
        movement_velocity.y -= gravity_accel * time.dt

        # Move player by integrated velocity
        player.position += movement_velocity * time.dt

        # Ground check: if grounded, reset vertical velocity
        if player.grounded:
            movement_velocity.y = 0
            is_airborne = False

    # Dash (keeps original behavior)
    if held_keys['q'] and dash_timer <= 0:
        dash_vector = player.forward.normalized() * DASH_DISTANCE
        player.animate_position(player.position + dash_vector, duration=0.2, curve=curve.linear)
        dash_timer = DASH_COOLDOWN

    # Timed mode countdown
    if is_timed_mode:
        time_remaining -= time.dt
        timer_text.text = f"Time: {int(time_remaining)}"
        if time_remaining <= 0:
            end_timed_mode()

    # Exit
    if held_keys['escape']:
        application.quit()

# =========================
# === RUN GAME ============
# =========================
app.run()
