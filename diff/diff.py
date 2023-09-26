# diff_tool.py

import argparse
import difflib
import sys
from pathlib import Path


def create_diff(old_file: Path, new_file: Path, output_file: Path = None):
    file_1 = open(old_file, encoding='utf-8').readlines()
    file_2 = open(new_file, encoding='utf-8').readlines()

    if output_file:
        delta = difflib.HtmlDiff(
                tabsize=8, wrapcolumn=60, linejunk=None, charjunk=difflib.IS_CHARACTER_JUNK
            ).make_table(
                file_1, file_2,  fromdesc='old version', todesc='new version', context=True, numlines=5
                )
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(delta)
    else:
        delta = difflib.unified_diff(
            file_1, file_2, old_file.name, new_file.name)
        sys.stdout.writelines(delta)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("old_file_version")
    parser.add_argument("new_file_version")
    parser.add_argument("--html", help="specify html to write to")
    args = parser.parse_args()

    old_file = Path(args.old_file_version)
    new_file = Path(args.new_file_version)

    if args.html:
        output_file = Path(args.html)
    else:
        output_file = None

    create_diff(old_file, new_file, output_file)


if __name__ == "__main__":
    main()
