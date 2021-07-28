"""
File: stanCodoshop.py
----------------------------------------------
SC101_Assignment3
Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.

-----------------------------------------------

"""
import math
import os
import sys
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns the color distance between pixel and mean RGB value

    Input:
        pixel (Pixel): pixel with RGB values to be compared
        red (int): average red value across all images
        green (int): average green value across all images
        blue (int): average blue value across all images

    Returns:
        dist (float): color distance between red, green, and blue pixel values

    """
    pixel_dist = math.sqrt((red - pixel.red) ** 2 + (green-pixel.green)**2 + (blue-pixel.blue)**2)
    return pixel_dist


def get_average(pixels):
    """
    Given a list of pixels, finds the average red, blue, and green values

    Input:
        pixels (List[Pixel]): list of pixels to be averaged
    Returns:
        rgb (List[int]): list of average red, green, blue values across pixels respectively

    Assumes you are returning in the order: [red, green, blue]

    """
    # 分別加總每張圖片的red, green, blue pixel，計算後回傳list
    red_pixel = 0
    green_pixel = 0
    blue_pixel = 0
    number = len(pixels)
    for i in range(number):
        red_pixel += pixels[i].red
        green_pixel += pixels[i].green
        blue_pixel += pixels[i].blue
    return [red_pixel//number, green_pixel//number, blue_pixel//number]


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest
    distance from the average red, green, and blue values across all pixels.

    Input:
        pixels (List[Pixel]): list of pixels to be averaged and compared
    Returns:
        best (Pixel): pixel closest to RGB averages

    """
    avg = get_average(pixels)                                       # 計算本組圖片的RGB平均值，
    pixels_dic = {}                                        # 建立空的dict用來儲存每張圖片的list of pixel所對應的color distance
    for i in pixels:
        pixels_dic[i] = get_pixel_dist(i, avg[0], avg[1], avg[2])
    return min(pixels_dic, key=pixels_dic.get)                          # 找出value的最小值，並回傳key(該圖片的pixel list）


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    # Write code to populate image and create the 'ghost' effect
    for x in range(width):
        for y in range(height):
            images_pixel_list = []
            for i in images:
                images_pixel_list.append(i.get_pixel(x, y))                   # 把全部的圖片的 (x,y) pixel丟到list
            result.set_pixel(x, y, get_best_pixel(images_pixel_list))
    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    # 把資料夾的檔案名稱for loop
    for filename in os.listdir(dir):                        # 得到在terminal輸入的資料夾名稱(main():args[0]，
        if filename.endswith('.jpg'):                       # 遇到副檔名為.jpg時，
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []                                 # 把資料夾裡的所有圖片裝到一個list
    jpgs = jpgs_in_dir(dir)                     # 得到圖片的檔案名
    for filename in jpgs:                       #
        print("Loading", filename)
        image = SimpleImage(filename)           # 創立一個新的圖片
        images.append(image)                    #
    return images                               # 回傳包有所有"圖片"的list


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]                         # 得到除了第0位置的輸入資料(這邊等於輸入的資料夾名稱)
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])               # 得到資料夾名稱後交給load_images處理，會得到資料夾所有的.jpg
    solve(images)                               # 處理所有圖片


if __name__ == '__main__':
    main()
