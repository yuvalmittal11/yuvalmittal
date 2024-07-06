import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
import random

kivy.require('2.1.0')

class Bird(Image):
    def __init__(self, **kwargs):
        super(Bird, self).__init__(**kwargs)
        self.source = 'bird.png'
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.pos = (100, Window.height // 2)
        self.velocity_y = 0

    def move(self):
        self.y += self.velocity_y
        self.velocity_y -= 0.5

    def jump(self):
        self.velocity_y = 10


class Pipe(Widget):
    def __init__(self, **kwargs):
        super(Pipe, self).__init__(**kwargs)
        with self.canvas:
            self.top_pipe = Rectangle(source='pipe.png', size=(100, random.randint(300, 500)), pos=(Window.width, 0))
            self.bottom_pipe = Rectangle(source='pipe.png', size=(100, Window.height), pos=(Window.width, Window.height))

    def move(self):
        self.top_pipe.pos = (self.top_pipe.pos[0] - 5, self.top_pipe.pos[1])
        self.bottom_pipe.pos = (self.bottom_pipe.pos[0] - 5, self.bottom_pipe.pos[1])

    def check_collision(self, bird):
        if (self.top_pipe.pos[0] < bird.x + bird.width and self.top_pipe.pos[0] + self.top_pipe.size[0] > bird.x and
            self.top_pipe.pos[1] < bird.y + bird.height and self.top_pipe.pos[1] + self.top_pipe.size[1] > bird.y):
            return True
        if (self.bottom_pipe.pos[0] < bird.x + bird.width and self.bottom_pipe.pos[0] + self.bottom_pipe.size[0] > bird.x and
            self.bottom_pipe.pos[1] < bird.y + bird.height and self.bottom_pipe.pos[1] + self.bottom_pipe.size[1] > bird.y):
            return True
        return False


class FlappyBirdGame(Widget):
    def __init__(self, **kwargs):
        super(FlappyBirdGame, self).__init__(**kwargs)
        self.bird = Bird()
        self.add_widget(self.bird)
        self.pipes = []
        self.pipe_interval = 0
        self.score = 0
        self.game_over = False

        self.jump_sound = SoundLoader.load('jump.wav')
        self.hit_sound = SoundLoader.load('hit.wav')

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_touch_down(self, touch):
        if not self.game_over:
            self.bird.jump()
            if self.jump_sound:
                self.jump_sound.play()

    def update(self, dt):
        if not self.game_over:
            self.bird.move()

            self.pipe_interval += 1
            if self.pipe_interval >= 90:
                new_pipe = Pipe()
                self.pipes.append(new_pipe)
                self.add_widget(new_pipe)
                self.pipe_interval = 0

            for pipe in self.pipes:
                pipe.move()
                if pipe.check_collision(self.bird):
                    self.game_over = True
                    if self.hit_sound:
                        self.hit_sound.play()
                    break

                if pipe.top_pipe.pos[0] < -100:
                    self.remove_widget(pipe)
                    self.pipes.remove(pipe)
                    self.score += 1

            if self.bird.y < 0 or self.bird.y > Window.height:
                self.game_over = True
                if self.hit_sound:
                    self.hit_sound.play()


class FlappyBirdApp(App):
    def build(self):
        return FlappyBirdGame()


if __name__ == '__main__':
    FlappyBirdApp().run()
