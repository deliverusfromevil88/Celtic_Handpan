import os
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.animation import Animation

ALIGNMENT_MODE = False
Window.clearcolor = (0.15, 0.15, 0.15, 1)

HERE = os.path.dirname(__file__)
ASSETS = os.path.join(HERE, "assets")
def asset(path): return os.path.join(ASSETS, path)

class HandpanApp(App):
    def build(self):
        layout = FloatLayout()

        background = Image(
            source=asset("handpan_layout.jpg"),
            allow_stretch=True, keep_ratio=True
        )
        layout.add_widget(background)

        self.sounds = [SoundLoader.load(asset(f"note_{i}.wav")) for i in range(9)]

        self.note_positions = [
            {'center_x': 0.5,   'center_y': 0.5},  # 0 Ding
            {'center_x': 0.625, 'center_y': 0.29}, # 1 A3
            {'center_x': 0.37,  'center_y': 0.29}, # 2 Bb3
            {'center_x': 0.81,  'center_y': 0.42}, # 3 C4
            {'center_x': 0.19,  'center_y': 0.42}, # 4 D4
            {'center_x': 0.75,  'center_y': 0.63}, # 5 E4
            {'center_x': 0.16,  'center_y': 0.59}, # 6 F4
            {'center_x': 0.53,  'center_y': 0.71}, # 7 G4
            {'center_x': 0.32,  'center_y': 0.71}, # 8 A4
        ]

        for i, pos in enumerate(self.note_positions):
            note_size = (0.26, 0.26)

            highlight = Image(
                source=asset("highlight.png"),
                pos_hint=pos, size_hint=note_size, opacity=0
            )
            layout.add_widget(highlight)

            button_color = (1, 0, 1, 0.5) if ALIGNMENT_MODE else (0, 0, 0, 0)
            btn = Button(
                text=str(i) if ALIGNMENT_MODE else "",
                font_size='30sp',
                pos_hint=pos,
                size_hint=note_size,
                background_color=button_color
            )
            btn.sound = self.sounds[i]
            btn.highlight = highlight
            btn.bind(on_press=self.play_sound)
            layout.add_widget(btn)

        return layout

    def play_sound(self, button_instance):
        snd = button_instance.sound
        if snd:
            snd.stop()
            snd.play()
        Animation(opacity=0, duration=0).start(button_instance.highlight)

if __name__ == "__main__":
    HandpanApp().run()
