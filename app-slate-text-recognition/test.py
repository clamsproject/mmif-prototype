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
    #f.write(str(c.__dict__)) #TypeError: Object of type View is not JSON serializable
    #f.write(c) #TypeError: Object of type View is not JSON serializable
    json.dump(c, f)

for i in c.views:
    a = i.__dict__
    print (a)
    c = a.get("contains")
    bd = a.get("annotations")
    for d in bd:
        print (d.__dict__)
print (datetime.now()-st)