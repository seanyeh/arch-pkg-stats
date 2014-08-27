#!/usr/bin/env python

import argparse
import datetime
import json
import subprocess

def run_cmd(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True)
        return output.decode("utf-8").strip().split("\n")
    except subprocess.CalledProcessError:
        return None


def generate_stats(bin_full_path=False):
    # Get all packages
    packages = run_cmd("pkgfile -r \"\"")

    # Create dict {bin_name: [pkg1, pkg2,...], ...}
    pkg_dict = {}
    for pkg in packages:
        output = run_cmd("pkgfile -l -b %s" % pkg)

        # If no bin files, ignore
        if not output:
            continue

        # each line is pkg_name\tbin_file
        for line in output:
            pkg_name, bin_file = line.split("\t")

            if not bin_full_path:
                bin_file = bin_file[bin_file.rindex("/") + 1:]

            if not bin_file in pkg_dict:
                pkg_dict[bin_file] = []

            pkg_dict[bin_file].append(pkg_name)

    return pkg_dict


def write_json(filename, pkg_dict):
    # Add last_updated timestamp
    d = {
        "last_updated": str(datetime.datetime.now()),
        "files": pkg_dict
        }

    outfile = open(filename, 'w')
    with outfile:
        json.dump(d, outfile, sort_keys=True, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("outfile", metavar="OUTFILE", type=str,
            help="JSON output filename")
    args = parser.parse_args()

    d = generate_stats()
    write_json(args.outfile, d)


if __name__ == "__main__":
    main()
