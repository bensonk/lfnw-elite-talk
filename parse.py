#!/usr/bin/python
from pprint import pprint
from pymongo import Connection

def is_headline(line):
  line = line.strip()
  if line:
    return reduce(lambda a, b: a and b, [ x == "=" for x in line ])
  else:
    return False

def parse_file(fname):
  with open(fname) as f:
    lines = f.readlines()

  slide_indexes = []
  for i, line in enumerate(lines):
    if is_headline(line):
      slide_indexes.append(i-1)

  slides = []
  for i, j in zip(slide_indexes, slide_indexes[1:]):
    slides.append( { "title": lines[i], "body": "".join(lines[i+2:j]) } )
  return slides

def insert_slides(slides, show):
  db = Connection("mongodb://127.0.0.1:3002/meteor").meteor
  for i, slide in enumerate(slides):
    slide["show_id"] = show
    slide["current"] = False
    slide['order'] = i
    db.slides.insert(slide)

def handle_file(fname, show):
  slides = parse_file(fname)
  insert_slides(slides, show)

if __name__ == "__main__":
  from sys import argv
  if len(argv) != 3:
    print "Usage: ./parse.py <filename> <slideshow_id>"
  else:
    handle_file(argv[1], argv[2])
