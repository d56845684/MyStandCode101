"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40  # Height of a brick (in pixels).
BRICK_HEIGHT = 15  # Height of a brick (in pixels).
BRICK_ROWS = 10  # Number of rows of bricks.
BRICK_COLS = 10  # Number of columns of bricks.
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10  # Radius of the ball (in pixels).
PADDLE_WIDTH = 75  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels).
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels).
FRAME_RATE = 1000 / 120  # 120 frames per second
INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball.
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):
        # Create a graphical window, with some extra space
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.window_width, height=self.window_height, title=title)
        # Create a paddle
        self.paddle_offset = paddle_offset
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        # a filled ball and default a ball for pandle in the graphical window
        self.ball_h = ball_radius
        self.basic_ball = GOval(2 * ball_radius, 2 * self.ball_h)
        self.basic_ball.filled = True
        self.bounce_ball = GOval(2 * ball_radius, 2 * ball_radius)
        self.bounce_ball.filled = True
        self.bounce_ball.fill_color = "orange"
        self.strong_doggy = GOval(20, 55)
        self.strong_doggy.filled = True
        self.strong_doggy.color = "red"
        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0
        self.speed()
        # Draw bricks
        self.brick = GRect(brick_width, brick_height)
        self.brick_space = BRICK_SPACING
        self.brick_number = 0
        # self.brick_setting()
        self.brick_number_show = GLabel(f"Brick:{self.brick_number}")
        # self.window.add(self.brick_number_show, x=10, y=self.window.height-5)
        # self.window.add(self.brick, x=400, y=300)     # brick test
        # self.window.add(self.brick_number_show, x=200, y=40)
        # Initialize our mouse listeners
        onmousemoved(self.pandle_tracker)
        onmouseclicked(self.ball_procedure)
        # check當作是否能接受onmouseclicked點擊的開關
        self.check = True
        self.basic_ball_count_state = 0
        self.bounce_ball_count_state = 0
        self.ball_number_count = 0
        self.ball_number_count_show = GLabel(f"Ball number:{self.ball_number_count}")
        # 點擊提示
        self.click_sug = GLabel("Click to start !")
        self.click_suggest = True
        # game當作遊戲開始的開關，起始為False
        self.game = False
        # 遊戲持續進行的開關
        self.game_not_over = True
        # 顯示生命值和win/lost
        self.live = 99
        self.show = GLabel(f"live left: {self.live}")
        self.lose = GLabel("You lose :(")
        self.win = GLabel("You win!")
        # 掉落物
        self.drop_1 = GRect(20, 20)
        self.drop_1_touch = ()
        self.drop_2 = GRect(20, 20)
        self.drop_2.filled = True
        self.drop_3 = GRect(20, 20)
        self.drop_3.filled = True
        self.drop_3.fill_color = "blue"
        self.drop_4 = GRect(20, 20)
        self.drop_4.filled = True
        self.drop_4.fill_color = "blue"
        self.drop_5 = GRect(20, 20)
        self.drop_5.filled = True
        self.drop_5.fill_color = "blue"
        self.drop_vy = 1
        self.drop_record = "1234567890aaaaaaaaaaaaaa"
        # 紀錄球的碰撞位置
        self.ball_touch = ()
        # 使用者介面
        # self. start = GLabel("start!!", x=self.window.width//2, y=self.window.height//2)
        # self.window.add(self.start)
        self.start_touch = True

    # 當點擊時使遊戲開始時執行(game = True)，再加入一顆移動的球。
    def ball_procedure(self, e):
        # self.start_touch = True
        # if self.window.get_object_at(e.x, e.y):
        if self.game_not_over:                                  # 假如可以進行遊戲
            if self.game is not True:
                self.game = True                                   # 點擊後開始遊戲
                if self.game:
                    self.check = False                          # 使onmouseclicked不能被使用
                    self.window.remove(self.click_sug)
                    self.window.add(self.basic_ball, x=self.paddle.x + (self.paddle.width - self.basic_ball.width) // 2,
                                    y=self.paddle.y - self.basic_ball.height)
                    self.basic_ball_count_state = 0
                    self.ball_number_count = 1              # 檯面上球數+1
                    self.ball_number_count_show.text = f"Ball number:{self.ball_number_count}"

    # 追蹤pandle，並使其不會超出界線
    def pandle_tracker(self, event):
        if self.game_not_over:
            self.paddle.x = event.x - self.paddle.width / 2
            self.paddle.y = self.window.height - PADDLE_OFFSET
            if event.x <= self.paddle.width / 2:
                self.paddle.x = 0
            elif event.x >= self.window.width - self.paddle.width / 2:
                self.paddle.x = self.window.width - self.paddle.width

    # 設定球速
    def speed(self):
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:  # half chance that change the direction of the ball
            self.__dx = - self.__dx

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return -self.__dy                   # 讓一開始的速度往上

    # 設定strong的速度和碰撞條件
    def strong_ball(self, strong):
        strong.move(0, -10)
        if self.ball_touch_point(strong) or not self.ball_touch_point(strong):
            pass

    # 設定bounce_ball的速度和碰撞條件
    def bounce_ball_playing(self, bounce_ball):
        bounce_ball.move(self.__dx, -self.__dy)
        if bounce_ball.x <= 0 or bounce_ball.x >= self.window.width - bounce_ball.width:
            self.__dx = -self.__dx                                          # bounce球接觸左右兩邊時
        if bounce_ball.y <= 0:                                              # bounce球接觸最上方
            self.__dy = -self.__dy
        if self.ball_on_pandle(bounce_ball):                               # 當bounce球接觸pandle時
            self.__dy = abs(self.__dy)                                     # 保持速度為正
        if self.ball_touch_point(bounce_ball):                             # 碰撞產生反彈
            self.__dy = -self.__dy
        if bounce_ball.y >= self.window.height:
            self.window.remove(bounce_ball)
            if self.bounce_ball_count_state == 0:
                self.bounce_ball_count_state = 1
                self.ball_number_count -= 1
                self.ball_number_count_show.text = f"Ball number:{self.ball_number_count}"
                self.bounce_ball_count_state = 2

    # 掉落物移動
    def dropping_item(self):
        self.drop_1.move(0, self.drop_vy)
        self.drop_2.move(0, self.drop_vy)
        self.drop_3.move(0, self.drop_vy)
        self.drop_4.move(0, self.drop_vy)
        self.drop_5.move(0, self.drop_vy)

    # 當有掉落物碰到pandle時，回傳true，需要給予一個引數drop
    def drop_item_function(self, drop):
        item_on_pandle_y = self.paddle.y - self.paddle.height <= drop.y <= self.paddle.y
        item_on_pandle_x = self.paddle.x <= drop.x >= self.paddle.x - self.paddle.width
        return item_on_pandle_x and item_on_pandle_y

    # 當球落在pandle之間的時候，需要給予一個引數ball
    def ball_on_pandle(self, ball):
        ball_on_x = self.paddle.x - ball.width <= ball.x <= self.paddle.x + self.paddle.width
        ball_on_y = self.paddle.y <= ball.y <= self.paddle.y + self.paddle.height
        return ball_on_x and ball_on_y

    # 用來偵測球碰撞時的反彈情況，需要給予一個引數ball，打破磚塊有機率會掉落物品
    def ball_touch_point(self, ball):
        x = (ball.x, ball.x + ball.width)
        y = (ball.y, ball.y + ball.height)
        for i in x:
            for j in y:
                self.ball_touch = self.window.get_object_at(x=i, y=j)
                if self.ball_touch is not None and self.ball_touch != self.paddle:
                    if self.ball_touch == self.show \
                            or self.ball_touch == self.drop_1 \
                            or self.ball_touch == self.drop_2 \
                            or self.ball_touch == self.drop_3 \
                            or self.ball_touch == self.drop_4 \
                            or self.ball_touch == self.drop_5 \
                            or self.ball_touch == self.basic_ball \
                            or self.ball_touch == self.strong_doggy \
                            or self.ball_touch == self.brick_number_show \
                            or self.ball_touch == self.ball_number_count_show \
                            or self.ball_touch == self.bounce_ball:
                        return False
                    else:
                        self.window.remove(self.ball_touch)
                        self.brick_number -= 1
                        self.dropping_item_type(ball)
                        self.brick_number_show.text = f"Brick:{self.brick_number}"
                        return True

    # 產生磚塊
    def brick_setting(self):
        y_distance = BRICK_OFFSET
        for i in range(BRICK_ROWS):
            x_distance = 0
            for k in range(BRICK_COLS):
                brick = GRect(self.brick.width, self.brick.height)
                brick.filled = True
                if i == 0 or i == 1 or i == 2 or i == 3 or i == 4:
                    brick.color = "black"
                if i == 5 or i == 6 or i == 7 or i == 8 or i == 9:
                    brick.fill_color = "gray"
                    brick.color = "gray"
                self.window.add(brick, x=x_distance, y=y_distance)
                x_distance += (self.brick.width + self.brick_space)
                self.brick_number += 1
            y_distance += (self.brick.height + self.brick_space)

    # 在球打破磚塊的位置生成掉落物，需要一個引數ball
    def dropping_item_type(self, ball):
        random_word = random.choice(self.drop_record)
        if random_word == "1":
            self.window.add(self.drop_1, x=ball.x, y=ball.y)  # 加一個掉落物1
            self.drop_record = self.drop_record.replace("1", "")
        if random_word == "2":
            self.window.add(self.drop_2, x=ball.x, y=ball.y)  # 加一個掉落物2
            self.drop_record = self.drop_record.replace("2", "")
        if random_word == "3":
            self.window.add(self.drop_3, x=ball.x, y=ball.y)  # 加一個掉落物3
            self.drop_record = self.drop_record.replace("3", "")
        if random_word == "4":
            self.window.add(self.drop_4, x=ball.x, y=ball.y)  # 加一個掉落物4
            self.drop_record = self.drop_record.replace("4", "")
        if random_word == "5":
            self.window.add(self.drop_5, x=ball.x, y=ball.y)  # 加一個掉落物5
            self.drop_record = self.drop_record.replace("5", "")

