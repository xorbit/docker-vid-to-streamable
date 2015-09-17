#!/usr/bin/env python
"""Video convertor to turn video output from Panasonic WV-SC385
IP camera into smaller, streamable H.264 MP4 files

Main convertor program
This monitors the recordings directory. For every recording, it will
generate a streamable video. If a recording is removed, there will
be a stream without recording and it will be deleted.

Copyright (c) 2015 Patrick Van Oosterwijck
Distributed under GPL v2 license"""


import rec
import cfg
import time
import subprocess
import os
import os.path


def find_exclusive(list, other_list):
  """Find and return items present in list that aren't in other_list"""
  exclusive = []
  for item in list:
    if item not in other_list:
      exclusive.append(item)
  return exclusive

# Main loop
while True:
  # Get list of recordings
  recordings = rec.get_recordings(cfg.REC_PATH)
  # Get list of streams
  streams = rec.get_recordings(cfg.STREAM_PATH)
  # Find recordings for which no stream exists
  recordings_without_stream = find_exclusive(recordings, streams)
  print "Recordings without stream:"
  print map(lambda x: x['name'], recordings_without_stream)
  # Do we have recordings to convert?
  if recordings_without_stream:
    # Yes, then convert them
    for recording in recordings_without_stream:
      file = recording['name']
      destfile = os.path.join(cfg.STREAM_PATH, file)
      print "Converting %s to stream" % file
      try:
        subprocess.call(['/usr/bin/ffmpeg', '-i',
                         os.path.join(cfg.REC_PATH, file), '-movflags',
                         'faststart', '-codec:v', 'libx264', '-codec:a',
                         'copy', destfile])
        os.utime(destfile, (recording['mod_ts'], recording['mod_ts']))
      except:
        pass
    # Allow break
    time.sleep(0.5)
  else:
    # Find streams for which no recording exists
    streams_without_recording = find_exclusive(streams, recordings)
    print "Streams without recording:"
    print map(lambda x: x['name'], streams_without_recording)
    # Are there streams without recording?
    if streams_without_recording:
      # If so, delete them
      for recording in streams_without_recording:
        file = recording['name']
        print "Deleting stream %s" % file
        os.remove(os.path.join(cfg.STREAM_PATH, file))
    # Sleep
    time.sleep(5)
