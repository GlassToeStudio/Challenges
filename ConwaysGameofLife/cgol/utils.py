""" Helper fuctions for conways_game_of_life. """
#!/usr/bin/env python3
import os
import subprocess as sp
import pyscreenshot as ImageGrab

def cls():
    """ Clear cmd window."""
    sp.call('cls', shell=True)
    return


def get_path():
    """ Return the current working directory."""
    return os.path.dirname(os.path.abspath(__file__))+'/'


def take_screenshot(index, screen_dimensions):
    """
        Take a screenshot of a bpxed area.
        Will save to: cgol/screenshots/

        int: index - for screenshots naming
        tuple: screen_dimensions - width and hight of boxed area

        Notes:
            Assumes CMD window is starts at 0, 0
    """

    screen_shot = ImageGrab.grab(bbox=(10, 31, (screen_dimensions[0] * 8),
                                       (screen_dimensions[1] * 12) + 29),
                                 childprocess=False) # X1,Y1,X2,Y2
    str_name = '{0}{1}{2}'.format('cgol/screenshots/screenshot_', str(index), '.png')
    screen_shot.save(str_name)
    return


def set_window_size(rows, columns):
    """
        Resize cmd window to fit current baord size.

        int: rows - for Y dimension
        int: columns = for X dimension
    """

    screen_dimensions = []
    screen_dimensions.append((columns * 2) + 35)
    screen_dimensions.append(rows + 12)
    os.system("mode con cols={0} lines={1}".format(screen_dimensions[0], screen_dimensions[1]))
    return screen_dimensions
