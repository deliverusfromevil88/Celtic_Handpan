from ursina import *
import math

# --- App Initialization ---
# We initialize the Ursina app. 'borderless=False' is good for VNC.
app = Ursina(borderless=False)

# --- Asset Loading ---

# Load the audio files into a list.
# The central note (Ding) will be note_0, and the others will follow.
note_sounds = [Audio(f'Celtic_Handpan/note_{i}.wav', autoplay=False) for i in range(9)]

# --- Scene Setup ---

# Create the main Handpan entity from the .obj file
handpan = Entity(
    model='handpan.obj',
    texture='handpan_texture.jpg',
    scale=15,  # Adjust scale to fit the screen well
    rotation_y=90, # Adjust rotation if it's not facing correctly
    collider=None # We will use separate colliders for notes
)

# Set up the camera. EditorCamera allows you to move around with the mouse.
# Right-click and drag to orbit, scroll wheel to zoom.
EditorCamera()
# You can use a fixed camera instead if you prefer:
# camera.position = (0, 20, 0)
# camera.rotation_x = 90

# Set up a light for better visuals
pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True)

# --- Interactivity: Creating Invisible Note Buttons ---

# This is the clever part. We create invisible entities (Buttons) on top
# of each note area. When clicked, they will play the sound.

# We will store our note buttons in a list
note_buttons = []

# Define positions for the notes. You will need to TWEAK these values
# to perfectly match your 3D model!
# Format: (x, y, z) position
# The handpan is at (0,0,0). Y is the up/down axis.
note_positions = [
    # Note 0: Central Ding
    (0, 0.6, 0),
    # The next 8 notes are placed in a circle. We use math to calculate their positions.
    # We define the radius of the circle of notes.
]

radius = 4.5 # Tweak this to match your model
angle_step = 360 / 8 # 8 notes in the circle
for i in range(8):
    angle = math.radians(i * angle_step)
    x = radius * math.cos(angle)
    z = radius * math.sin(angle)
    # The 'y' value might need slight adjustment if notes are at different heights
    note_positions.append((x, 0.5, z))


# Create a button for each position
for i, pos in enumerate(note_positions):
    # The 'note_id' stores which sound this button corresponds to.
    # We use a lambda function to capture the correct 'i' value for the click handler.
    btn = Button(
        parent=handpan,  # Parented to the handpan so they move together
        position=pos,
        model='sphere',  # A simple shape for the collider
        scale=2.0,      # Tweak scale to match the note size
        color=color.clear, # Make the button invisible
        highlight_color=color.rgba(255, 255, 255, 80), # Slight highlight on hover
        on_click=lambda i=i: play_note(i) # Call play_note function on click
    )
    note_buttons.append(btn)


# --- Functions ---

def play_note(note_id):
    """Plays the sound corresponding to the note_id and gives visual feedback."""
    if 0 <= note_id < len(note_sounds):
        print(f"Playing note {note_id}")
        note_sounds[note_id].play()
        
        # Optional: Add some visual feedback
        button = note_buttons[note_id]
        button.animate_color(color.white33, duration=0.1)
        button.animate_color(color.clear, duration=0.3, delay=0.1)

# --- Start the App ---
app.run()
