import numpy
import time
import math
from ppadb.client import Client
from PIL import Image

# default ppadb settings
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

Completed_levels = 18

# exit out of there is no device detected
if len(devices) == 0:
    print('no device attached')
    quit()

# Assume that we only attached one device to this thing
device = devices[0]

# gets a screenshot of the moment; reason is just to be easier to debug
def get_screenshot(reason= ""):
    i = device.screencap()
    with open('screen.png', 'wb') as b:
        b.write(i)
    # sometimes the image is corrupted and the verify function checks if it is
    try:
        i = Image.open('screen.png')
        test = Image.open('screen.png')
        test.verify()
        i = numpy.array(i, dtype=numpy.uint8)
        print("took screenshot " + reason)
        # just testing if we can pull an array or not
        test2 = [list(i[:3]) for i in i[80]]

    # got a corrupted image so try again essentially.
    except (IOError, SyntaxError, TypeError):
        return get_screenshot()
    return i

# take a screenshot and use it to measure the screen size as well as other functions
def find_dimentions():
    screen = get_screenshot("to get screensize")
    return len(screen[0]), len(screen)

W, H = find_dimentions()

# checks if the rgb colors are within an acceptable range. Its highly unlikely different colors
# are gonna be implemented in this game
def is_valid_color(x, r_min, r_max, g_min, g_max, b_min, b_max):
    return r_min <= x[0] <= r_max and g_min <= x[1] <= g_max and b_min <= x[2] <= b_max


# from the main menu, open the story mode
def open_story():
    tap(W / 6, H * (20 / 21))
    tap(W * (3 / 8), H / 2)
    tap(W / 2, H * (5 / 16))


# click the autoplay and wait for it to finish
def play_level():
    tap(W * (7 / 9), H * (20 / 21))
    find_green("finding autoplay")


# taps on screen, if we don't care about position we can just do tap()
def tap(x=W / 2, y=H / 2):
    device.shell(f'input tap {int(x)} {int(y)}')
    # device.shell('input tap ' + str(x) + ' ' + str(y))

# drags the screen for a short amount of time.
def drag(x1,y1,x2 = None,y2 = None):
    if x2 == None:
        x2 = x1
    if y2 == None:
        y2 = y1
    device.shell(f'input touchscreen swipe {int(x1)} {int(y1)} {int(x2)} {int(y2)} 200')


# the most recent level to play
def start_lvl():
    tap(W / 2, H * (9 / 23))
    time.sleep(0.5)
    find_green("finding play button")
    #out_of_stamina()
    time.sleep(0.75)
    find_green("to refill stamina (if any)")
    time.sleep(0.75)
    find_green()


# find the skip button if there is any, only ever in top right. No penalty if there isn't any
def find_skip():
    screen = get_screenshot("finding skip button")
    p = [list(i[:3]) for i in screen[80]]
    for i in range(int(W * 0.75), W):
        x = p[i]
        if is_valid_color(x, 100, 125, 30, 50, 55, 70):
            tap(i, 80)
            return True
    return False


# loops through a column of pixels and sees if the rgb value more or less becomes green.
def find_green(reason=""):
    screen = get_screenshot(reason)
    # using the middle collumn and sees if it detects a green, the green is repeated throughout
    for i in range(H):
        # start at the bottom half since that's where the green button tend to be at
        p = [list(i[:3]) for i in screen[int(i)]]
        x = p[int(W / 2)]
        # there are 2 distinctive shades of green so
        if is_valid_color(x, 60, 70, 100, 110, 90, 100) or is_valid_color(x, 80, 90, 110, 120, 90, 100):
            tap(W / 2, i)
            return True
    # unlike skip, there are multiple green buttons to press and they are random so this makes them easier to handle
    return False


# see if there is a full black screen by getting 4 areas and seeing if the rgb = 0
# while the game is playing itself, it'll check if it detects a red value corrisponding to the gameover
def did_game_over():
    screen = get_screenshot("finding game over")
    p = [list(i[:3]) for i in screen[int(H / 2)]]
    # no need to check the entire width, only the first quarter is sufficent
    for i in range(0, int(W/4), 5):
        x = p[i]
        # takes in account text changes brightness so it waits till the brightest or dullest
        if is_valid_color(x, 140, 160, 40, 60, 30, 50) or is_valid_color(x,105,120,30,40,25,30):
            return True
    return False


# goes through the game over screen to get us back to the main level
def game_over():
    tap()
    time.sleep(1)
    find_green("finding play again")
    time.sleep(1)
    find_green("finding play again")


# checks to see the middle row has a yellow that is only found in the stage clear
def did_stage_clear():
    screen = get_screenshot("finding stage clear")
    p = [list(i[:3]) for i in screen[int(H / 2)]]
    for i in range(int(W/4), int(W * 0.75), 5):
        x = p[i]
        if is_valid_color(x, 205, 225, 190, 210, 100, 120):
            return True

    return False



# clicks the screen and goes over the reward section. sometimes theres 1-3 things to click but
# nothing happens if it doesn't see any so who cares
def stage_clear():
    # keeps track of how many levels have been completed
    global Completed_levels
    Completed_levels += 1
    print("detected stage is cleared")
    temp = True
    tap()
    time.sleep(4)
    find_skip()
    time.sleep(3)
    # when you unlock a character and the animation takes forever
    # chapter 1 lvl 5 book 2 and 3
    if Completed_levels == 48 or Completed_levels == 98 or Completed_levels == 163:
        print("waiting for unlocking character animation to finish")
        time.sleep(4)
        tap()
        tap()
    # the amount of green buttons to press is arbitrary and this fixes that
    while temp:
        temp = find_green("finding level bonus (if any)")
        time.sleep(1)


