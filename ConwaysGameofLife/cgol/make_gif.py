''' Create animated gif from png files. '''

#!/usr/bin/env python3
import os
import glob
import time
import moviepy.editor as mpy


def save_gif(folder='screenshots'):
    """
        Search for all png images in cgol/screenshots/ and
        convert to an animatied gif.

        gif saved in cgol/gif/.
    """

    gif_name = 'cgol' + str(time.time())
    fps = 12
    file_list = glob.glob('cgol/{}/*.png'.format(folder))
    list.sort(file_list, key=lambda x: int(x.split('_')[1].split('.png')[0]))
    clip = mpy.ImageSequenceClip(file_list, fps=fps)
    clip.write_gif('cgol/{}/gif/{}.gif'.format(folder, gif_name), fps=fps)
    return

# TODO: Should move to utils and create arg for file type .png, .gif
def remove_old_files(folder='screenshots'):
    """ Delete all *.png files from given folder."""

    for old_file in glob.glob('cgol/{}/*.png'.format(folder)):
        os.remove(old_file)
    return

def remove_old_gifs(folder='screenshots'):
    """ Delete all *.gif files from gvien folder."""

    for old_file in glob.glob('cgol/{}/gif/*.gif'.format(folder)):
        os.remove(old_file)
    return
