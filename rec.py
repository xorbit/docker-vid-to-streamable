"""Video convertor to turn video output from Panasonic WV-SC385
IP camera into smaller, streamable H.264 MP4 files

This module provides helper functions to deal with recordings

Copyright (c) 2015 Patrick Van Oosterwijck
Distributed under GPL v2 license"""

import os
import os.path
from datetime import datetime
import re


recformat = re.compile(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})_' +
      r'(?P<hour>\d{2})(?P<min>\d{2})(?P<sec>\d{2})(?P<milli>\d{3})\.mp4')

def get_recordings(path):
  """Get all correctly formatted recordings, their modified time, size and
  filename derived timestamp, from the provided path"""
  files = [rec for rec in os.listdir(path) if rec.endswith('.mp4')]
  recordings = []
  for name in files:
      recnameparse = recformat.match(name)
      if recnameparse:
          name_ts = datetime(
                  int(recnameparse.group('year')),
                  int(recnameparse.group('month')),
                  int(recnameparse.group('day')),
                  int(recnameparse.group('hour')),
                  int(recnameparse.group('min')),
                  int(recnameparse.group('sec')))
          stat = os.stat(os.path.join(path, name))
          recordings.append({
              'name': name,
              'name_ts': name_ts,
              'mod_ts': round(stat.st_mtime, 2)
          })
  return recordings

