"""
    TODO:
        Save longest living cell - nah
        Stop after oscilating state (stable but with deaths and births)
            - Think a 3rd list will be needed archived, previous.., current
        Add command line args
        Allow input file to be 0 and 1, and convert to '  ' and ' o'.

    TODID:
        DONE: Load data from PNG image (Black and White only)
        DONE: Image resize is proportional to original image. (make_iamge.py)
        DONE: Can choose to wrap around indexes or stop at egdge.
        DONE: Make util module for util functions
        DONE: Incorporate make_gif
        DONE: Accept input file for initial state
        DONE: Add config variables to gameconfig dict.
        DONE: Add Global variables to stats dict
        DONE: Clear old screenshots before a new run.
        DONE: Save final iteration
        DONE: Save total births
        DONE: Save total deaths
        DONE: Stop when stable
        DONE: Stop when all dead
        DONE: Output statistics
        DONE: Dynamic sizing of console window based on grid size
        DONE: Dynamic sizing of screenshot area based on grid size
        DONE: Random initiial state population (with probability of life)
        DONE: Make gif from screenshots
        DONE: Create an __init__
        DONE: Take screenshots of cmd window
        DONE: Create cgol algorithm
"""

#!/usr/bin/env python3
from PIL import Image
from random import uniform
import os
import sys
import csv
import utils
import make_gif
import make_image

GAMECONFIG = {
    'dead_cells' : '  ',        # Character placed for a dead cell in console output
    'living_cells' : ' o',      # Character placed for a live cell in console output
    'chance_to_spawn' : 0.15,    # Use for random population, the change that is a cell is alive
    'board_size' : 50,          # By default, the board is square nxn
    'iterations' : 10,         # How many times to run the simulation
    'edge_buffer' : 0.1,        # Percentage of ege rows and columns omit from population
    'wrap_around' : True,       # Wrap around indices or stop at egdes
    'take_screenshot' : True,  # If True, a screenshot the cmd output/animated gif is created
    'make_image' : True,        # If True, write values to image/animated gif is created
    'resize_image' : True,      # If True, output png images will be resized.
    'load_from_file' : False,   # Choose to load from a file or make a random population
    'load_from_image' : False
    }

STATS = {
    'initial_population' : 0,
    'Births' : 0,
    'Deaths' : 0,
    'Cycles' : 0,
    'All_Dead' : False,
    'All_Alive' : False,
    'cycle_births' : 0,
    'cycle_deaths': 0
    }

# region Main
def main():
    """ Main """

    # Inital Setup
    load_from_file = GAMECONFIG['load_from_file']
    load_from_image = GAMECONFIG['load_from_image']
    dead_cells = GAMECONFIG['dead_cells']
    loops = GAMECONFIG['iterations']
    take_screenshot = GAMECONFIG['take_screenshot']
    make_images = GAMECONFIG['make_image']
    current_loop = 0

    #clean up
    clean_up_files(make_images, take_screenshot)

    # Load a random board based on game config
    if load_from_file == load_from_image:
        rows = GAMECONFIG['board_size']
        columns = GAMECONFIG['board_size']
        screen_w_h = resize_output_window(take_screenshot, rows, columns)
        current_cycle_data = [[dead_cells for i in range(columns)] for j in range(rows)]
        randomly_populate_board(current_cycle_data)
    # Load from image
    elif load_from_image:
        current_cycle_data, rows, columns = load_board_from_image('image.png')
        screen_w_h = resize_output_window(take_screenshot, rows, columns)
    # Load from file
    elif load_from_file:
        current_cycle_data, rows, columns = load_board_from_file('input_file.csv')
        screen_w_h = resize_output_window(take_screenshot, rows, columns)

    previous_cycle_data = [[dead_cells for i in range(columns)] for j in range(rows)]
    save_previous_cycle_iteration(current_cycle_data, previous_cycle_data)
    #create_png_image(current_cycle_data, current_loop, make_images)

    # Begin simulation loop
    while current_loop <= loops:
        if STATS['All_Dead'] is True:
            everyone_died(current_cycle_data, current_loop, screen_w_h, take_screenshot)
            break
        if STATS['All_Alive'] is True:
            noone_died(current_cycle_data, current_loop, screen_w_h,take_screenshot)
            break

        format_and_print_output(current_cycle_data)
        screenshot_windows(current_loop, screen_w_h, take_screenshot)

        if current_loop < loops:
            utils.cls()

        create_png_image(current_cycle_data, current_loop, make_images)
        next_life_cycle_iteration(previous_cycle_data, current_cycle_data)

        current_loop += 1
        STATS['Cycles'] = current_loop

    # Simulation complete, make an animated gif
    make_gifs(make_images, take_screenshot)
