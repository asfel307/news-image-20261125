#!/usr/bin/env python3
"""news-image-20261125 entry: copy the pre-rendered front page into the
output directory. Standard library only; a plain byte-for-byte copy, so
every run produces identical output.

Usage:  MAKEFUN_OUTPUT_DIR=out python3 main.py
        (falls back to ./out when the variable is unset)
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(
        os.getcwd(), "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("copied", src, "->", dst)


if __name__ == "__main__":
    main()
