# here we go mfer
import ctypes
from sdl2 import sdlimage as si
from sdl2 import *

WINDOW_HEIGHT = 860
WINDOW_WIDTH = 1024

def clear_screen(renderer):
    SDL_SetRenderDrawColor(renderer, 0, 255, 255, 255);
    SDL_RenderClear(renderer);


def loop(renderer):
    event = SDL_Event()
    while True:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                return

        clear_screen(renderer)
        SDL_RenderPresent(renderer)

def main():
    SDL_Init(SDL_INIT_VIDEO)
    window = SDL_CreateWindow(b"tamber", SDL_WINDOWPOS_CENTERED, 
                            SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, 
                            WINDOW_HEIGHT, SDL_WINDOW_SHOWN)
    rend_flags = SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC
    renderer = SDL_CreateRenderer(window, -1, rend_flags)

    loop(renderer)

    SDL_DestroyRenderer(renderer)
    SDL_DestroyWindow(window)
    SDL_Quit()
main()
