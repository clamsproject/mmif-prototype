import sys
import json
from app_demux import Demuxer


demuxer = Demuxer()
print(demuxer.annotate(open(sys.argv[1]).read()))
