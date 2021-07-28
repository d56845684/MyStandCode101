"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

1. 建立ball_playing，當live > 0時執行
2. 當ball_playing執行時：brick_number 為0時讓live = 0 ; 球掉到最下方時 live -= 1，以上情況皆終止一次ball_playing
3. 當live = 0 時，終止main()的while loop，同時讓game_not_over = False
4. 判斷磚塊數量，0的話則顯示Win，不為0則為Lose
"""
from campy.gui.events.timer import pause
from breakoutgraphics_ext import BreakoutGraphics
FRAME_RATE = 1000 / 120  # 120 frames per second
graphics = BreakoutGraphics()
vx = graphics.get_dx()
vy = graphics.get_dy()
graphics_open = False


def main():
    # 使用者點擊介面
    # 點擊開始使graphics.game == True，執行major_playing
    # graphics.game_not_over = False

    major_playing()
    # 結束後，進行排名


def major_playing():
    # 設定遊戲介面
    graphics.brick_setting()
    graphics.window.add(graphics.paddle,
                        x=(graphics.window_width - graphics.paddle.width) // 2,
                        y=graphics.window_height - graphics.paddle_offset)
    graphics.window.add(graphics.brick_number_show,
                        x=10,
                        y=graphics.window.height - 5)
    graphics.window.add(graphics.ball_number_count_show,
                        x=100,
                        y=graphics.window.height - 5)
    graphics.window.add(graphics.show,
                        x=graphics.window.width - 75,
                        y=graphics.window.height - 5)
    # 點擊後開始遊戲
    while graphics.live > 0:
        # 出現點擊提示
        if graphics.click_suggest:
            graphics.window.add(graphics.click_sug, x=graphics.window.width / 2 - 40,
                                y=graphics.window.height / 2)
            graphics.click_suggest = False
        pause(FRAME_RATE)
        if graphics.game:
            ball_playing(graphics.basic_ball)
    graphics.game_not_over = False
    # 方塊為0遊戲結束
    if graphics.brick_number == 0:
        graphics.window.add(graphics.win, x=graphics.window.width / 2 - 40, y=graphics.window.height / 2)
    else:
        graphics.window.add(graphics.lose, x=graphics.window.width / 2 - 40, y=graphics.window.height / 2)


def ball_playing(ball_label):
    bounce_check = True
    while True:
        graphics.dropping_item()                                                    # 打破磚塊時物品掉落
        if graphics.drop_item_function(graphics.drop_1):                          # 當掉落物1碰到pandle，讓球變顏色
            graphics.window.remove(graphics.drop_1)
            ball_label.fill_color = "blue"
        if graphics.drop_item_function(graphics.drop_2):                          # 當掉落物2碰到pandle，加一顆球
            graphics.window.remove(graphics.drop_2)
            graphics.window.add(graphics.bounce_ball,
                                x=graphics.paddle.x + (graphics.paddle.width - graphics.bounce_ball.width) // 2,
                                y=graphics.paddle.y - graphics.bounce_ball.height)
            if bounce_check:
                graphics.ball_number_count += 1                                 # 檯面上球數+1
                graphics.ball_number_count_show.text = f"Ball number:{graphics.ball_number_count}"
                bounce_check = False                                                   # 確保不會重複計算
        for i in (graphics.drop_3, graphics.drop_4, graphics.drop_5,):
            if graphics.drop_item_function(i):                                  # 當掉落物3碰到pandle，發射
                graphics.window.remove(i)
                graphics.window.add(graphics.strong_doggy,
                                    x=graphics.paddle.x + (graphics.paddle.width - graphics.strong_doggy.width) // 2,
                                    y=graphics.paddle.y - graphics.strong_doggy.height)

        # 分別得到球的水平 & 垂直速度
        global vx
        global vy
        ball_label.move(vx, vy)
        pause(FRAME_RATE)
        graphics.bounce_ball_playing(graphics.bounce_ball)                              # 呼叫bounce_ball_playing
        graphics.strong_ball(graphics.strong_doggy)
        graphics.dropping_item()                                                        # 打破磚塊時物品掉落
        speed_change(ball_label)                                                        # 改變球的方向
        if graphics.ball_on_pandle(ball_label):                                         # 當球接觸pandle時
            if vy > 0:
                vy = -vy
        if graphics.ball_touch_point(ball_label):                # 碰撞產生反彈
            vy = -vy
        if graphics.brick_number == 0:                          # 當磚塊數量為0時的
            graphics.live = 0                                   # 使生命為0並結束遊戲
            break                                               # break迴圈

        if ball_label.y > graphics.window.height:
            if graphics.basic_ball_count_state == 0:            # 當basic ball state狀態為0時
                graphics.basic_ball_count_state = 1             # 先讓basic ball state = 1
                graphics.window.remove(ball_label)
                graphics.ball_number_count -= 1                 # 檯面上球數-1
                graphics.ball_number_count_show.text = f"Ball number:{graphics.ball_number_count}"
                graphics.basic_ball_count_state = 2             # 最後讓basic ball state = 2
        if graphics.ball_number_count <= 0:                     # 檯面上球數為0時，生命值-1
            graphics.live -= 1
            # dropping_remove()                                   # 移除所有掉落物
            graphics.check = True                               # 使可接受下一輪遊戲
            graphics.game = False                               # 使本輪遊戲終止
            graphics.click_suggest = True                       # 點擊提示打開
            graphics.show.text = f"live left: {graphics.live}"
            break


def speed_change(ball_label):
    global vx
    global vy
    if ball_label.x <= 0 or ball_label.x >= graphics.window.width - ball_label.width:
        vx = -vx
    if ball_label.y <= 0:
        vy = -vy


def dropping_remove():
    graphics.window.remove(graphics.drop_1)
    graphics.window.remove(graphics.drop_2)
    graphics.window.remove(graphics.drop_3)


if __name__ == '__main__':
    main()
