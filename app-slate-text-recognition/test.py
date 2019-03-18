import sys
import json
from slate_recognition import SlateRecognition
from datetime import datetime

st = datetime.now()
sd = SlateRecognition()
a = open(sys.argv[1])
b = a.read()
c = sd.annotate(b)
with open("../test-jsons/slate-reco.json", "w") as f:
    f.write(str(c))

print (datetime.now()-st)