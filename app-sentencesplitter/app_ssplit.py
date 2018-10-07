from clams.serve import ClamApp
from clams.serialize import *
from clams.vocab import AnnotationTypes
from clams.vocab import MediaTypes
from clams.restify import Restifier
import os
import nltk
from contextlib import redirect_stdout

with redirect_stdout(open(os.devnull, "w")):
    nltk.download('punkt')

class SentenceSplitter(ClamApp):

    def appmetadata(self):

        metadata = {"name": "NLTK sentence splitter",
                    "description": "This tool wraps around NLTK sentence splitter.",
                    "vendor": "Team CLAMS",
                    "requires": [MediaTypes.T],
                    "produces": [AnnotationTypes.Sentences]}
        return metadata

    def sniff(self, mmif):
        return True

    def annotate(self, mmif_json):
        mmif = Mmif(mmif_json)
        #  text_filename = mmif.get_medium_location(MediaTypes.T)
        text_filename = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "cpb-aacip-507-fj2988397d.lab")
        text_file = open(text_filename)
        text = text_file.read()
        text_file.close()
        sentences = nltk.tokenize.sent_tokenize(text)

        new_view = mmif.new_view()
        new_view.new_contain(AnnotationTypes.Sentences)
        cur = 0
        for idx, sentence in enumerate(sentences):
            annotation = new_view.new_annotation(idx)
            annotation.start = text.index(sentence,cur)
            annotation.end = annotation.start + len(sentence)
            annotation.attype = AnnotationTypes.Sentences

        for contain in new_view.contains.keys():
            mmif.contains.update({contain:new_view.id})
        return mmif

if __name__ == "__main__":
    ssplit_tool = SentenceSplitter()
    ssplit_service = Restifier(ssplit_tool)
    ssplit_service.run()