#endregion

# region Loading Options
def load_board_from_file(file_name):
    """ Load a csv file and return a 2D list."""

    # File does not exist, throw error and exit
    if not os.path.isfile(utils.get_path() + file_name):
        print('file does not exist')
        sys.exit()
    else:
        living_cells = GAMECONFIG['living_cells']
        data = list(csv.reader(open(utils.get_path() + file_name)))
        rows = len(data)
        columns = len(data[0])

        for row in range(0, rows):
            for col in range(0, columns):
                if data[row][col] == living_cells:
                    STATS['initial_population'] += 1

    return data, rows, columns

def load_board_from_image(file_name):
    """ Load a csv file and return a 2D list."""

    # File does not exist, throw error and exit
    if not os.path.isfile(utils.get_path() + file_name):
        print('file does not exist')
        sys.exit()
    else:
        dead_cells = GAMECONFIG['dead_cells']
        living_cells = GAMECONFIG['living_cells']

        im = Image.open(utils.get_path() + file_name)
        if im.mode not in ('L', 'RGB'):
            im = im.convert('RGB')
        pixel_values = im.load()
        width, height = im.size
        make_image.save_width_height(width, height)
        data = [[dead_cells for i in range(width)] for j in range(height)]

        for col in range(0, width):
            for row in range(0, height):
                if pixel_values[col, row] == (0, 0, 0):
                    data[row][col] = living_cells
                    STATS['initial_population'] += 1
        im.close()
    return data, height, width

def randomly_populate_board(board):
    """ Populate a 2D list with a chance of spawning a live cell."""

    buffer = GAMECONFIG['edge_buffer']
    chance_to_spawn = GAMECONFIG['chance_to_spawn']
    living_cells = GAMECONFIG['living_cells']
    dead_cells = GAMECONFIG['dead_cells']

    rows = len(board)
    columns = len(board[0])

    for row in range(int(rows * buffer), rows - (int(rows * buffer))):
        for col in range(int(columns * buffer), columns - (int(columns * buffer))):
            rand_num = uniform(0, 1)
            if rand_num > (1 - chance_to_spawn):
                STATS['initial_population'] += 1
                board[row][col] = living_cells
            else:
                board[row][col] = dead_cells
    return
# endregion

# region Conways game of life functions
def next_life_cycle_iteration(previous_cycle, current_cycle):
    """ 
        Start the next iteration of the simulation.
        Will save previous cycle data.
    """

    STATS['All_Dead'] = True
    STATS['All_Alive'] = True
    STATS['cycle_births'] = 0
    STATS['cycle_deaths'] = 0

    rows = len(previous_cycle)
    columns = len(previous_cycle[0])

    for row in range(0, rows):
        for col in range(0, columns):
            live_neighbors = count_neighbors(previous_cycle, row, col)
            check_conway_rules(previous_cycle, current_cycle, row, col, live_neighbors)

    STATS['Deaths'] += STATS['cycle_deaths']
    STATS['Births'] += STATS['cycle_births']
    save_previous_cycle_iteration(current_cycle, previous_cycle)
    return

def count_neighbors(previous_cycle, r, c):
    """ Count total number of living cells around a given cell."""

    living_cells = GAMECONFIG['living_cells']
    wrap_around = GAMECONFIG['wrap_around']

    rows = len(previous_cycle)
    columns = len(previous_cycle[0])

    total_neighbors = 0
    for row in range((r - 1), (r + 2)):
        for col in range((c - 1), (c + 2)):
            if row != r or col != c: # Dont count yourself as a neighbor.
                # If True, allow the board to loop from the last index back to 0 and vice versa
                if wrap_around:
                    if previous_cycle[row % rows][col % columns] == living_cells:
                        total_neighbors += 1
                else:
                    if (row < rows and row >= 0 and col < columns and col >= 0
                            and previous_cycle[row][col] == living_cells):
                        total_neighbors += 1

    return total_neighbors

