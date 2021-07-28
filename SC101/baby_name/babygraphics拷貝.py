"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue', 'pink', 'darkred']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    # （總長-2個視窗間隔 / list of years數量)乘上index + 初始間隔
    x_position = (width - 2 * GRAPH_MARGIN_SIZE) / len(YEARS) * year_index + GRAPH_MARGIN_SIZE
    return x_position


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')  # delete all existing lines from the canvas

    # Write your code below this line
    # 產生橫線
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE,
                       width=LINE_WIDTH)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, CANVAS_WIDTH - GRAPH_MARGIN_SIZE,
                       CANVAS_HEIGHT - GRAPH_MARGIN_SIZE, width=LINE_WIDTH)
    # 產生直線
    for i in range(len(YEARS)):
        canvas.create_line(get_x_coordinate(CANVAS_WIDTH, i), 0, get_x_coordinate(CANVAS_WIDTH, i), CANVAS_HEIGHT,
                           width=LINE_WIDTH)
        canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i) + TEXT_DX, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
                           text=YEARS[i], anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)  # draw the fixed background grid

    color_index = 0
    for name in lookup_names:
        # 指定字的顏色by color list index
        color = COLORS[color_index]
        line_x_y_list = []                                          # 用來儲存畫線用的list
        for i in YEARS:                                             # 找出年份(年份為int)
            if name_data[name].get(str(i)) is not None:             # 判斷是否有key存在
                # 透過get_x_coordinate得到x。y需先把y軸的線長度按照MAX_RANK的比例分配後，乘上對應的rank分數
                canvas.create_text(get_x_coordinate(CANVAS_WIDTH, YEARS.index(i)) + TEXT_DX,
                                   int(name_data[name][str(i)]) * (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE)/MAX_RANK + GRAPH_MARGIN_SIZE,
                                   text=f"{name} {name_data[name][str(i)]}",
                                   anchor=tkinter.SW, fill=color)
                # 把座標加入list
                line_x_y_list.append(get_x_coordinate(CANVAS_WIDTH, YEARS.index(i)))
                line_x_y_list.append(int(name_data[name][str(i)]) * (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE)/MAX_RANK + GRAPH_MARGIN_SIZE)
            else:
                # 假如沒有排名，印出帶有*的名子
                canvas.create_text(get_x_coordinate(CANVAS_WIDTH, YEARS.index(i)) + TEXT_DX, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
                                   text=f"{name} *",
                                   anchor=tkinter.SW,
                                   fill=color)
                # 把座標加入list
                line_x_y_list.append(get_x_coordinate(CANVAS_WIDTH, YEARS.index(i)))
                line_x_y_list.append(CANVAS_HEIGHT - GRAPH_MARGIN_SIZE)
            # 假如有4個座標就畫線
            if len(line_x_y_list) == 4:
                canvas.create_line(line_x_y_list[0], line_x_y_list[1], line_x_y_list[2],
                                   line_x_y_list[3],
                                   width=LINE_WIDTH,
                                   fill=color)
                # 移除前兩個座標
                line_x_y_list.pop(0)
                line_x_y_list.pop(0)
        
        color_index += 1
        # 假如顏色用完，從頭開始
        if color_index == len(COLORS):
            color_index = 0
# main() code is provided, feel free to read through it but DO NOT MODIFY


def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
