import ctypes
from sdl2 import *

WINDOW_HEIGHT = 860
WINDOW_WIDTH = 1000
BGCOLOR = [0, 100, 255]


# PIANO STUFF
PIANO_LOCATION = [50, 600]

WHITE_PIANO_COLOR = [255, 255, 255]
BLACK_PIANO_COLOR = [0, 0, 0]
PLAYED_PIANO_COLOR = [160, 180, 20]

# Width is first in dim
WHITE_KEY_DIMS = [50, 200]
BLACK_KEY_DIMS = [30, 110]
NUM_OCTAVES = 2

FRAME_DURATION = 60 # in milliseconds
SOUND_FRAME_DURATION = int(0.4 * (1000 / FRAME_DURATION))

# INT TO PIANO KEY MAPPING:
#  0 is C, from then on all evens are white keys 
#   and odds are black keys. Cannot be higher than 12.
#  Also B# and E# also known as 13 and 5 do not exist!!
# Thomas' system: 1 num = 1 half step
# So, need to return x but subtract given 5 and 13
# This returns the number of half-steps up x is
def piano_key_of_int(x):
    octave_num = x // 14
    octave_x = x % 14
    assert octave_x != 5 and octave_x != 13, "input can't be note 5 or 13"
    key = x
    # We'll subtract 2 for each octave (which contains 2 non-notes)
    # Also subtract 1 if above 13 and 1 if above 5
    key -= (octave_num * 2) + int(octave_x > 13) + int(octave_x > 5)
    return key

def play_note(x):
    key = piano_key_of_int(x)
    # TODO: THIS IS A PLACEHOLDER
    print("Playing", "cCdDefFgGaAb"[key % 12] + str(key // 12))

def clear_screen(renderer):
    SDL_SetRenderDrawColor(renderer, BGCOLOR[0], BGCOLOR[1], BGCOLOR[2], 255);
    SDL_RenderClear(renderer);

def fill_piano_rect(renderer, x, y, is_white, is_played):
    w, h = WHITE_KEY_DIMS if is_white else BLACK_KEY_DIMS
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); # black border
    SDL_RenderDrawRect(renderer, SDL_Rect(x - 1, y - 1, w + 2, h + 2))

    c1, c2, c3 = ((WHITE_PIANO_COLOR if is_white else BLACK_PIANO_COLOR) 
                    if not is_played else PLAYED_PIANO_COLOR)
    SDL_SetRenderDrawColor(renderer, c1, c2, c3, 255)
    SDL_RenderFillRect(renderer, SDL_Rect(x, y, w, h))

def calc_piano_key_x(n, x):
    drawx = x + ((n // 2) * WHITE_KEY_DIMS[0]) 
    if n % 2 == 0: 
        return drawx
    else:
        black_x_component = WHITE_KEY_DIMS[0] // 2 + BLACK_KEY_DIMS[0] // 3
        return drawx + black_x_component

def draw_octave(renderer, x, y, drawkey):
    # White keys
    for i in range(0, 14, 2):
        drawx = calc_piano_key_x(i, x)
        played = i == drawkey
        fill_piano_rect(renderer, drawx, y, True, played)
    # Black keys
    for i in range(1, 13, 2):
        drawx = calc_piano_key_x(i, x)
        played = i == drawkey
        if i != 5:
            fill_piano_rect(renderer, drawx, y, False, played)

def octave_width():
    return WHITE_KEY_DIMS[0] * 7 

def piano_width():
    return octave_width() * NUM_OCTAVES

def draw_piano(renderer, pressed_piano_key):
    x, y = PIANO_LOCATION
    for i in range(NUM_OCTAVES):
        drawkey = pressed_piano_key % 14 if pressed_piano_key // 14 == i else -1
        draw_octave(renderer, x + (i * octave_width()), y, drawkey)

def calc_piano_key_pressed(x, y):
    px, py = PIANO_LOCATION
    x = x - px
    y = y - py
    if x > piano_width() or y > WHITE_KEY_DIMS[1] or x < 0 or y < 0:
        return -1
    numkeys = 14 * NUM_OCTAVES

    # Need to calc white, black keys separately bc of overlap
    whitekey = -1
    for i in range(0, numkeys, 2):
        if x >= calc_piano_key_x(i, 0):
            if i == numkeys - 1 or x < calc_piano_key_x(i + 2, 0):
                whitekey = i
    blackkey = -1
    for i in range(1, numkeys, 2):
        piano_key_x = calc_piano_key_x(i, 0)
        if i % 14 not in [5, 13]:
            if piano_key_x + BLACK_KEY_DIMS[0] > x >= piano_key_x and y < BLACK_KEY_DIMS[1]:
                if i == numkeys - 1 or x < calc_piano_key_x(i + 2, 0):
                    blackkey = i
    return blackkey if blackkey != -1 else whitekey

def loop(renderer):
    piano_press_frame = 0
    pressed_piano_key = -1
    event = SDL_Event()
    while True:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                return
            elif event.type == SDL_MOUSEBUTTONDOWN:
                butx, buty = event.button.x, event.button.y
                pressed_piano_key = calc_piano_key_pressed(butx, buty)
                piano_press_frame = 0
                play_note(pressed_piano_key)

        if piano_press_frame < SOUND_FRAME_DURATION:
            piano_press_frame += 1
        elif pressed_piano_key != -1:
            pressed_piano_key = -1
            print("done playing")

        clear_screen(renderer)
        draw_piano(renderer, pressed_piano_key)
        SDL_RenderPresent(renderer)
        SDL_Delay(FRAME_DURATION)

def main():
    SDL_Init(SDL_INIT_VIDEO)
    window = SDL_CreateWindow(b"timbre", SDL_WINDOWPOS_CENTERED, 
                            SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, 
                            WINDOW_HEIGHT, SDL_WINDOW_SHOWN)
    rend_flags = SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC
    renderer = SDL_CreateRenderer(window, -1, rend_flags)

    loop(renderer)

    SDL_DestroyRenderer(renderer)
    SDL_DestroyWindow(window)
    SDL_Quit()

if __name__ == "__main__":
    main()