def check_conway_rules(previous_cycle, current_cycle, row, column, live_neighbors):
    """
        Any LIVE cell with fewer than TWO live neighbours dies, as if caused by underpopulation.
        Any LIVE cell with TWO or THREE live neighbours lives on to the next generation.
        Any LIVE cell with more than THREE live neighbours dies, as if by overpopulation.
        Any DEAD cell with exactly THREE live neighbours becomes a live cell, as if by reproduction.
    """

    dead_cells = GAMECONFIG['dead_cells']
    living_cells = GAMECONFIG['living_cells']

    # rules for living cells
    if previous_cycle[row][column] == living_cells:
        if live_neighbors < 2:
            current_cycle[row][column] = dead_cells
            STATS['All_Alive'] = False
            STATS['cycle_deaths'] += 1
        elif live_neighbors == 2 or live_neighbors == 3:
            current_cycle[row][column] = living_cells
            STATS['All_Dead'] = False
        else:
            current_cycle[row][column] = dead_cells
            STATS['All_Alive'] = False
            STATS['cycle_deaths'] += 1

    # rules for dead cells
    else:
        if live_neighbors == 3:
            current_cycle[row][column] = living_cells
            STATS['All_Dead'] = False
            STATS['All_Alive'] = False
            STATS['cycle_births'] += 1
        else:
            current_cycle[row][column] = dead_cells
    return

def save_previous_cycle_iteration(from_board, to_board):
    """ Copy contents of current cycle to previous cycle. """

    rows = len(from_board)
    columns = len(from_board[0])

    for row in range(0, rows):
        for col in range(0, columns):
            to_board[row][col] = from_board[row][col]
    return
# endregion

# region Helper functions
def everyone_died(current_cycle_data, current_loop, screen_w_h, take_screenshot):
    """ Everyone is dead, display final output. """

    format_and_print_output(current_cycle_data)
    print("\n\tEveryone died after: {} iterations".format(current_loop))
    screenshot_windows(current_loop, screen_w_h, take_screenshot)

def noone_died(current_cycle_data, current_loop, screen_w_h,take_screenshot):
    """ No new births or deaths, display final output. """

    format_and_print_output(current_cycle_data)
    print("\n\tSimulation is stable after: {} iterations".format(current_loop))
    screenshot_windows(current_loop, screen_w_h, take_screenshot)

def format_and_print_output(board):
    """ Create a printable board and output to console."""

    rows = len(board)
    columns = len(board[0])

    output = ''
    for row in range(0, rows):
        output += ' |\t'
        for col in range(0, columns):
            output += '{}'.format(board[row][col])
        if row == 1:
            output += '\t|  --------------\n'
        elif row == 2:
            output += '\t|  New Births: {}\n'.format(STATS['cycle_births'])
        elif row == 4:
            output += '\t|  New Deaths: {}\n'.format(STATS['cycle_deaths'])
        elif row == 5:
            output += '\t|  --------------\n'
        else:
            output += '\t|\n'
    output += ("\n \tInitial Population {0}\n"
               " \tTotal Births: {1}\n"
               " \tTotal Deaths: {2}\n"
               " \tCurrent Iteration: {3}/{4}\n".format(
                   STATS['initial_population'],
                   STATS['Births'],
                   STATS['Deaths'],
                   STATS['Cycles'],
                   GAMECONFIG['iterations']
                   )
              )
    print(output)
    return
# endregion

# region Wrappers for util and image functions...
def create_png_image(board, current_loop, make_images):
    """ IMAGE FUNCTIONS ARE IN HERE! """

    if make_images is True:
        living_cells = GAMECONFIG['living_cells']
        resize_image = GAMECONFIG['resize_image']

        rows = len(board)
        columns = len(board[0])

        image, pixels = make_image.create_new_image(rows, columns)

        for row in range(0, rows):
            for col in range(0, columns):
                if board[row][col] == living_cells:
                    make_image.set_live_pixel(pixels, col, row)
        make_image.save_image(image, current_loop, resize_image)
    return

def clean_up_files(make_images, take_screenshot):
    """ clean up """

    if make_images is True:
        make_gif.remove_old_files('images')
    if take_screenshot is True:
        make_gif.remove_old_files('screenshots')
    return

def resize_output_window(take_screenshot, rows, columns):
    """ resize output window """

    screen_w_h = (0, 0)
    if take_screenshot is True:
        screen_w_h = utils.set_window_size(rows, columns)
    return screen_w_h

def screenshot_windows(current_loop, screen_w_h, take_screenshot):
    """ take screenshot """

    if take_screenshot is True:
        utils.take_screenshot(current_loop, screen_w_h)
    return

def make_gifs(make_images, take_screenshot):
    """ make animated gifs """

    if make_images is True:
        make_gif.save_gif('images')
    if take_screenshot is True:
        make_gif.save_gif('screenshots')
    return
#endregion
