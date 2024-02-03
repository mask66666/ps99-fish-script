# made by 1mask_1 on discord

import win32api, win32con
from PIL import ImageGrab
import time

OriginalWidth, OriginalHeight = 1920, 1080
cur_wtih = win32api.GetSystemMetrics(0)
cur_heig = win32api.GetSystemMetrics(1)
X_of_bar, Y_of_bar = 765 ,242 # for not half screen 1492, 234 and for left half 765 ,242

X_of_bar_new = X_of_bar * (cur_wtih // OriginalWidth)
Y_of_bar_new = Y_of_bar * (cur_wtih // OriginalHeight)

# CONSTANTS/GLOBALS
WHITE = (255,255,255)
FISH_SLEEP_TIME = 5
BAR_TOP = (X_of_bar_new, Y_of_bar_new)

CPS_CLICK_TO_FILL_BAR = 20
CPS_CLICK_TO_FILL_BAR_TIME_DELAY = 1 / CPS_CLICK_TO_FILL_BAR
THE_THINGS = "--------------------------------"

MAIN_LOOP_PRE_SEC = 15
MAIN_LOOP_PRE_SEC_TIME_DELAY = 1 / MAIN_LOOP_PRE_SEC
BOBER_COLOR = (43, 251, 255)

# click
def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0) #presses the left mouse button
    time.sleep(0.0001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0) # releases the left mouse button

# detects if pixel is white (used to tell if bober is on screen)
def check_for_white_pixel(x=None,y=None):
    if x is None or y is None:
        return -2
    screenshot = ImageGrab.grab(all_screens=True, include_layered_windows=False)
    
    try:
        pixel_color = screenshot.getpixel((x, y))
        if pixel_color == WHITE:
            return 0
        elif pixel_color == BOBER_COLOR:
            return 1
        else:
            return -1
    except Exception as e:
        print(f"Error in check_for_white_pixel: {e}")
        return -3 # this is only here to make sure when something goes wrong i know that it went wrong

# basicly stolen form Lisek_guy2 :) but in function
def check_for_bait_underwater():
    pos = win32api.GetCursorPos() # grabs position of mouse
    screenshot = ImageGrab.grab(all_screens=True, include_layered_windows=False) # grabs screenshot
    water_color = (235, 245, 245) # defines water collor thank you Lisek_guy2 for having this somewere in your scirpt idk where it is in spagetti code but it is somewere
    try:
        pixel_color = screenshot.getpixel((pos[0], pos[1])) # grabs the specifinc pixel color and makes it in to tuple
        
        # Adjust these values to match the underwater color of your bait
        if all(c1 - 10 <= c2 <= c1 + 10 for c1, c2 in zip(pixel_color, water_color)): # Lisek_guy2 code :)
            return 0 # true
        else:
            return -1 # false
    except Exception as e:
        print(f"Error in check_for_bait_underwater: {e}") # prints eror mesage
        return -2 # error

# throws and caches fish
def fish():
    start_time = time.time()
    time.sleep(1)
    click()
    while check_for_bait_underwater() != 0:
        time_dif = time.time() - start_time
        if time_dif > 9:
            break
        #ime.sleep(0.05)
    #time.sleep(FISH_SLEEP_TIME) # waits the desired amaut of time before hopefully caching fish
    click()
    time.sleep(0.4)

# when fish() is done and WHITE_BAR is pressent it will click to fill it
def click_to_fill_bar():
    global last_click_to_fill_bar_time
    start_time = time.time()
    res = check_for_white_pixel(BAR_TOP[0],BAR_TOP[1]) #cheks initaly
    while res == 0:
        res = check_for_white_pixel(BAR_TOP[0],BAR_TOP[1]) #checks in loop so it knows when it is done
        if res != 0: # checks if res is still 0 and if not ends the function
            break
        click()
        time.sleep(CPS_CLICK_TO_FILL_BAR_TIME_DELAY) # delays the clicks from themselfs bc it would be useless
    end_time = time.time()
    last_click_to_fill_bar_time = end_time - start_time
    time.sleep(0.5)

# main function
def main():
    # some values
    last_sucess_time = time.time()
    sucess = 0
    fail = 0
    errors = 0
    while True:
        # fishes a fish
        fish()

        # if fished fish it will count it as sucess otherwise a fail
        if check_for_white_pixel(BAR_TOP[0],BAR_TOP[1]) == 0:
            sucess += 1
            last_sucess_time = time.time()
        elif check_for_white_pixel(BAR_TOP[0],BAR_TOP[1]) == -3:
            errors += 1
        else:
            fail += 1
            time_dif = time.time() - last_sucess_time
            if time_dif >= 60:
                print("1 minute passed without suceess. clicking")
                click()
                last_sucess_time = time.time()
                time.sleep(1)
        
        
        
        #print values
        print(f"{THE_THINGS}\nnumber of sucess: {sucess}\nnumber of fails: {fail}\nnumber of errors: {errors}\n{THE_THINGS}")

        # now finaly do the fish and if it has not cought a fish before it will just not do anything
        click_to_fill_bar()
        time.sleep(MAIN_LOOP_PRE_SEC_TIME_DELAY)

if __name__ == "__main__":
    main()