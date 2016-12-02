#!/usr/bin/python3
""" Script to generate urls following a provided distribution.

Usage:

  generate_urls.py hits_frequency_file n_urls prefix output_file

Example:

  generate_urls.py hits_frequency.txt 100 example.com?a= out.txt

The hits frequency file should look like:

  1275358
  562369
  437312
  406583
  168296
  ...

where each line represents the frequency of some url in the underlying
distribution.

The output will look like:

  example.com?a=362
  example.com?a=48
  example.com?a=100
  example.com?a=1
  example.com?a=1000916
  ...

where the appended suffixes are indexes into the hits frequency file.  (The
expectation, however, is that the webserver will just treat them as unique urls,
so it doesn't actually matter that they have this correspondence.)
"""

import random
import sys


def start(hits_frequency_file, n_urls, prefix, output_file):
  n_urls = int(n_urls)

  with open(hits_frequency_file) as inf:
    total_hits = sum(int(line) for line in inf)

  targets = [random.randrange(0, total_hits) for _ in range(n_urls)]
  targets.sort()

  # We can make one pass over hits_frequency_file because targets is sorted in
  # ascending order: while we're looking to see if we've hit target=N then we
  # know we can ignore target=M (where M >= N).
  target = 0
  total_so_far = 0
  indexes = []
  with open(hits_frequency_file) as inf:
    for index, line in enumerate(inf):
      # If the hits frequency file starts:
      #   57
      #   22
      #   8
      # Then targets of 0-56 should get index=0, 57-78 should get index=1,
      # 79-86 get index=2, and so on.
      total_so_far += int(line)

      while target < len(targets) and targets[target] < total_so_far:
        # This is a loop because targets may have duplicates.
        indexes.append(index)
        target += 1

  random.shuffle(indexes)

  with open(output_file, "w") as outf:
    for index in indexes:
      outf.write("%s%s\n" % (prefix, index))

if __name__ == "__main__":
  start(*sys.argv[1:])
