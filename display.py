import ctypes
from sdl2 import *
from audio import calculate_sound 
import calculations 
from random import random
import math 

RADIUS_FACTOR = 0.8

WINDOW_HEIGHT = 860
WINDOW_WIDTH = 1000
BGCOLOR = [240, 240, 240]

# PIANO STUFF
PIANO_LOCATION = [120, 600]

WHITE_PIANO_COLOR = [255, 255, 255]
BLACK_PIANO_COLOR = [0, 0, 0]
PLAYED_PIANO_COLOR = [160, 180, 20]

# Width is first in dim
WHITE_KEY_DIMS = [50, 200]
BLACK_KEY_DIMS = [30, 110]
NUM_OCTAVES = 2

FRAME_DURATION = 60 # in milliseconds
SOUND_FRAME_DURATION = int(0.35 * (1000 / FRAME_DURATION))

# Spokes
NUM_NEIGHBORS = 8
NEIGHBOR_RADIUS = 30
# Circles will be a tuple (x, y, r)
WHEEL_FOCUS = (WINDOW_WIDTH // 2, 300, 30)
# Wheel will be a list of [c, v] where c is a circle and v a feature vector
WHEEL_RADIUS = 150

HIGHLIGHT_COLOR = [192, 243, 27]
HIGHLIGHT_EXTRA_RADIUS = 20

# Buttons
NEW_NEIGHBORS = (WINDOW_WIDTH // 2 + 150, 50, 100, 34)
NEW_NEIGHBORS_COLOR = [200, 150, 20]
BACK_BUTTON = (WINDOW_WIDTH // 2 - 150 - 100, 50, 100, 34)
BACK_BUTTON_COLOR = [50, 50, 200]

TRIANGLE_BOX_DIMENSIONS = [75, 75]

def color_of_feature_vector(feature_vector):
    not_first_fv = feature_vector[1:]
    reverse_fv = not_first_fv[::-1]
    return [int(255 * n) for n in reverse_fv] 

# INT TO PIANO KEY MAPPING:
#  0 is C, from then on all evens are white keys 
#   and odds are black keys. Cannot be higher than 12.
#  Also B# and E# also known as 13 and 5 do not exist!!
# Thomas' system: 1 num = 1 half step
# So, need to return x but subtract given 5 and 13
# This returns the number of half-steps up x is
def calc_piano_key(x):
    octave_num = x // 14
    octave_x = x % 14
    assert octave_x != 5 and octave_x != 13, "input can't be note 5 or 13"
    key = x
    # We'll subtract 2 for each octave (which contains 2 non-notes)
    # Also subtract 1 if above 13 and 1 if above 5
    key -= (octave_num * 2) + int(octave_x > 13) + int(octave_x > 5)
    return key

def generate_neighbors_list(wheel_focus, radius):
    """ 
    Generates neighbors list but puts in some empty or test vector
    for the feature vector component. Just calculates locations.
    """
    wheel_vector = wheel_focus[1]
    neighbors = []
    angle_increment = math.radians(360 / calculations.num_neighbors)
    fx, fy, _ = WHEEL_FOCUS
    vector_neighbors = calculations.calculate_neighbors(wheel_vector, radius)
    if len(vector_neighbors) < calculations.num_neighbors:
        return []
    for i in range(calculations.num_neighbors):
        angle = angle_increment * i
        x = int(WHEEL_RADIUS * math.cos(angle)) + fx
        y = int(WHEEL_RADIUS * math.sin(angle)) + fy
        neighbors.append([(x, y, NEIGHBOR_RADIUS), vector_neighbors[i]])
    return neighbors

def triangle_rect_of_button(button_rec, is_left):
    x, y, w, h = button_rec
    tw, th = TRIANGLE_BOX_DIMENSIONS
    ty = y - ((th - h) // 2)
    tx = x - tw + 1 if is_left else x + w
    return (tx, ty, tw, th)

def in_rect(rec, clickx, clicky):
    x, y, w, h = rec
    return x < clickx < x + w and y < clicky < y + h

def clear_screen(renderer):
    SDL_SetRenderDrawColor(renderer, BGCOLOR[0], BGCOLOR[1], BGCOLOR[2], 255);
    SDL_RenderClear(renderer);

def drawpixel(renderer, x, y, pixel_dims=[1,1]):
    SDL_RenderFillRect(renderer, SDL_Rect(x, y, pixel_dims[0], pixel_dims[1]))

def hypotenuse(a, b):
    return math.sqrt(math.pow(a, 2) + math.pow(b, 2))

def in_circle(centerx, centery, radius, x, y):
    distance = hypotenuse(x - centerx, y - centery)
    return distance < radius

# Color should be a list [r, g, b] of 3 nums
def draw_circle(renderer, centerx, centery, radius, color):
    r, g, b = color
    diameter = radius * 2
    startx, starty = centerx - radius, centery - radius
    for x in range(diameter):
        for y in range(diameter):
            drawx, drawy = x + startx, y + starty
            if in_circle(centerx, centery, radius, drawx, drawy):
                SDL_SetRenderDrawColor(renderer, r, g, b, 255) 
                drawpixel(renderer, drawx, drawy)

def draw_wheel(renderer, wheel, highlight_idx):
    for i in range(len(wheel)):
        ls = wheel[i]
        x, y, r = ls[0]
        if i == highlight_idx:
            color = HIGHLIGHT_COLOR
            draw_circle(renderer, x, y, r + HIGHLIGHT_EXTRA_RADIUS, color)
        color = color_of_feature_vector(ls[1])
        draw_circle(renderer, x, y, r, color)

def fill_rect(renderer, rec, color):
    x, y, w, h = rec
    r, g, b = color
    SDL_SetRenderDrawColor(renderer, r, g, b, 255) # black border
    SDL_RenderFillRect(renderer, SDL_Rect(x, y, w, h))

def in_triangle(tx, ty, radius, x, y, is_left):
    if abs(x - tx) > radius or abs(y - ty) > radius: return False
    if is_left:
        x = 2 * tx - x
    if y < ty:
        y = 2 * ty - y
    return y - ty <= 0.5 * (tx + radius - x)
    
def in_arrow(rec, clickx, clicky, is_left):
    tx, ty, tw, th = triangle_rect_of_button(rec, is_left)
    r = tw // 2
    return in_rect(rec, clickx, clicky) or \
           in_triangle(tx + r, ty + r, r, clickx, clicky, is_left)

def fill_triangle(renderer, rec, color, is_left):
    """ Assumes square """
    tx, ty, tw, th  = triangle_rect_of_button(rec, is_left)
    radius = tw // 2
    r, g, b = color
    diameter = radius * 2
    centerx, centery = tx + radius, ty + radius
    for x in range(diameter):
        for y in range(diameter):
            drawx, drawy = x + tx, y + ty
            if in_triangle(centerx, centery, radius, drawx, drawy, is_left):
                SDL_SetRenderDrawColor(renderer, r, g, b, 255) 
                drawpixel(renderer, drawx, drawy)

def fill_arrow(renderer, rec, color, is_left):
    fill_rect(renderer, rec, color)
    fill_triangle(renderer, rec, color, is_left)


def fill_piano_rect(renderer, x, y, is_white, is_played):
    w, h = WHITE_KEY_DIMS if is_white else BLACK_KEY_DIMS
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255) # black border
    SDL_RenderDrawRect(renderer, SDL_Rect(x - 1, y - 1, w + 2, h + 2))

    r, g, b = ((WHITE_PIANO_COLOR if is_white else BLACK_PIANO_COLOR) 
                    if not is_played else PLAYED_PIANO_COLOR)
    SDL_SetRenderDrawColor(renderer, r, g, b, 255)
    SDL_RenderFillRect(renderer, SDL_Rect(x, y, w, h))

def calc_piano_key_x(n, x):
    drawx = x + ((n // 2) * WHITE_KEY_DIMS[0]) 
    if n % 2 == 0: 
        return drawx
    else:
        black_x_component = WHITE_KEY_DIMS[0] // 2 + BLACK_KEY_DIMS[0] // 3
        return drawx + black_x_component

def draw_octave(renderer, x, y, drawkeys):
    # White keys
    for i in range(0, 14, 2):
        drawx = calc_piano_key_x(i, x)
        played = i in drawkeys
        fill_piano_rect(renderer, drawx, y, True, played)
    # Black keys
    for i in range(1, 13, 2):
        drawx = calc_piano_key_x(i, x)
        played = i in drawkeys
        if i != 5:
            fill_piano_rect(renderer, drawx, y, False, played)

def octave_width():
    return WHITE_KEY_DIMS[0] * 7 

def piano_width():
    return octave_width() * NUM_OCTAVES

def draw_piano(renderer, piano_sound_queue):
    x, y = PIANO_LOCATION
    for i in range(NUM_OCTAVES):
        drawkeys = [p[1] % 14 for p in piano_sound_queue if p[1] // 14 == i]
        draw_octave(renderer, x + (i * octave_width()), y, drawkeys)

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
            if piano_key_x + BLACK_KEY_DIMS[0] > x >= piano_key_x and \
                                                        y < BLACK_KEY_DIMS[1]:
                if i == numkeys - 1 or x < calc_piano_key_x(i + 2, 0):
                    blackkey = i
    return blackkey if blackkey != -1 else whitekey

def calc_wheel_click(clickx, clicky, wheel):
    for i in range(len(wheel)):
        centerx, centery, r = wheel[i][0]
        if in_circle(centerx, centery, r, clickx, clicky):
            return i
    return -1

def focus_of_vec(vec):
    return [WHEEL_FOCUS, vec]

def create_waveform_matrix(wheel):
    return [[None for n in range(12 * NUM_OCTAVES)] for w in range(len(wheel))]

def waveform_lookup(wv_mat, wheel, w, n):
    if wv_mat[w][n] == None:
        wv_mat[w][n] = calculate_sound(wheel[w][1], n)
    return wv_mat[w][n]

def loop(renderer):
    radius = 0.5
    pressed_piano_key = -1
    event = SDL_Event()
    piano_sound_queue = []
    wheel_focus = focus_of_vec([0] * 4)
    neighbors = generate_neighbors_list(wheel_focus, radius)
    wheel = [wheel_focus] + neighbors
    waveform_matrix = create_waveform_matrix(wheel)
    wheel_highlight = 0
    previous_vectors = []
    while True:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                return
            elif event.type == SDL_MOUSEBUTTONDOWN:
                butx, buty = event.button.x, event.button.y
                # Check piano clicking
                pressed_piano_key = calc_piano_key_pressed(butx, buty)
                if pressed_piano_key != -1:
                    note = calc_piano_key(pressed_piano_key)
                    sound = waveform_lookup(waveform_matrix, wheel,  \
                                                    wheel_highlight, note)
                    piano_sound_queue.insert(0, [sound, pressed_piano_key, 0])
                    piano_sound_queue[0][0].play(-1)

                # Check clicking on wheel 
                new_highlight = calc_wheel_click(butx, buty, wheel)
                if new_highlight != -1: wheel_highlight = new_highlight

                # Check buttons
                if in_arrow(NEW_NEIGHBORS, butx, buty, False) and \
                                                                len(wheel) > 1:
                    previous_vectors.append(wheel_focus[1])
                    radius *= RADIUS_FACTOR
                    wheel_focus = focus_of_vec(wheel[wheel_highlight][1])
                    neighbors = generate_neighbors_list(wheel_focus, radius)
                    wheel = [wheel_focus] + neighbors
                    waveform_matrix = create_waveform_matrix(wheel)
                    wheel_highlight = 0
                elif in_arrow(BACK_BUTTON, butx, buty, True) and \
                                                    len(previous_vectors) > 0:
                    new_center_vec = previous_vectors.pop()
                    radius /= RADIUS_FACTOR
                    wheel_focus = focus_of_vec(new_center_vec)
                    neighbors = generate_neighbors_list(wheel_focus, radius)
                    wheel = [wheel_focus] + neighbors
                    waveform_matrix = create_waveform_matrix(wheel)
                    wheel_highlight = 0

        for i in range(len(piano_sound_queue)):
            if piano_sound_queue[i][2] < SOUND_FRAME_DURATION:
                piano_sound_queue[i][2] += 1
        while len(piano_sound_queue) > 0 and \
                    piano_sound_queue[-1][2] >= SOUND_FRAME_DURATION:
            piano_sound_queue[-1][0].stop()
            piano_sound_queue.pop()

        clear_screen(renderer)
        draw_piano(renderer, piano_sound_queue)
        draw_wheel(renderer, wheel, wheel_highlight)
        fill_arrow(renderer, NEW_NEIGHBORS, NEW_NEIGHBORS_COLOR, False)
        fill_arrow(renderer, BACK_BUTTON, BACK_BUTTON_COLOR, True)
        SDL_RenderPresent(renderer)
        SDL_Delay(FRAME_DURATION)

def main():
    SDL_Init(SDL_INIT_VIDEO)
    window = SDL_CreateWindow(b"Timbreline", SDL_WINDOWPOS_CENTERED, 
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
