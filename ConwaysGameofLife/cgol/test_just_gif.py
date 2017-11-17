''' Create animated gif from png files. '''
#!/usr/bin/env python3
import glob
import moviepy.editor as mpy


gif_name = 'cgol'
fps = 12
file_list = glob.glob('cgol/images/*.png')
list.sort(file_list, key=lambda x: int(x.split('_')[1].split('.png')[0]))
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_gif('cgol/images/{}.gif'.format(gif_name), fps=fps)
