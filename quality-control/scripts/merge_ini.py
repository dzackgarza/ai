"""Merge two INI files using ConfigParser and write the result to a third file.

Usage:
    python3 merge_ini.py <global_ini> <local_ini> <output_ini>

The local ini is applied on top of the global ini: duplicate section keys from
the local file extend or override those in the global file, which is the
standard ConfigParser behaviour when read_string is called twice.
"""

import configparser
import sys


def main() -> None:
    global_path, local_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    parser = configparser.RawConfigParser()
    with open(global_path) as f:
        parser.read_string(f.read())
    with open(local_path) as f:
        parser.read_string(f.read())
    with open(out_path, "w") as f:
        parser.write(f)


if __name__ == "__main__":
    main()
