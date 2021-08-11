#!/usr/bin/env python3
# Copyright 2021 wagga40 (https://github.com/wagga40)
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Project: sigma2CSV.py
Date: 07 aug 2021
Author: wagga40 (https://github.com/wagga40)
Version: 1.0
Description: 
    Asked by frak113 in issue #1787 (https://github.com/SigmaHQ/sigma/issues/1787#issuecomment-894618060)
    This script converts sigma rules to a CSV format for statistics puprpose. 
    For now, it only keeps title, description, level, tags and author fields.
    Feel free to modify it according to your needs.
Requirements:
    $ pip install pyyaml
"""

import yaml
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--rulesdirectory", help="Sub-directory generated by rules-search", required=True, type=str)
parser.add_argument("-f", "--fileext", help="Rule file extension", default="yml", type=str)
parser.add_argument("-d", "--delimiter", help="Separator", default=",", type=str)
parser.add_argument("--oneline", help="Put all tags on a single line", action="store_true")
args = parser.parse_args()

files = glob.glob(args.rulesdirectory + "/**/*." + args.fileext, recursive=True)
# for each file in the given directory
for file in files:
    d={}
    with open(file, 'r') as stream:
        docs = yaml.load_all(stream, Loader=yaml.FullLoader)
        for doc in docs:
            for k,v in doc.items():
                if k in ['title','description','tags','level','author']: # Modify here if you want to include other fields
                    d[k]=v
            # Check for optional fields
            if "author" not in d: d["author"]=""
            if "level" not in d: d["level"]=""
            if args.oneline: # All tags will be on a single line
                if "tags" in d:
                    expandTags = args.delimiter.join([ tags for tags in d["tags"] if "attack" in tags ]) # Only output attack related tags
                    print(f'{d["title"]}{args.delimiter}{d["description"]}{args.delimiter}{d["level"]}{args.delimiter}{d["author"]}{args.delimiter}{expandTags}')
                else:
                    print(f'{d["title"]}{args.delimiter}{d["description"]}{args.delimiter}{d["level"]}{args.delimiter}{d["author"]}')
            else: 
                if "tags" in d:
                    for tag in d["tags"]:
                        if "attack" in tag: # Only output attack related tags
                            print(f'{d["title"]}{args.delimiter}{d["description"]}{args.delimiter}{d["level"]}{args.delimiter}{d["author"]}{args.delimiter}{tag}')