import sys
import json
from app_ssplit import SentenceSplitter


ssplit = SentenceSplitter()
print(ssplit.annotate(open(sys.argv[1]).read()))
