import os
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.animation import Animation
import pygame

### <<< THE ALIGNMENT TOOL >>> ###
# Set this to True to see the buttons. Set to False for normal use.
ALIGNMENT_MODE = False
# ---------------------------------

# --- Setup ---
Window.clearcolor = (0.15, 0.15, 0.15, 1)
# Update this path to your 432 Hz + reverb sounds
APP_PATH = '/storage/emulated/0/Download/Celtic_Handpan_432_reverb'

# --- Audio Setup ---
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.set_num_channels(16)
sounds = []
for i in range(9):
    sound_file = os.path.join(APP_PATH, f'note_{i}.wav')
    if os.path.exists(sound_file):
        sounds.append(pygame.mixer.Sound(sound_file))
    else:
        raise FileNotFoundError(f"Audio file not found: {sound_file}")

# --- Kivy Application ---
class HandpanApp(App):
    def build(self):
        layout = FloatLayout()

        # Background image
        background = Image(
            source=os.path.join(APP_PATH, '../Celtic_Handpan/handpan_layout.jpg'),
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(background)

        # Note positions (center_x, center_y)
        self.note_positions = [
            {'center_x': 0.5,   'center_y': 0.5},   # Note 0 (Ding)
            {'center_x': 0.625, 'center_y': 0.29},  # Note 1 (A3)
            {'center_x': 0.37,  'center_y': 0.29},  # Note 2 (Bb3)
            {'center_x': 0.81,  'center_y': 0.42},  # Note 3 (C4)
            {'center_x': 0.19,  'center_y': 0.42},  # Note 4 (D4)
            {'center_x': 0.75,  'center_y': 0.63},  # Note 5 (E4)
            {'center_x': 0.16,  'center_y': 0.59},  # Note 6 (F4)
            {'center_x': 0.53,  'center_y': 0.71},  # Note 7 (G4)
            {'center_x': 0.32,  'center_y': 0.71},  # Note 8 (A4)
        ]

        # Create notes
        for i, pos in enumerate(self.note_positions):
            note_size = (0.26, 0.26) if i == 0 else (0.26, 0.26)

            # Highlight effect when note is played
            highlight = Image(
                source=os.path.join(APP_PATH, '../Celtic_Handpan/highlight.png'),
                pos_hint=pos,
                size_hint=note_size,
                opacity=0
            )
            layout.add_widget(highlight)

            # Button appearance in alignment mode
            button_color = (1, 0, 1, 0.5) if ALIGNMENT_MODE else (0, 0, 0, 0)
            btn_text = str(i) if ALIGNMENT_MODE else ""

            btn = Button(
                text=btn_text,
                font_size='30sp',
                pos_hint=pos,
                size_hint=note_size,
                background_color=button_color,
            )
            btn.sound = sounds[i]
            btn.highlight = highlight

            # Bind press event with touch (to access pressure)
            btn.bind(on_press=self.play_sound)

            layout.add_widget(btn)

        return layout

    def play_sound(self, button_instance, touch):
        """
        Play sound with volume based on touch pressure.
        Falls back to full volume if pressure is not available.
        """
        # Get pressure if available (0.0 to 1.0+), else default to medium
        raw_pressure = getattr(touch, 'pressure', 1.0)
        # Clamp and scale pressure for natural response
        volume = 0.1 + 0.9 * min(max(raw_pressure, 0.0), 1.0)

        # Stop any previous playback of this sound
        button_instance.sound.stop()
        # Set dynamic volume
        button_instance.sound.set_volume(volume)
        # Play the note
        button_instance.sound.play()

        # Visual feedback: pulse the highlight
        highlight = button_instance.highlight
        anim = (
            Animation(opacity=0.7, duration=0.1) +
            Animation(opacity=0, duration=0.8, t='out_quad')
        )
        anim.start(highlight)


if __name__ == '__main__':
    HandpanApp().run()
