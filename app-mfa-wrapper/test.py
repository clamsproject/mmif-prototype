import sys
import json
from mfa_wrapper import VanillaMFAWrapper


mfa = VanillaMFAWrapper()
print(mfa.annotate(open(sys.argv[1]).read()))
