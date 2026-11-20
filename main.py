#!/usr/bin/env python3
"""Entry point for the 20 November news-image entry.

Copies the rendered front page (entry.png, in this repository's root)
into the output directory so the harness can collect it. No network,
no extra work: the image is already rendered by render_20nov.py.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("OUTPUT_DIR", "/output")


def main():
    if not os.path.isfile(SRC):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    dst = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
