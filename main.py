#!/usr/bin/env python3
"""Copy the rendered front page to /output/entry.png.

The image (entry.png) is the entry: a 1024x1024 front page summing up
20 November 2026's world news, rendered once by render_20nov.py.
This program only copies it, so two runs write identical bytes.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