# after autoplay is clicked, this will check if a gameover or level clear is detected
def automate_game():
    play_level()
    while True:
        if did_game_over():
            print("game over detected")
            game_over()
            time.sleep(6)
            play_level()
# if a skip button was found while this was running. its safe to assume stage was cleared
        elif did_stage_clear() or find_skip():
            return
        else:
            # sometimes there will be a green pop up and we just tap it if its there
            find_green("...")


# annoying that this has a small margin of error
def change_book():
    y = H * (13/46)
    x1 = W /2
    x2 = W / 6
    drag(x1, y, x2, y)


def start_chapter():
    tap(W/2, H * (9/23))


def out_of_stamina():
    global Completed_levels
    if Completed_levels == 5:
        time.sleep(1)
        find_green("refill stamina")
        pass
    else:
        return


# this block of code completes one chapter at a time
def repeat_chapter(n):
    for i in range(n):
        print("selecting the next level")
        start_lvl()
        pre_lvl_cutscene()
        # finally can start clicking play
        time.sleep(2)
        # click autoplay for a while
        automate_game()
        stage_clear()
        # have to consider that there is animation to selecting level before reseting the cycle
        time.sleep(2)

# goes through one book with the number of chapters to go by
def finish_book(chapters):
    for i in range(chapters):
        start_chapter()
        repeat_chapter(5)
        # take in account loading new chapters takes some time
        time.sleep(2)
        print("chapter done, picking next one")
    print("Book done, picking next one")

# all the books have the same format, so we can plug them to this function
def play_everything():
    global Completed_levels
    # do book 1, chapter 10-5 is stupidly hard so lets give up. 45 levels in total
    if Completed_levels < 48:
        play_what_chapters(9)
    change_book()
    # do book 2 chapter 11-5 is hard. 60 lvls in total
    if Completed_levels < 108:
        # make sure we do not include previous books. each book always has 5 levels so we multiply
        # by how many chapters completed
        Completed_levels -= 9 * 5
        play_what_chapters(10)
    change_book()
    # do book 3
    if Completed_levels < 163:
        Completed_levels -= 19 * 5
        play_what_chapters(11)
    change_book()
    # do book 4
    if Completed_levels < 223:
        Completed_levels -= 30 * 5
        play_what_chapters(10)
    change_book()
    # do book 5
    if Completed_levels < 283:
        Completed_levels -= 40 * 5
        play_what_chapters(10)
    change_book()
    finish_book(2)

def play_what_chapters(max):
    # total levels completed that isn't the tutorial
    # 14 2 chap 4 levels
    x = Completed_levels - 3
    # finding how many books has been completed
    chapters_done = math.ceil(x/5)
    # finding how many levels has been done
    levels_done = x % 5
    # means we finished a chapter and have to start one
    print(chapters_done, levels_done)
    if levels_done == 0:
        # copy and paste of finish chapter
        start_chapter()
        # finish the remaining levels in that chapter
        repeat_chapter(5 - levels_done)
        # take in account loading new chapters takes some time
        time.sleep(2)
        print("chapter done, picking next one")
    # finish the rest of the book
    finish_book(max - chapters_done)


def remaining_levels():
    global Completed_levels
    x = Completed_levels
    x -= 3
    y = x % 5
    if y == 0:
        y = 5
    # copy and paste of finish chapter
    start_chapter()
    repeat_chapter(y)
    # take in account loading new chapters takes some time
    time.sleep(2)
    print("chapter done, picking next one")

def tutorial():
    # level 1
    find_skip()
    find_green()
    find_skip()
    drag(100,H * (14/23),W * (5/12),H * (14/23))
    time.sleep(1.5)
    find_skip()
    drag(W * (6/13), H * (14 / 23), W * (10 / 13), H * (12 / 23))
    time.sleep(3)
    tap()
    # stage clear pops up
    time.sleep(1)
    tap()
    find_skip()
    time.sleep(2)
    # preface 2 screen booted up
    find_skip()
    time.sleep(3)
    find_skip()
    drag(100, H * (16 / 23), W * (8 / 13), H * (14 / 23))
    time.sleep(6)
    find_skip()
    drag(100, H * (13 / 23), W * (8 / 13), H * (13 / 23))
    time.sleep(6)
    tap()
    time.sleep(7)
    find_skip()
    drag(W * (5 / 13), H * (13 / 23), W * (9 / 13), H * (13 / 23))
    time.sleep(8)
    tap()
    # stage clear pop up
    time.sleep(3)
    tap()
    time.sleep(5)
    find_skip()
    find_green()
    # download screen
    time.sleep(3)
    find_green()


def tutorial2():
    for i in range(3):
        start_lvl()
        # open prologue 2
        pre_lvl_cutscene()
        time.sleep(2.5)
        # only the tutorial will give instructions before you can access autoplay
        find_green("skipping dumb how to (if any)")
        time.sleep(1)
        automate_game()
        stage_clear()
        time.sleep(3)


def title_screen():
    tap()


# after we click battle, there will most liekly gonna be diologue we have to sit through
def pre_lvl_cutscene():
    # sometimes there will be diologue before it transitions to the level
    time.sleep(5.5)
    find_skip()
    # displaying what chapter and lvl your in
    time.sleep(3)
    find_skip()


def main():
    print("Fire Emblem begins")
    open_story()
    time.sleep(1)
    # complete tutorial
    if Completed_levels < 3:
        print("opened prologue")
        start_chapter()
        time.sleep(1)
        # prologue has some stupid shit
        tutorial2()
    # start playing the rest of the book since the steps will be identical basically
    play_everything()
    pass


if __name__ == '__main__':
    try:
        main()
    except:
        raise Exception("You have completed " + str(Completed_levels) + " levels. PLease change Completed_levels")
    pass
