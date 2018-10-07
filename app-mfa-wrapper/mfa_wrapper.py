import os
from clams.serve import ClamApp
from clams.serialize import *
from clams.vocab import AnnotationTypes
from clams.vocab import MediaTypes
from clams.restify import Restifier
import textgrid


class VanillaMFAWrapper(ClamApp):

    def appmetadata(self):
        # TODO (krim @ 10/7/2018): set up a proper tool metadata scheme
        metadata = {"name": "Vanilla Montreal Forced Aligner",
                    "description": "This tool wraps around Montreal Forced Aligner",
                    "vendor": "Team CLAMS",
                    "requires": [MediaTypes.A, MediaTypes.T],
                    "produces": [AnnotationTypes.FA]}
        return metadata

    def sniff(self, mmif):
        # this mock-up method always returns true
        return True

    def annotate(self, mmif_json):
        mmif = Mmif(mmif_json)
        audio_filename = mmif.get_medium_location(MediaTypes.A)
        transcript_filename = mmif.get_medium_location(MediaTypes.T)
        mfa_output = self.run_mfa(audio_filename, transcript_filename)
        # convert textgrid to a mmif view
        new_view = mmif.new_view()
        new_view.new_contain(AnnotationTypes.FA)
        tg = textgrid.TextGrid.fromFile(mfa_output)
        for int_id, interval in enumerate(tg.getFirst("words").intervals):
            annotation = new_view.new_annotation(int_id)
            annotation.start = str(interval.minTime)
            annotation.end = str(interval.maxTime)
            annotation.attype = AnnotationTypes.FA
            annotation.add_feature("word", interval.mark)

        for contain in new_view.contains.keys():
            mmif.contains.append({contain: new_view.id})
        return mmif

    @staticmethod
    def run_mfa(audio_filename, transcript_filename):
        # mock-up wrapper returns existing textgrid files
        if audio_filename.endswith("cpb-aacip-507-fj2988397d.wav"):
            return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "cpb-aacip-507-fj2988397d.TextGrid")
        else:
            raise NotImplementedError


if __name__ == "__main__":
    mfa_tool = VanillaMFAWrapper()
    mfa_service = Restifier(mfa_tool)
    mfa_service.run()



