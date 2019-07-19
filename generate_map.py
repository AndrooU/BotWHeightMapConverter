# Aaaboy97 2019

from PIL import Image
import array
import math
import os
import sys
import time

gen_all_maps = False


def generate_mdb(n):
    mdb = []
    i = 0
    while len(mdb) < n:
        if i & 0x55555555 == i:
            mdb.append(i)
        i += 1
    return mdb


def z_from_xy(xy, mdb):
    return mdb[xy[0]] + 2*mdb[xy[1]]


def draw_grid(grid_tl, grid_xy, detail, image, mdb):
    name = '5' + str(detail)
    grid_z = z_from_xy(grid_xy, mdb)

    name += format(grid_z, '0>8X')
    file = None
    try:
        file = open('terrain/' + name + '.hght', 'rb')
    except:
        return

    h = array.array('H')
    h.fromfile(file, 65536)
    h = h.tostring()
    temp = Image.frombytes('I;16', (256, 256), h)

    grid_rel_x = 256*(grid_xy[0] - grid_tl[0])
    grid_rel_y = 256*(grid_xy[1] - grid_tl[1])
    image.paste(temp, (grid_rel_x, grid_rel_y))

    file.close()


def draw_map(grid_tl, grid_br, detail, image, mdb):
    start = grid_tl[1]
    width = grid_br[1] - grid_tl[1]
    for y in range(grid_tl[1], grid_br[1] + 1):
        frac = 1
        if width != 0:
            frac = (y - start)/width
        fill = round(frac*40)
        print('\r[', '█'*fill + ' '*(40-fill), '] {:>7.2%}'.format(frac),
              sep='', end='')
        sys.stdout.flush()
        for x in range(grid_tl[0], grid_br[0] + 1):
            draw_grid(grid_tl, (x, y), detail, image, mdb)


def create_image(tl, br, detail, name=str(int(time.time()))):
    grid_size = 2**detail
    grid_tl = tuple([int(x*grid_size) for x in tl])
    grid_br = tuple([math.ceil(x*grid_size) - 1 for x in br])

    mdb = generate_mdb(grid_size)

    img_size = (256*(1 + grid_br[0] - grid_tl[0]),
                256*(1 + grid_br[1] - grid_tl[1]))
    img = Image.new('I', img_size)

    draw_map(grid_tl, grid_br, detail, img, mdb)
    print('\nSaving File as hghtmap_{}.png...'.format(name))
    img.save('hghtmap_{}.png'.format(name), 'PNG')
    print('Completed!')


def class_input(prompt, desired_type):
    output = None
    type_str = str(desired_type)[8:-2]
    asked_already = False
    while type(output) != desired_type:
        if not asked_already:
            asked_already = True
            output = input(prompt)
            try:
                output = desired_type(output)
            except:
                print('Please only enter a value of type {}'.format(type_str))
        else:
            output = input(prompt)
            try:
                output = desired_type(output)
            except:
                print('Please only enter a value of type {}'.format(type_str))

    return output


def main():
    if not os.path.isdir('terrain'):
        print('No terrain folder found! All .hght files must be in a folder')
        print('Named \'terrain\' in the same directory as this file!')
        input()
        return

    okay_boundaries = False
    print('Enter the boundaries of the desired region in order of left,')
    print('top, right, bottom as values from 0 to 1, with the top left')
    print('corner of the map being at (0, 0). For reference, the playable')
    print('region has boundaries (0.1875, 0.25, 0.8125, 0.75)')
    while not okay_boundaries:
        l = class_input('Left:   ', float)
        t = class_input('Top:    ', float)
        r = class_input('Right:  ', float)
        b = class_input('Bottom: ', float)
        if l > r:
            l, r = r, l
        if t > b:
            t, b = b, t
        if (l >= 0 and t >= 0 and r >= 0 and b >= 0 and
                l <= 1 and t <= 1 and r <= 1 and b <= 1):
            okay_boundaries = True
        else:
            print('Values must be between 0 and 1\n')
        if (l == r or t == b):
            okay_boundaries = False
            print('Cannot enter an region with size 0')

    okay_lod = False
    print('\nEnter the desired LOD to use (from 0 to 8)')
    while not okay_lod:
        lod = class_input('LOD: ', int)
        if lod >= 0 and lod <= 8:
            okay_lod = True
        else:
            print('Value must be between 0 and 8\n')

    print()
    create_image((l, t), (r, b), lod)
    print('\nPress any key to continue...', end='')
    input()

if __name__ == "__main__":
    if gen_all_maps:
        for i in range(9):
            create_image((0, 0), (1, 1), i, i)
    else:
        main()
