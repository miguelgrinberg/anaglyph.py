#!/usr/bin/env python

# Copyright (c) 2013 by Miguel Grinberg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import optparse
from PIL import Image, ImageSequence
from images2gif import writeGif

matrices = {
    'true': [ [ 0.299, 0.587, 0.114, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 0, 0, 0.299, 0.587, 0.114 ] ],
    'mono': [ [ 0.299, 0.587, 0.114, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0.299, 0.587, 0.114, 0.299, 0.587, 0.114 ] ],
    'color': [ [ 1, 0, 0, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 1, 0, 0, 0, 1 ] ],
    'halfcolor': [ [ 0.299, 0.587, 0.114, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 1, 0, 0, 0, 1 ] ],
    'optimized': [ [ 0, 0.7, 0.3, 0, 0, 0, 0, 0, 0 ], [ 0, 0, 0, 0, 1, 0, 0, 0, 1 ] ],
}

def make_anaglyph(left, right, color, path):
    width, height = left.size
    leftMap = left.load()
    rightMap = right.load()
    m = matrices[color]

    for y in range(0, height):
        for x in range(0, width):
            r1, g1, b1 = leftMap[x, y]
            r2, g2, b2 = rightMap[x, y]
            leftMap[x, y] = (
                int(r1*m[0][0] + g1*m[0][1] + b1*m[0][2] + r2*m[1][0] + g2*m[1][1] + b2*m[1][2]),
                int(r1*m[0][3] + g1*m[0][4] + b1*m[0][5] + r2*m[1][3] + g2*m[1][4] + b2*m[1][5]),
                int(r1*m[0][6] + g1*m[0][7] + b1*m[0][8] + r2*m[1][6] + g2*m[1][7] + b2*m[1][8])
            )
    left.save(path)
    
def make_stereopair(left, right, color, path):
    width, height = left.size
    leftMap = left.load()
    rightMap = right.load()
    pair = Image.new('RGB', (width * 2, height))
    pairMap = pair.load()
    for y in range(0, height):
        for x in range(0, width):
            pairMap[x, y] = leftMap[x, y]
            pairMap[x + width, y] = rightMap[x, y]
    if color == 'mono':
        pair = pair.convert('L')
    pair.save(path)

def make_wiggle3d(left, right, color, path):
    if color == 'mono':
        left = left.convert('L')
        right = right.convert('L')
    writeGif(path, [left, right], 0.1, True, False, 0, False, 2)

def parse_arguments():
    parser = optparse.OptionParser(usage = 'usage: %prog [options] left_image right_image stereo_image')

    group = optparse.OptionGroup(parser, "Stereo image options")
    group.add_option('-a', '--anaglyph',
        action = 'store_const', const = 'anaglyph', dest = 'type', default = 'anaglyph',
        help = 'generate a stereo anaglyph (default)')
    group.add_option('-p', '--parallel',
        action = 'store_const', const = 'parallel', dest = 'type',
        help = 'generate a parallel viewing stereo pair')
    group.add_option('-x', '--crossed',
        action = 'store_const', const = 'crossed', dest = 'type',
        help = 'generate a crossed viewing stereo pair')
    group.add_option('-w', '--wiggle',
        action = 'store_const', const = 'wiggle', dest = 'type',
        help = 'generate a "Wiggle 3D" animated GIF file')
    parser.add_option_group(group)

    group = optparse.OptionGroup(parser, "Color options")
    group.add_option('-t', '--true',
        action = 'store_const', const = 'true', dest = 'color',
        help = 'generate a true color picture')
    group.add_option('-m', '--mono',
        action = 'store_const', const = 'mono', dest = 'color',
        help = 'generate a monochrome picture')
    group.add_option('-c', '--color',
        action = 'store_const', const = 'color', dest = 'color',
        help = 'generate a color picture')
    group.add_option('-f', '--halfcolor',
        action = 'store_const', const = 'halfcolor', dest = 'color',
        help = 'generate a half color picture')
    group.add_option('-o', '--optimized',
        action = 'store_const', const = 'optimized', dest = 'color', default = 'optimized',
        help = 'generate an optimized color picture (default)')
    parser.add_option_group(group)

    group = optparse.OptionGroup(parser, "Other options")
    group.add_option('-r', '--resize',
        action = 'store', type = 'int', dest = 'size', default = 0,
        help = 'resize image to the given width (height is automatically calculated to preserve aspect ratio)')
    parser.add_option_group(group)

    options, args = parser.parse_args()
    if len(args) != 3:
        parser.error('wrong number of arguments')

    leftImage = Image.open(args[0])
    pixelMap = leftImage.load()
    rightImage = Image.open(args[1])
    if leftImage.size != rightImage.size:
        parser.error('left and right images must have the same size')
    if options.size > 0:
        width, height = leftImage.size
        leftImage = leftImage.resize((options.size, options.size * height / width), Image.ANTIALIAS)
        rightImage = rightImage.resize((options.size, options.size * height / width), Image.ANTIALIAS)
    return options, leftImage, rightImage, args[2]

def main():
    options, leftImage, rightImage, stereoPath = parse_arguments()

    if options.type == 'anaglyph':
        make_anaglyph(leftImage, rightImage, options.color, stereoPath)
    elif options.type == 'parallel':
        make_stereopair(leftImage, rightImage, options.color, stereoPath)
    elif options.type == 'crossed':
        make_stereopair(rightImage, leftImage, options.color, stereoPath)
    elif options.type == 'wiggle':
        make_wiggle3d(leftImage, rightImage, options.color, stereoPath)

if __name__ == '__main__':
    main()
