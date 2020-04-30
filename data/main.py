"""Main program file"""

import pygame

import data.constants as c
from data.events import Events
from data.grid import Grid
from data.player import Player
from data.snake import Snake
from data.view import View


def main():
    """Main program"""

    pygame.init()
    view = View()
    events = Events()
    player = Player()

    view.init_textures()
    view.update()
    player.retrieve_scores()

    main_loop = True
    active_game = False
    prev_state = None
    state = "MENU"

    # Main looop
    while main_loop:

        # Menu loop
        while main_loop and state == "MENU":

            if prev_state != state:
                view.draw_menu()
                view.update()
                active_game = False
                prev_state = state
            else:
                view.tick()

            actions = events.get()
            if "quit" in actions:
                main_loop = False
            if "enter" in actions:
                state = "GAME"

        # Game loop
        while main_loop and state == "GAME":

            if prev_state != "PAUSE":
                frames = 0

            if prev_state != state:
                if not active_game:
                    grid = Grid()
                    snake = Snake()
                    player.start_game()
                    snake.place_head(grid)
                    grid.generate()
                    direction = None
                    active_game = True
                prev_state = state

            view.draw_header(snake, player)

            while frames < c.NB_FRAMES:

                view.draw_field(grid, snake, frames)
                view.draw_game()
                view.update()

                view.tick()
                actions = events.get()
                if "quit" in actions:
                    main_loop = False
                if "escape" in actions:
                    state = "PAUSE"
                if not (main_loop and state == "GAME"):
                    break

                new_dir = events.calc_dir(snake.dir)
                if new_dir:
                    direction = new_dir

                frames += 1

            if snake.dead:
                state = "GAME OVER"
            if not (main_loop and state == "GAME"):
                break
            if not direction:
                continue

            player.calc_score()

            snake.place_head(grid)
            snake.move_body(grid, direction)
            snake.behind_trail(grid)
            snake.check_front(grid, player)

            snake.goal_reached(player)

            if player.goal_reached:
                player.inc_score()
                player.new_goal()

        # Pause
        while main_loop and state == "PAUSE":

            if prev_state != state:
                view.draw_pause()
                view.update()
                prev_state = state
            else:
                view.tick()

            actions = events.get()
            if "quit" in actions:
                main_loop = False
            if "unpause" in actions:
                state = "GAME"

        # Game over
        while main_loop and state == "GAME OVER":

            if prev_state != state:
                player.calc_score()
                player.compare_scores()
                view.draw_game_over(player)
                view.update()
                player.save_scores()
                prev_state = state
            else:
                view.tick()

            actions = events.get()
            if "quit" in actions:
                main_loop = False
            if "escape" in actions:
                state = "MENU"
            if "enter" in actions:
                state = "MENU"

    pygame.quit()
