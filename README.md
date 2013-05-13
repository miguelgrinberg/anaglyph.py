anaglyph.py
===========

Simple anaglyph image generator written in Python and PIL. Detailed tutorial and usage instructions are in my blog article: http://blog.miguelgrinberg.com/post/take-3d-pictures-with-your-canon-dslr-and-magic-lantern.

It can generate a few different types of stereo images:

- Red/cyan anaglyphs: true, monochrome, color, half color and optimized algorithms (see [this page](http://www.3dtv.at/knowhow/anaglyphcomparison_en.aspx) for algorithm details)

  <img src="http://blog.miguelgrinberg.com/static/images/3d-pictures-01-icon.jpg" />

- Stereo pairs: parallel or cross-eyed viewing, in color or monochrome

  <img src="http://blog.miguelgrinberg.com/static/images/3d-pictures-05-icon.jpg" />

- Wiggle 3D animated GIFs

  <img src="http://blog.miguelgrinberg.com/static/images/3d-pictures-08.gif" />

Run `./anaglyph.py --help` for usage information.


License
-------

(the MIT license)

Copyright (c) 2013 by Miguel Grinberg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

