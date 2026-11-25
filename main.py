from random import randint
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.label import Label


class BallDodgeGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.game_over = False
        self.ball_radius = dp(18)
        self.ball_y = dp(65)
        self.ball_x = 0
        self.ball_speed = dp(330)
        self.obs_width = dp(58)
        self.obs_height = dp(20)
        self.obs_y = 0
        self.obs_x = 0
        self.obs_speed = dp(280)
        self.move_direction = 0
        self._touch_uid = None

        self.score_label = Label(
            text="Score: 0", font_size="20sp",
            color=(0, 0, 0, 1), size_hint=(None, None),
            halign="left", valign="middle"
        )
        self.message_label = Label(
            text="", font_size="20sp",
            color=(0.86, 0.08, 0.18, 1),
            size_hint=(None, None), halign="center",
            valign="middle"
        )
        self.add_widget(self.score_label)
        self.add_widget(self.message_label)
        self.bind(size=self._layout, pos=self._layout)
        self.reset_game()
        Clock.schedule_interval(self.update, 1 / 60)

    def _layout(self, *_):
        self.score_label.pos = (dp(12), self.height - dp(42))
        self.score_label.size = (self.width - dp(24), dp(32))
        self.score_label.text_size = self.score_label.size
        self.message_label.size = (self.width - dp(30), dp(100))
        self.message_label.center = self.center
        self.message_label.text_size = self.message_label.size
        self.ball_y = dp(65)

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.obs_speed = dp(280)
        self.ball_x = self.width / 2 if self.width else dp(180)
        self.obs_y = self.height + self.obs_height
        self.obs_x = randint(0, max(0, int(self.width - self.obs_width))) if self.width else 0
        self.message_label.text = ""
        self.score_label.text = "Score: 0"

    def on_size(self, *_):
        self.ball_x = min(max(self.ball_x, self.ball_radius), max(self.ball_radius, self.width - self.ball_radius))
        self.obs_x = min(self.obs_x, max(0, self.width - self.obs_width))

    def on_touch_down(self, touch):
        if self.game_over:
            self.reset_game()
            return True
        self._touch_uid = touch.uid
        self._set_direction(touch.x)
        return True

    def on_touch_move(self, touch):
        if self._touch_uid == touch.uid and not self.game_over:
            self._set_direction(touch.x)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self._touch_uid == touch.uid:
            self._touch_uid = None
            self.move_direction = 0
            return True
        return super().on_touch_up(touch)

    def _set_direction(self, x):
        self.move_direction = -1 if x < self.center_x else 1

    def update(self, dt):
        if self.width <= 0 or self.height <= 0:
            return
        if not self.game_over:
            self.ball_x += self.move_direction * self.ball_speed * dt
            self.ball_x = max(self.ball_radius, min(self.width - self.ball_radius, self.ball_x))
            self.obs_y -= self.obs_speed * dt

            if self.obs_y + self.obs_height < 0:
                self.obs_y = self.height
                self.obs_x = randint(0, max(0, int(self.width - self.obs_width)))
                self.score += 1
                self.obs_speed += dp(12)
                self.score_label.text = f"Score: {self.score}"

            ball_left = self.ball_x - self.ball_radius
            ball_right = self.ball_x + self.ball_radius
            ball_bottom = self.ball_y - self.ball_radius
            ball_top = self.ball_y + self.ball_radius
            hit = (
                ball_right > self.obs_x and
                ball_left < self.obs_x + self.obs_width and
                ball_top > self.obs_y and
                ball_bottom < self.obs_y + self.obs_height
            )
            if hit:
                self.game_over = True
                self.message_label.text = (
                    f"GAME OVER\nFinal score: {self.score}\nTap anywhere to play again"
                )

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

            if not self.game_over:
                Color(30 / 255, 144 / 255, 1, 1)
                Ellipse(
                    pos=(self.ball_x - self.ball_radius, self.ball_y - self.ball_radius),
                    size=(self.ball_radius * 2, self.ball_radius * 2)
                )
                Color(220 / 255, 20 / 255, 60 / 255, 1)
                Rectangle(pos=(self.obs_x, self.obs_y), size=(self.obs_width, self.obs_height))


class BallDodgeApp(App):
    def build(self):
        self.title = "Ball Dodge Game"
        return BallDodgeGame()


if __name__ == "__main__":
    BallDodgeApp().run()
